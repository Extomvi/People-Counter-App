"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60


def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser


def connect_mqtt():
    ### TODO: Connect to the MQTT client ###
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    return client


def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    total_count = 0
    last_count = 0
    start_time = 0
    request_id = 0
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    prob_threshold = args.prob_threshold

    ### TODO: Load the model through `infer_network` ###
    infer_network.load_model(args.model, args.device)
    net_input_shape = infer_network.get_input_shape()
    ### TODO: Handle the input stream ###
    if args.input == "CAM":
        input_stream = 0
    else:
        input_stream = args.input
        assert os.path.isfile(args.input), "Specified input file doesn't exist"

    try:
        cap = cv2.VideoCapture(args.input)
    except FileNotFoundError:
        print("Cannot locate video file: " + args.input)
    except Exception as e:
        print("Something went wrong with the video file: ", e)
        
    if input_stream:
        cap.open(args.input)
    if not cap.isOpened():
        log.error("Can't open video source")
        
    width = int(cap.get(3))
    height = int(cap.get(4))
    ### TODO: Loop until stream is over ###

        ### TODO: Read from the video capture ###

        ### TODO: Pre-process the image as needed ###

        ### TODO: Start asynchronous inference for specified request ###

        ### TODO: Wait for the result ###

            ### TODO: Get the results of the inference request ###

            ### TODO: Extract any desired stats from the results ###

            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###
            ### Topic "person/duration": key of "duration" ###

        ### TODO: Send the frame to the FFMPEG server ###

        ### TODO: Write an output image if `single_image_mode` ###
    while cap.isOpened():
        # Read the next frame
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)
        pro_frame = cv2.resize(frame, (net_input_shape[3], net_input_shape[2]))
        pro_frame = pro_frame.transpose((2,0,1))
        pro_frame = pro_frame.reshape(1, *pro_frame.shape)

        inf_start = time.time()
        infer_network.async_inference(pro_frame)
            
        if infer_network.wait() == 0:
            det_time = time.time() - inf_start
            result = infer_network.get_output()
                
            current_count = 0
            for box in result[0][0]: 
                # Draw bounding box for object when it's probability is more than
                #  the specified threshold
                conf = box[2]
                if box[2] > prob_threshold:
                    xmin = int(box[3] * width)
                    ymin = int(box[4] * height)
                    xmax = int(box[5] * width)
                    ymax = int(box[6] * height)
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (225, 225, 225), 1)
                    current_count = current_count + 1
            inf_time_message = "Inference time: {:.3f}ms" \
                .format(det_time * 1000)
            cv2.putText(frame, inf_time_message, (15, 15),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (200, 10, 10), 1)
            if current_count > last_count:
                start_time = time.time()
                total_count = total_count + current_count - last_count
                client.publish("person", json.dumps({"total": total_count}))
            if current_count < last_count:
                duration = int(time.time() - start_time)
                client.publish("person/duration",
                               json.dumps({"duration": duration}))
            client.publish("person", json.dumps({"count": current_count}))
            last_count = current_count

            if key_pressed == 27:
                break
        sys.stdout.buffer.write(frame)
        sys.stdout.flush()
        
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()
    infer_network.clear()
        

def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
    exit(0)

