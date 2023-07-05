gradcam
==============

This file includes the ``GradCAM`` class, which implements the GradCAM algorithm for visualizing and analyzing deep neural networks. 


Initialization
---------------

This initilizes the ``GradCAM`` object by setting the provided model and layer name. 
If a layer name in not provided, the last convolutional layer will be used. 


.. code-block:: python

     def __init__(self, model=None, layer_name=""):


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

    def insert_into_runtime(self, path_to_image, plot_type_id, model_id, runnum=0):


Parameters
~~~~~~~~~~~~~~~~~~~~~~~

- ``path_to_image``: A string representing the path to the image file. 
- ``plot_type_id``: An integer representing the plot ID in the datbase. 
- ``model_id``: An interger representing the model ID in the database. This is set to -1 if no model is available. 
- ``runnum``: An optional integer representing the run number 


Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    if modelID==-1 :
            print("True")
            grad=GradCAM(None,-1)
            grad.insert_into_runtime(args["input"],-1,-1,runnum)

