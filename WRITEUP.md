# PEOPLE COUNTER APP DOCUMENTATION

## Explaining Custom Layers

The process behind converting custom layers involves:
The link to the faster-rcnn-inception used: http://download.tensorflow.org/models/object_detection/faster_rcnn_inception_v2_coco_2018_01_28.tar.gz

The process behind converting custom layers differs, depending on the original model framework. However, in both Tensorflow and Caffe, the first option is to register the custom layers as extensions to the Model Optimizer.
For Tensorflow, the second option is to replace the unsupported subgraph with a different subgraph and offload the computation of the subgraph back to Tensorflow during inference. While for Caffe, is to register the layers as Custom, then use Caffe to calculate the output shape of the layer.
Some of the potential reasons for handling custom layers are as follows:
● If a topology contains any layers that are not in the list of known layers.
● If a device doesn't support a particular layer.
### Procedure on the command line
- wget 'link to the model'
- tar -xvf faster_rcnn_inception_v2_coco_2018_01_28.tar.gz
- cd to the directory i.e cd faster_rcnn_inception_v2_coco_2018_01_28
- Run this code to use the model optimizer
python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/faster_rcnn_support.json 


Some of the potential reasons for handling custom layers are:
- To utilize the .xml and .bin files in the model
- To increase the model speed for output

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were:
- Less impact on the network
- Faster inference
- Smaller model size lessen need for on-device memory 
- Faster models free up computation


The difference between model accuracy pre- and post-conversion was:
- The accuracy of the post conversion was faster and higher

The size of the model pre- and post-conversion was:
- Pre-model size was: 143MB
- Post-model size was: 1.2GB

The inference time of the model pre- and post-conversion was - 153.49 sec

## Assess Model Use Cases

Some of the potential use cases of the people counter app are:
### Educational Institutions:
* For attendance register in a lecture halls. It’ll be useful because it’ll be able to count the total number of people that came into the hall per lecture and cross-check with the total number of people that signed into the class for the lecture so as to detect those that didn’t attend a lecture and their signature was seen in the attendance register.

### Shopping Malls: 
- Shopping Malls draw lots of visitor traffic; not only because of shopping opportunities but also for entertainment value. With people counting, one will be able to see which areas are most crowded and attractive, thus, shape marketing attractions and planning accordingly.

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows:

- Optimization for several models differs from what the individual model is used for and how much memory it can take while processing. A model that performs several tasks would require more memory size and network, but a singular model would not require so much memory size, thereby making it have a higher speed.
- High accuracy, if more resources are available
- Low-power devices will likely have to sacrifice some accuracy for a lighter, faster app, and need some additional considerations about network usage.


## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
  
- Model 2: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

