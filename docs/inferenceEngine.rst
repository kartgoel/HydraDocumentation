inference_engine
=====================

This file includes the ``InferenceEngine`` class, which performs data analysis and prediction. 


Initialization
------------------

The ``__init__`` method initializes the ``InferenceEngine`` object. 

.. code-block:: python

    def __init__(self, DBConnector, data, debug_mode=False, ModelRootPath="DB", ChunkNumber=0, ForceModel_ID=-1, forcedPlotType=None, outfile="", hydraHeads=None):
        if os.path.isdir(data):
            then = int(time.time()*1000)
            plots = Plots(DBConnector, isInference=True, directory=data).DATA_dataframe
            now = int(time.time()*1000)
            if(len(plots)!=0):
                print("Retrieved "+str(len(plots))+" plots from directory in "+str(now-then)+" ms")
        elif os.path.isfile(data):
            plots = pd.DataFrame(columns=["img"])
            plots=plots.append({"img":data}, ignore_index=True)
        else:
            print("Data path is broken!")
        then = int(time.time()*1000)
        self.ANAset = None
        if(len(plots) != 0):
            self.ANAset = self.DoDataANA(DBConnector, plots, debug_mode,ForceModel_ID, hydraHeads=hydraHeads)
            print("ANAset: ", self.ANAset)
        now = int(time.time()*1000)

Parameters 
~~~~~~~~~~~~~~~~~~~~~

- ``DBConnector``: An object used to connect to the database
- ``data``:A string representing the path to plots for analysis.  
- ``debug_mode``: An optional boolean flag indicating whether or not the debug mode is enabled. 
- ``ModelRootPath``: An optional string representing the root path to the AI models in the database. Defaults to DB. 
- ``ChunkNumber``: An optional interger representing the number of chunks to process. Defaults to 0. 
- ``ForceModel_ID``: An optional integer representing the ID of the model to evaluate.
- ``forcedPlotType``: An optional string representing a specified plot type for analysis. Defaults to 'None'.                                                                              
- ``outfile``: An optional string representing the name of the report file. Defaults to an empty string. 
- ``hydraHeads``: An optional object containing additional model instances.


----------------------------------------------------------------------------

DoDataANA
-------------------

This method performs data analysis and predictions on the given data. 

.. code-block:: python
    
    # Extended code available on Github
    def DoDataANA(self, DBConnector, plots, debug_mode, ForceModel_ID=-1, outdir="", hydraHeads=None):


Parameters
~~~~~~~~~~~~~~~~~~~~

- ``DBConnector``: An object used to connect to the database
- ``plots``: An object that contains inofrmation about the plots to be analyzed. 
- ``debug_mode``: An optional boolean flag indicating whether or not the debug mode is enabled. 
- ``ForceModel_ID``: An optional integer representing the ID of the model to evaluate.
- ``outdir``: An optional string that specifies the output directory for the analysis results. 
- ``hydraHeads``: An optional object that contains additional model instances.

