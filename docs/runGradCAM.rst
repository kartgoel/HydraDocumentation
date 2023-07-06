run_gradCAM
=====================

This file uses a parser to generate a GradCAM to analyze and process present images.
Processed data is reported back to the database through a run time while logged messages are recorded.

.. code-block:: python 

    def main(argv):
    
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--config", required=True, help="path to config file")
        ap.add_argument("-i", "--input", required=True, help="full path to input image")
        ap.add_argument("-M", "--model", required=False, help="id of model",default=-1)

        args = vars(ap.parse_args())

        configPath = args["config"]
        modelID=int(args["model"])
        DBConnector = connector.DBManager(configPath)

        image_pth=args["input"]
        runnum=int(image_pth.split("/")[-2].replace("Run",""))

        print("modelID",modelID)
        if modelID==-1 :
            print("True")
            grad=GradCAM(None,-1)
            grad.insert_into_runtime(args["input"],-1,-1,runnum)
        else:

            model_q="SELECT Location,Name,PlotType_ID FROM Models WHERE ID="+str(modelID)
        
            model_r=DBConnector.FetchAll(model_q)[0]

            modelInstance = Model(DBConnector, modelID=modelID, modelRootPath=model_r["Location"])
            model_used=modelInstance.model
            grad=GradCAM(model_used,"mixed10")


            grad.insert_into_runtime(args["input"],model_r["PlotType_ID"],args["model"],runnum)

