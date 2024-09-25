hydra_predict
====================================================

This file generates a report using the GradCAM and AI model. 
It preloads the AI models from the database and performs a prediction and evaluation of the input plots.
The results of the AI model predictions are reported and stored in the appropriate location for the 'Keeper'.


WriteReport
--------------

This method writes the prediction report based on the model's predictions. 

.. code-block:: python

    #Extended code available on Github
    def WriteReport(plotType_ID,model_ID,to_pred,preds,labels_of_model,outfile,outdir,debug_mode=False):


Parameters
~~~~~~~~~~~~~

- ``plotType_ID``:An integer representing the plot ID in the database. 
- ``model_ID``: An integer representing the AI model ID in the database. 
- ``to_pred``: A string representing the path of the image to be predicted. 
- ``preds``: A list of floats representing the predicted labels for the plots. 
- ``labels_of_model``: A string representing the labels associated with the AI model. 
- ``outfile``: A string representing the output file path where the report will be written. 
- ``outdir``: A string representing the output directory where the plot will be moved. 
- ``debug_mode``: An optional boolean that will run the script in debug mode when 'True'. Default is 'False'.


Example Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    WriteReport(plotType_ID,model_ID,to_pred[i],preds,labels_of_model,outfile,OutDir.value,gradCAMheatmap,debug_mode)


--------------------------------------------

Breakfast 
---------------

This method performs a prediction using a specified AI model and dataset. 

.. code-block:: python 

    def Breakfast(hydraHeads, headkey, breakfast_path):
        try:
            to_pred=pd.DataFrame(columns=["datum"])
            to_pred=to_pred.append({"datum":breakfast_path}, ignore_index=True)

            inputShape_parse=hydraHeads[headkey].shape[+1:-1].split(",")
            imgheight=int(inputShape_parse[0].strip())
            imgwidth=int(inputShape_parse[1].strip())
            color_mode="rgb"
            if(int(inputShape_parse[2].strip())==1):
                color_mode="grayscale"

            test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
            test_generator = test_datagen.flow_from_dataframe(
                    dataframe=to_pred,
                    directory=None,
                    x_col="datum",
                    target_size=(imgheight,imgwidth),
                    color_mode=color_mode,
                    batch_size=1,
                    class_mode=None,
                    shuffle=False)
            test_generator.reset()
            preds=hydraHeads[headkey].model.predict(test_generator,verbose=1,steps=test_generator.n)
        except:
            print("Error in Breakfast")
            pass


Parameters
~~~~~~~~~~~~~~~~~~~~

- ``hydraHeads``: A dictionary containing the AI model instances. 
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
        recvport=int(keeperPort)
        recvconnection="tcp://"+keeperHost
        recvcontext= zmq.Context()
        print("Listening to "+recvconnection+" on port "+str(recvport))
        recvsocket=recvcontext.socket(zmq.SUB)
        recvsocket.setsockopt(zmq.SUBSCRIBE, b"")
        recvsocket.connect(recvconnection+":"+str(recvport))
        while True:
            message=str(recvsocket.recv(),"utf8")
            hasKeeper.value=1
        

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
        print("Model preloading started...")
        hydraHeads = {}
        then=int(time.time()*1000.0)
        # logging.info("Preloading Models")
        # logging.info("Preloading Models...")
        data_to_analyze_q="SELECT * FROM Plot_Types where Active_Model_ID IS NOT NULL;"
        data_to_analyze = DBConnector.FetchAll(data_to_analyze_q)
        for d in data_to_analyze:
            headkey=str(d["Name"])
            if(d["IsChunked"] == 1):
                headkey += "_1"
            # logging.info("Loading head for "+str(headkey))
            modelInstance = Model(DBConnector, modelID=d["Active_Model_ID"], modelRootPath=ModelRootPath)
            if modelInstance.model == None:
                # logging.error("Model could not be loaded with ID ", d["Active_Model_ID"])
                print("Model could not be loaded with ID ", d["Active_Model_ID"])
            else:
                hydraHeads[headkey] = modelInstance
        return hydraHeads


Parameters 
~~~~~~~~~~~~~~~

- ``DBConnector``: An object representing the connector for the database that is responsible for executing queries
- ``ModelRootPath``: A string representing the root path to the directory containing the AI models. 

Example Usage   
~~~~~~~~~~~~~

.. code-block:: python 

    hydraHeads = PreloadModels(DBConnector, ModelRootPath)


