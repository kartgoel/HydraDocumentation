gradcam
==============

This file includes the ``GradCAM`` class, which implements the GradCAM algorithm for visualizing and analyzing deep neural networks. 


Initialization
---------------

The ``__init__`` method initilizes the ``GradCAM`` object by setting the provided model and layer name. 
If a layer name in not provided, the last convolutional layer will be used. 


.. code-block:: python

     def __init__(self, model=None, layer_name=""):
        print("init gradcam")
        print(model)
        self.model = model

        self.layer_name = layer_name
        if layer_name!="":
            self.layer_name = layer_name
            try:
                layer=self.model.get_layer(self.layer_name)
            except Exception as e:
                print(f"Error getting the layer: {e}", "reverting to last convolutional layer")
                self.layer_name = ""
        
        if self.layer_name=="" and self.model is not None:
            for layer in reversed(self.model.layers):
                if isinstance(layer, tf.keras.layers.Conv2D):
                    self.layer_name = layer.name
                    break
        

        if self.layer_name == "":
            print("Error finding the last convolutional layer")
        
        print("layer name:",self.layer_name)

        try:
            self.grad_model = tf.keras.models.Model([self.model.inputs], [self.model.get_layer(self.layer_name).output, self.model.output])
        except Exception as e:
            print(f"Error getting the model: {e}")
            self.grad_model = None


Parameters 
~~~~~~~~~~~~~~

- ``model``: An optional object representing a trained AI model. 
- ``layer_name``: An optional string corresponding to a specific layer in the AI model.


----------------------------------------------------------------------

get_heatmap
-----------------

This method generates the GradCAM heatmap for the given image path.

.. code-block:: python

    def get_heatmap(self, path_to_image, pred_index=None):
        print("getting heatmap")
        print(self.grad_model)
        if self.grad_model is None:
            return None
        
        input_shape=self.model.input_shape[1:]
        print("input shape",input_shape)
        print("reading image:",path_to_image)
        image = cv2.imread(path_to_image, cv2.IMREAD_COLOR)
        #image = cv2.resize(image, input_shape[:2])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype('float32')
        image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
        #image=image.transpose(1,0,2)
        tensor = tf.convert_to_tensor(image)
        tensor = np.expand_dims(tensor, axis=0)
        print("post tensor")
        with tf.GradientTape() as tape:
            last_conv_layer_output, preds = self.grad_model(tensor)            
            if pred_index is None:
                pred_index = tf.argmax(preds[0])
            class_channel = preds[:, pred_index]

        grads = tape.gradient(class_channel, last_conv_layer_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        heatmap_rgb = cm.coolwarm(heatmap)[:, :, :3] * 255
        heatmap_rgb = heatmap_rgb.astype('uint8')
        heatmap = cv2.resize(heatmap_rgb, (tensor.shape[2], tensor.shape[1]))
        
        print(preds)
        print(pred_index)
        return heatmap, preds, pred_index
    
    # add in a mysqldb connection to put the heatmap into the database

Parameters 
~~~~~~~~~~~~~~~~~~~

- ``path_to_image``: A string representing the path to the image file. 
- ``pred_index``: An optional integer representing the predicted class index. 


Example Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

     if model_id!=-1:
            gradCAMheatmap, preds, top_class_index = self.get_heatmap(path_to_image)
        


------------------------------------------------------------------

insert_into_runtime
---------------------

This method inserts the GradCAM heatmap and related information into the runtime database. 

.. code-block:: python 

    # Extended code available on Github
    def insert_into_runtime(self, path_to_image, plot_type_id, model_id, runnum=0):


Parameters
~~~~~~~~~~~~~~~~~~~~~~~

- ``path_to_image``: A string representing the path to the image file. 
- ``plot_type_id``: An integer representing the plot ID in the datbase. 
- ``model_id``: An integer representing the model ID in the database. This is set to -1 if no model is available. 
- ``runnum``: An optional integer representing the run number 


Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    if modelID==-1 :
            print("True")
            grad=GradCAM(None,-1)
            grad.insert_into_runtime(args["input"],-1,-1,runnum)

