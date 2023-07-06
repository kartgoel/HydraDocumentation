hydra_predict
====================================================

This file generates a report using the GradCAM and AI model. 
It preloads the AI models from the database and performs a prediction and evaluation of the input plots.
The results of the AI model predictions are reported and stored in the appropriate location for the 'Keeper'.


WriteReport
--------------

This method writes the prediction report based on the model's predictions. 

.. code-block:: python

    def WriteReport(plotType_ID,model_ID,to_pred,preds,labels_of_model,outfile,outdir,debug_mode=False):


Parameters
~~~~~~~~~~~~~

- ``plotType_ID``:An integer representing the plot ID in the database. 
- ``model_ID``: An interger representing the AI model ID in the database. 
- ``to_pred``: A string representing the path of the image to be predicted. 
- ``preds``: A list of floats representing the predicted labels for the plots. 
- ``labels_of_model``: A string representing the labels associated with the AI model. 
- ``outfile``: A string representing the output file path where the report will be written. 
- ``outdir``: A string representing the output directory where the plot will be moved. 
- ``debug_mode``: An optional boolean that will run the script in debug mode when 'True'. Defaults to 'False'.


Example Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    WriteReport(plotType_ID,model_ID,to_pred[i],preds,labels_of_model,outfile,OutDir.value,gradCAMheatmap,debug_mode)


--------------------------------------------

Breakfast 
---------------

This method performs a prediction using a specified AI model and dataset. 

.. code-block:: python 

    def Breakfast(hydraHeads, headkey):


Parameters
~~~~~~~~~~~~~~~~~~~~

- ``hydraHeads``: A dictionary which contains the AI model instances. 
- ``headkey``: A string representing the key to access the specific AI model instances.

Example Usage 
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    breakfast_path=parms["DATA_LOCATION"]["Breakfast"]


----------------------------------------------

CheckForKeeper
------------------

This method checks for the presence of a 'Keeper' by listening to a specified connection and port. 

.. code-block:: python 

    def CheckForKeeper(hasKeeper,keeperHost,keeperPort):


Parameters 
~~~~~~~~~~~~~~~~~~

- ``hasKeeper``: A Value object (integer) indicating the presence of a Keeper process. 
- ``keeperHost``: A string representing the hostname or IP address of the Keeper process. 
- ``keeperPort``: An integer representing the port number on which the Keeper process is running. 


Example Usage 
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

     p=Process(target=CheckForKeeper,args=(hasKeeper, keeperHost, keeperPort))


-----------------------------------------------------

PreloadModels
---------------

 This method preloads the AI models from the database and returns them as a dictionary. 

 .. code-block:: python

    def PreloadModels(DBConnector, ModelRootPath):


Parameters 
~~~~~~~~~~~~~~~

- ``DBConnector``: An object represents the connector for the database that is responsible for executing queries
- ``ModelRootPath``: A string representing the root path to the directory containing the AI models. 

Example Usage   
~~~~~~~~~~~~~

.. code-block:: python 

    hydraHeads = PreloadModels(DBConnector, ModelRootPath)


