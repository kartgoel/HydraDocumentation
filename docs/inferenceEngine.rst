inference_engine
=====================

This library establishes infrastructure for the data generator to reach inferences based upon the models and plots. 

.. code-block:: python

    class InferenceEngine:
 
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


    def DoDataANA(self, DBConnector, plots, debug_mode, ForceModel_ID=-1, outdir="", hydraHeads=None):
        ''' Predict and perform analysis on the Data

        PARAMETERS
        -------------------------------------
            debug_mode : Boolean, required
                If Debug mode is True, no DB insertion performed.

            outfile : str, required
                Name of report file.

            data_list : list of path to files, required
                path to images/Data to analyze.

            ForcedModel_ID : int, optional
                Model Id to evaluate, if -1, Model is identified based on data found 

            RunPeriod : str, optional

            RunNumber : int, optional

            watch : Boolean, optional

            outdir : str, optional

            crawling : boolean, optional (default = False)


        DEPENDENCIES
        -------------------------------------
            Global Variables - woke_HydraHeads, dbcursor
        
            Functions - LoadModel, WriteReport, DB_Record, SnagAndTag
        '''
        data_list = list(plots['img'])
        if len(data_list)==0:
            return None
        
        plots_dict = {}
        plotTypeName_list = []
        print("I'm looking at: ", data_list)
        for path in data_list:
            fileStr = str(path,"utf-8").rsplit("/",1)[1]
            fileStrParse = fileStr.rsplit(".",1)
            fileType = fileStrParse[1]
            nameParse = fileStrParse[0].split("_")
            isChunked = nameParse[-1].isnumeric()

            if isChunked:
                plotTypeName = "_".join(nameParse[:-1])
                plotTypeName_toUse = plotTypeName
            else:
                plotTypeName_toUse = fileStrParse[0]
            
            if("-" in plotTypeName_toUse):
                padNum=plotTypeName_toUse.rsplit("-",1)[1]
                if(padNum.isnumeric()):
                    plotTypeName_toUse="-".join(plotTypeName_toUse.split("-")[:-1])

            if isChunked:
                plotTypeName_toUse = plotTypeName_toUse+"_1"

            if plotTypeName_toUse not in plots_dict:
                plots_dict[plotTypeName_toUse] = [path]
                plotTypeName_list.append(plotTypeName_toUse)
            else:
                plots_dict[plotTypeName_toUse].append(path)
        output = []
        for plotTypeName_toUse in plotTypeName_list:
            to_pred=pd.DataFrame(columns=["datum"])
            for datum in plots_dict[plotTypeName_toUse]:
                if os.path.exists(datum):
                    to_pred=to_pred.append({"datum":str(datum,"utf-8")}, ignore_index=True)
                    break
                else:
                    continue
            
            if len(to_pred.index) == 0:
                continue

            if hydraHeads != None and plotTypeName_toUse in hydraHeads:
                modelInstance = hydraHeads[plotTypeName_toUse]
            else:
                modelInstance = Model(DBConnector, plotTypeName=plotTypeName_toUse,fileType=fileType,modelID=ForceModel_ID)
                if modelInstance.model == None:
                    print("Model could not be loaded for PlotType: ", plotTypeName_toUse)
                    print(hydraHeads)
                    output.append([-1, to_pred, b"{0: 'NoModel'}",[[1]]])
                    continue
            shape_tuple=ast.literal_eval(modelInstance.shape)
            
            imgheight=shape_tuple[0]
            imgwidth=shape_tuple[1]
            labels_of_model = modelInstance.labels
            color_mode="rgb"
            if(shape_tuple[2]==1):
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
                shuffle=False
            )

            
            if(test_generator.n==0):
                continue
                
            test_generator.reset()
            try:
                print("predicting on:",to_pred)
                preds=modelInstance.model.predict(test_generator,verbose=1,steps=test_generator.n)
                print("preds:",preds)
            except Exception as e:
                print(e)
                continue

            predicted_class_indices=np.argmax(preds,axis=1)
            
            output.append([modelInstance.ID, to_pred,labels_of_model,preds])
        
        return output
        
    def getResults(self):
        return self.output



