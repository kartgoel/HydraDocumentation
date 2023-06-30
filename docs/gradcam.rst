hydra_train
===============================

This file

.. code-block:: python

    def main(argv):
        """Main Function, takes below command line arguments...
        """
        ap = argparse.ArgumentParser()
        ap.add_argument("-D", "--data", required=True,
        help="Name of image to train a model for")
        ap.add_argument("-e", "--epochs", required=False,
        help="Maximum number of epochs")
        ap.add_argument("-d", "--debug", required=False, action="store_true",
        help="debug does not do inserts")
        ap.add_argument("-a", "--anneal", required=False, action="store_true",
        help="anneal the model")
        ap.add_argument("-lm", "--loadmodel", required=False,
        help="ID of model to load to train on")
        ap.add_argument("-M", "--merge", required=False,action="store_true",
        help="Take all Plot types with the same name regardless of chunked or not")
        ap.add_argument("-g", "--gpus", required=False,
        help="number of gpus to use")
        ap.add_argument("-c", "--config", required=True,
        help="path to config file")
        args = vars(ap.parse_args())

        config_file_path = args["config"]
        # ------------- Code Block to get CLI parameters ---------------
        data_to_use = args["data"]
        print("Using Data: ", data_to_use)


        EPOCHS = 1000 # num epochs
        if(args["epochs"] is not None):
            EPOCHS=int(args["epochs"])

        debug_mode = False
        debug_mode=args["debug"]
        print("Debug mode: ", debug_mode)

        anneal=False
        anneal=args["anneal"]
        AnnealEpochs=0
        
        mergeAll=False
        mergeAll=args["merge"]

        GPUS=1 
        if(args['gpus']):
            print("SETTING GPUS")
            GPUS=int(args['gpus'])
            print("GPUS set to: ", GPUS)
        # ------------ CLI parameters setting done -------------------------------

        # ------------ Setting other parameters -----------------------------
        EARLY_STOPPING_MIN_DELTA=.005 #UNUSED
        EARLY_STOPPING_PATIENCE=5*GPUS #DEFAULT VALUE
        BS=int(16*GPUS) #DEFAULT VALUE         
        DATACHOKE=-1 
        rootloc="../data_monitoring/" #DEFAULT VALUE
        TrainFraction=.95

        INIT_LR = 0.01 #.01*BS #0.05*BS # Learning rate
        ROOT_MODEL_OUT="../Hydra_models/" #DEFAULT VALUE
        SAMPLING_SCHEME="undersample"
        runnum_zfill=6
        try:
            with open(config_file_path) as parms_json:
                parms=json.load(parms_json)
                #print(parms.keys())

                #"INITIAL_LEARNING_RATE": 0.01,
                #"ROOT_MODEL_OUT": "/group/halld/Hydra_models/"
                EARLY_STOPPING_PATIENCE=int(parms["TRAINING_PARAMS"]["EARLY_STOPPING_PATIENCE_SCALE"])*GPUS
                BS=int(int(parms["TRAINING_PARAMS"]["BATCH_SIZE_SCALE"])*GPUS)
                DATACHOKE=parms["TRAINING_PARAMS"]["DATACHOKE"]
                rootloc=parms["TRAINING_PARAMS"]["IMG_ROOT_LOCATION"]
                TrainFraction=parms["TRAINING_PARAMS"]["TRAIN_FRACTION"]
                INIT_LR=parms["TRAINING_PARAMS"]["INITIAL_LEARNING_RATE"]
                ROOT_MODEL_OUT=parms["TRAINING_PARAMS"]["ROOT_MODEL_OUT"]
                runnum_zfill=len(parms["TRAINING_PARAMS"]["RUN_NUMBER_FORM"])
                SAMPLING_SCHEME=parms["TRAINING_PARAMS"]["SAMPLING_SCHEME"]

        except Exception as e:
            print(e)
            exit(1)


        # --------------- Parameters set -------------------------

        connector = DBManager(configPath=config_file_path)

        # --------------- Get Classes -----------------------------
        Plot_Type_ID=-1
        if( ("chunk" in data_to_use.lower() or "chunks" in data_to_use.lower()) and not mergeAll):
            name=data_to_use.replace("Chunks","").replace("chunks","").replace("chunk","").replace("Chunk","")
            Plot_Type_ID_q="SELECT ID FROM Plot_Types where IsChunked=1 && Name=\""+name+"\""
            # dbcursor.execute(Plot_Type_ID_q)
            Plot_Type_ID = connector.FetchAll(Plot_Type_ID_q)[0]["ID"]
        else:
            name=data_to_use.replace("Chunks","").replace("chunks","").replace("chunk","").replace("Chunk","")
            Plot_Type_ID_q="SELECT ID FROM Plot_Types where Name=\""+name+"\""
            # dbcursor.execute(Plot_Type_ID_q)
            Plot_Type_ID = connector.FetchAll(Plot_Type_ID_q)
        print("Query to get Plot_Type_ID: ", Plot_Type_ID_q)
        print("Working on Plot Type ID: ", Plot_Type_ID)
        if not mergeAll:
            plt_ID=-1
            if not str(Plot_Type_ID).isnumeric():
                plt_ID=Plot_Type_ID[0]['ID']
            else:
                plt_ID=Plot_Type_ID
            Classifications_q="SELECT Classification from Plot_Classifications where Classification != \"Ignore\" && ID in (SELECT Plot_Classifications_ID from Valid_Classifications WHERE Plot_Types_ID="+str(plt_ID)+") ORDER BY ID asc"
        else:
            print(Plot_Type_ID)
            Classifications_q="SELECT Classification from Plot_Classifications where Classification != \"Ignore\" && ID in (SELECT Plot_Classifications_ID from Valid_Classifications WHERE Plot_Types_ID="+str(Plot_Type_ID[0]['ID'])+" "
            if len(Plot_Type_ID) > 1:
                for i in range(1,len(Plot_Type_ID)):
                    Classifications_q+="|| Plot_Types_ID="+str(Plot_Type_ID[i]['ID'])
            Classifications_q+=") ORDER BY ID asc"
        print("Get Plot_Classification Query: ", Classifications_q)
        # dbcursor.execute(Classifications_q)
        Plot_Classifications = connector.FetchAll(Classifications_q)
        original_Plot_Classifications=Plot_Classifications
        print(len(Plot_Classifications))
        # ------------------------------------------------------------------

        # -------------- Get Data ----------------------------------

        All_data_q="SELECT Plots.ID,Plot_Types.Name, Plot_Types.FileType, Plots.ID,Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plot_Types.IsChunked, Plots.TrainingWeight, Plot_Classifications.Classification FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id inner join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.name = \'"+data_to_use+"\' && Plot_Classifications.Classification != \'Ignore\' and (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id) ORDER BY Plots.RunNumber asc"

        if("chunk" in data_to_use.lower() or "chunks" in data_to_use.lower()):
            name=data_to_use.replace("Chunks","").replace("chunks","").replace("chunk","").replace("Chunk","")
            All_data_q="SELECT Plot_Types.Name, Plot_Types.FileType, Plots.ID, Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plot_Types.IsChunked, Plots.TrainingWeight, Plot_Classifications.Classification FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id inner join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.IsChunked=1 && Plot_Types.name = \'"+name+"\' && Plot_Classifications.Classification != \'Ignore\' and (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id) ORDER BY Plots.RunNumber asc"

        print("Fetching all data with the Query: ", All_data_q)
        # dbcursor.execute(All_data_q)
        DATA = connector.FetchAll(All_data_q)
        print("Number of data samples: ", len(DATA))
        # -----------------------------------------------------------

        # --------------- Prepare Data -----------------------------------
        DATA_dataframe=pd.DataFrame(columns=["img","label"])
        for datum in DATA:
            if datum["RunNumber"] != 0:
                location=datum["RunPeriod"]+str(datum["RunNumber"]).zfill(runnum_zfill)+"/"+datum["Name"]
                if(datum["IsChunked"] == 1):
                    location=location+"_"+str(datum["Chunk"]).zfill(4)
                location=location+"."+datum["FileType"]
                if not os.path.isfile(location):
                    location=location.replace(rootloc,"/work/halld/online_monitoring/AI/keeper/") ## EVENTUALLY REPLACE THIS WITH CONFIG PARAM
            else:
                location=rootloc+"/simulated/"+datum["RunPeriod"]+"."+datum["FileType"]

            for i in range (0,datum["TrainingWeight"]):
                DATA_dataframe=DATA_dataframe.append({"img":location,"label":datum["Classification"],"imgID":datum["ID"]}, ignore_index=True)

        DATA_dataframe=shuffle(DATA_dataframe)
        if(DATACHOKE != -1):
            DATA_dataframe=DATA_dataframe.iloc[:int(DATACHOKE)]

        # Split into training and validation data
        training_dataframe, validation_dataframe = DataPreparation().train_test_split(DATA_dataframe,TrainFraction,BS,SAMPLING_SCHEME)

        training_IDs=training_dataframe["imgID"].tolist()

        #drop imgID from dataframes
        training_dataframe=training_dataframe.drop(columns=["imgID"])
        validation_dataframe=validation_dataframe.drop(columns=["imgID"])

        #noDataFlag = False
        clsnm = []
        print("Class |\t Train |\t Valid")
        for Class in Plot_Classifications:
            className=Class["Classification"]
            trainCount=training_dataframe.loc[training_dataframe.label == className].shape[0]
            validCount=validation_dataframe.loc[validation_dataframe.label == className].shape[0]
            row=className+"  |  "+str(trainCount)+" ("+str(float(trainCount)/float(training_dataframe.shape[0]))+")  |  "+str(validCount)+" ("+str(float(validCount)/validation_dataframe.shape[0])+")"
            print(row)
            if(trainCount+validCount >= 2):
                #noDataFlag = True
                clsnm.append(str(className))
                #Plot_Classifications = [x for x in Plot_Classifications if x["Classification"] != className]
                #removeLabelfromDataset(training_dataframe,className)
                #removeLabelfromDataset(validation_dataframe,className)
                #moveDataAllButOne(training_dataframe,validation_dataframe,className)
                if(trainCount == 0 and validCount != 0):
                validation_dataframe,training_dataframe= moveDataAllButOne(validation_dataframe,training_dataframe,className)
                elif(validCount == 0 and trainCount != 0):
                training_dataframe,validation_dataframe= moveDataOne(training_dataframe,validation_dataframe,className)
            else:
                print("WARNING:")
                print("not enough samples for class: ",className)
                print("removing class: ",className)
                Plot_Classifications = [x for x in Plot_Classifications if x["Classification"] != className]
                training_dataframe=removeLabelfromDataset(training_dataframe,className)
                validation_dataframe=removeLabelfromDataset(validation_dataframe,className)

        print("==========================================================")        
        print("Class |\t Train |\t Valid")
        for Class in original_Plot_Classifications:
            className=Class["Classification"]
            trainCount=training_dataframe.loc[training_dataframe.label == className].shape[0]
            validCount=validation_dataframe.loc[validation_dataframe.label == className].shape[0]
            row=className+"  |  "+str(trainCount)+" ("+str(float(trainCount)/float(training_dataframe.shape[0]))+")  |  "+str(validCount)+" ("+str(float(validCount)/validation_dataframe.shape[0])+")"
            print(row)

        # Normalize the pixel values
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

        #YOU NEED TO ADD THE RIGHT PAD NUMBER BACK IN. THIS IS A HACK TO GET IT TO WORK
        #loop over training_dataframe and replace img
        #for i in range(0,training_dataframe.shape[0]):
        #    img=training_dataframe.iloc[i]["img"]
        #    img=img.replace("selftiming","selftiming-02")
        #    training_dataframe.iloc[i]["img"]=img

        #loop over validation_dataframe and replace img
        #for i in range(0,validation_dataframe.shape[0]):
        #    img=validation_dataframe.iloc[i]["img"]
        #    img=img.replace("selftiming","selftiming-02")
        #    validation_dataframe.iloc[i]["img"]=img
        
        #print(training_dataframe.iloc[0]["img"])

        imgshape=cv2.imread(str(training_dataframe.iloc[0]["img"])).shape
        imgheight=imgshape[0] #128
        imgwidth=imgshape[1] #128

        print("Using images of size %sx%s" % (imgwidth,imgheight) )

        train_generator=train_datagen.flow_from_dataframe(
            dataframe=training_dataframe, 
            directory=None, 
            x_col="img", y_col="label", 
            class_mode="categorical", 
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=BS,
            shuffle=True,
            seed=42)

        validation_generator=valid_datagen.flow_from_dataframe( 
            dataframe=validation_dataframe, 
            directory=None, 
            x_col="img", y_col="label", 
            class_mode="categorical", 
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=1,
            shuffle=True,
            seed=42)


        strategy = tf.distribute.MirroredStrategy()
        
        #print("TF Version: ", TF_VERSION)
        if(TF_VERSION == "2.7.1"):
            atexit.register(strategy._extended._collective_ops._pool.close) # type: ignore
        else:
        #    atexit.register(strategy._extended._collective_ops._pool.close) # type: ignore
            pass

        print("Number of devices: {}".format(strategy.num_replicas_in_sync))
        
        # ------------------------------------------------------------------------------------
        # train_dataset = tf.data.Dataset.from_tensor_slices(train_generator)
        # validation_dataset = tf.data.Dataset.from_tensor_slices(validation_generator)
        # ------------------------------------------------------------------------------------

        #with strategy.scope():
        input_tensor = Input(shape=(imgheight,imgwidth,3))
        model = InceptionV3(include_top=True, weights=None, input_tensor=input_tensor, input_shape=None, pooling=None, classes=len(Plot_Classifications))

        # ---------------- Load model ---------------------------------------

        loaded_model_ID=-1
        model_to_load=""
        loaded_model_LR=INIT_LR
        if(args["loadmodel"]):
            print("LOADING MODEL: ", args["loadmodel"])
            Model_q="SELECT * FROM Models where ID="+str(args["loadmodel"])
            # dbcursor.execute(Model_q)
            Model_to_load_line=connector.FetchAll(Model_q)
            if(len(Model_to_load_line)!=1):
                print("Cannot find Model with ID "+str(args["loadmodel"])+". Training from scratch...")
            else:
                loaded_model_ID=int(args["loadmodel"])
                model_to_load=Model_to_load_line[0]["Location"]+Model_to_load_line[0]["Name"]
                inputShape_parse=Model_to_load_line[0]["InputShape"][+1:-1].split(",")
                loaded_model_LR=Model_to_load_line[0]["LearningRate"]
                imgheight=int(inputShape_parse[0].strip())
                imgwidth=int(inputShape_parse[1].strip())
                print("Loading model from: "+model_to_load)

        print("[INFO] training network...")
        if(loaded_model_ID!=-1):
            print(loaded_model_ID)
            print("Loaded LR: "+str(loaded_model_LR))
            INIT_LR=loaded_model_LR

        opt=None
        if(TF_VERSION=="2.7.1"):
            opt = SGD(lr=INIT_LR, decay=INIT_LR / EPOCHS)#, momentum=.2, nesterov=True)
        else:
            opt = SGD(learning_rate=INIT_LR, momentum=.2, nesterov=True)
        #opt = Adadelta()
        
        # -------------------- Set Mirrored Strategy if more than 1 GPUs are available -------------
        if GPUS<=1 :
            input_tensor = Input(shape=(imgheight,imgwidth,3))
            model = InceptionV3(include_top=True, weights=None, input_tensor=input_tensor, input_shape=None, pooling=None, classes=len(Plot_Classifications))
            if(loaded_model_ID != -1):
                print("Loading model from: "+model_to_load)
                model=load_model(model_to_load)
            parallel_model = model
            parallel_model.compile(loss="categorical_crossentropy", optimizer=opt,metrics=["accuracy"])
        else:
            if(loaded_model_ID != -1):
                print("Loading model from: "+model_to_load)
                with strategy.scope():
                    model=load_model(model_to_load)
                    parallel_model = model
                    parallel_model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
            else:
                with strategy.scope():
                    input_tensor = Input(shape=(imgheight,imgwidth,3))
                    model = InceptionV3(include_top=True, weights=None, input_tensor=input_tensor, input_shape=None, pooling=None, classes=len(Plot_Classifications))
                    parallel_model = model
                    parallel_model.compile(loss="categorical_crossentropy", optimizer=opt,metrics=["accuracy"])

        model_name=data_to_use+"-"+str(datetime.datetime.now().timestamp()).replace(".","_")+".h5"
        #callbacks
        logroot="./training_logs/"
        if(debug_mode==True):
            logroot="./debug_training_logs/"
        print("Location of logs: ", logroot)
        early_stopping_var='val_loss'
        tensorboard=TensorBoard(log_dir=logroot+'tensorboard_'+model_name, histogram_freq=0, write_graph=True,update_freq='epoch',write_images=True)
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor=early_stopping_var,min_delta=EARLY_STOPPING_MIN_DELTA ,patience=EARLY_STOPPING_PATIENCE,restore_best_weights=True,verbose=1)
        model_checkpoint= ModelCheckpoint("/home/tbritton/Hydra_temp/latest_epoch_"+model_name, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
        # ADJUST MODEL CHECKPOINT LOC
        STEP_SIZE_TRAIN=int(train_generator.n/train_generator.batch_size)
        STEP_SIZE_VALID=int(validation_generator.n/validation_generator.batch_size)
        print("Training Step Size: ", STEP_SIZE_TRAIN)
        print("FITTING")
        H=None
        fit_success=False

        try:
            #parallel_model.summary()
            print('Plot_Classifications: ',Plot_Classifications)
            print('len(Plot_Classifications): ',len(Plot_Classifications))
            H = parallel_model.fit(train_generator, steps_per_epoch=STEP_SIZE_TRAIN, validation_data=validation_generator, validation_steps=STEP_SIZE_VALID, epochs=EPOCHS,callbacks=[early_stopping])#,model_checkpoint])
            # H = parallel_model.fit(train_dataset, steps_per_epoch=STEP_SIZE_TRAIN, validation_data=validation_dataset, validation_steps=STEP_SIZE_VALID, epochs=EPOCHS,callbacks=[tensorboard,early_stopping])#,model_checkpoint])
            fit_success=True
        except Exception as e:
            print("fitting threw exception:",e)
            pass

        print("ANALYZING")

        model_value=min(H.history[early_stopping_var])
        Numepochs=H.history[early_stopping_var].index(model_value)+1

        labels = (validation_generator.class_indices)
        # print("Labels: ", labels)
        #results=pd.DataFrame(columns=["Filename","Predictions"])
        to_pred=pd.DataFrame(columns=["plot"])
        for f in validation_generator.filenames:
            to_pred=to_pred.append({"plot":f}, ignore_index=True)

        test_generator = test_datagen.flow_from_dataframe(
        dataframe=to_pred,
            directory=None,
            x_col="plot",
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=1,
            class_mode=None,
            shuffle=False
        )
        test_generator.reset()

        preds=parallel_model.predict_generator(test_generator,verbose=1,steps=test_generator.n)

        predicted_class_indices=np.argmax(preds,axis=1)
        #print(preds)
        labels = (train_generator.class_indices)
        labels = dict((v,k) for k,v in labels.items())
        predictions = [labels[k] for k in predicted_class_indices]


        print(labels)
        filenames=test_generator.filenames
        results=pd.DataFrame({"plot":filenames,
                            "Predictions":predictions})

        right=0.
        total=0.
        for index, row in results.iterrows():
            total=total+1
            label_val=validation_dataframe[validation_dataframe['img']==row["plot"]]
            if label_val.iloc[0]["label"] == row["Predictions"]:
                right=right+1

        print("Accuracy on test data: ", right/total)
        learning_rate=K.eval(parallel_model.optimizer.lr * 1. / (1. + parallel_model.optimizer.decay*tf.cast(parallel_model.optimizer.iterations,tf.float32)))

        # Extract the training loss and accuracy
        train_loss = H.history['loss']
        train_acc = H.history['accuracy']

        # Extract the validation loss and accuracy
        val_loss = H.history['val_loss']
        val_acc = H.history['val_accuracy']
        
        # Plot the training and validation loss
        plt.plot(train_loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.legend()
        plt.savefig('loss'+'_'+model_name+'.png', bbox_inches='tight')
        
        plt.clf()

        # Plot the training and validation accuracy
        plt.plot(train_acc, label='Training Acc')
        plt.plot(val_acc, label='Validation Acc')
        plt.legend()
        plt.savefig('accuracy'+'_'+model_name+'.png', bbox_inches='tight')
        plt.close()
        try:
            connector.Close()
        except:
            pass

        connector = DBManager(configPath=config_file_path) #refresh the connection in case it timed out
        if(debug_mode==False):
            parallel_model.save(ROOT_MODEL_OUT+"/"+model_name)

            plt_ID=-1
            if not str(Plot_Type_ID).isnumeric():
                plt_ID=Plot_Type_ID[0]['ID']
            else:
                plt_ID=Plot_Type_ID

            inserted_model_q="INSERT into Models (Date,EarlyStopValue,Location,Name,MergedTrain,SamplingMethod,TensorFlowVersion,PythonVersion,KerasVersion,PlotType_ID,Labels,Epochs,EarlyStopQuantity,InputShape,LearningRate,AnnealEpochs) VALUES (NOW(),"+str(model_value)+",\""+str(ROOT_MODEL_OUT)+"\", \""+str(model_name)+"\","+str(mergeAll)+",\""+str(SAMPLING_SCHEME)+"\",\""+str(TF_VERSION)+"\",\""+str(PYVERSION)+"\",\""+str(KERAS_VERSION)+"\","+str(plt_ID)+",\""+str(labels)+"\","+str(Numepochs)+",\""+str(early_stopping_var)+"\",\""+str(imgshape)+"\","+str(learning_rate)+","+str(AnnealEpochs)+")"
            if(args["loadmodel"]):
                inserted_model_q="INSERT into Models (Date,Parent_Model_ID,EarlyStopValue,Location,Name,MergedTrain,SamplingMethod,TensorFlowVersion,PythonVersion,KerasVersion,PlotType_ID,Labels,Epochs,Parent_Model_ID,EarlyStopQuantity,InputShape,LearningRate,AnnealEpochs) VALUES(NOW(),"+str(loaded_model_ID)+","+str(model_value)+",\""+str(ROOT_MODEL_OUT)+"\", \""+str(model_name)+"\","+str(mergeAll)+",\""+str(SAMPLING_SCHEME)+"\",\""+str(TF_VERSION)+"\",\""+str(PYVERSION)+"\",\""+str(KERAS_VERSION)+"\","+str(Plot_Type_ID)+",\""+str(labels)+"\","+str(Numepochs)+",\""+str(early_stopping_var)+"\",\""+str(imgshape)+"\","+str(learning_rate)+","+str(AnnealEpochs)+")"
            
            print("Model insert Query: ", inserted_model_q)

            connector.Update(inserted_model_q)

            #GET ID FROM NAME RECORD TRAINING SET
            Model_ID_q="SELECT * FROM Models where Name=\""+str(model_name)+"\" && Location=\""+str(ROOT_MODEL_OUT)+"\""
            
            print("\n\n"+Model_ID_q)
            # dbcursor.execute(Model_ID_q)
            Model=connector.FetchAll(Model_ID_q)
            print("Returned Model: ",Model)
            if(len(Model)!=1):
                print("Model Lost. Returning")
                return
            else:
                #insert training Set
                Model_ID=Model[0]['ID']

                for id in training_IDs:
                    insert_training_q="INSERT into Training_Sets (Models_ID,Plots_ID) VALUES ("+str(Model_ID)+","+str(id)+")"
                    connector.Update(insert_training_q)

            for k in labels.keys():
                label_name=labels[k]
                #get the ID of the label
                ID_q="SELECT ID from Plot_Classifications where Classification=\""+str(label_name)+"\""
                class_ID=connector.FetchAll(ID_q)

                if(len(class_ID) != 1):
                    print("Error: Label not found")
                    return
                else:
                    class_ID=class_ID[0]['ID']
                    insert_label_thresholds_q="INSERT into ModelThresholds (Model_ID,Plot_Classification_ID,Threshold) VALUES ("+str(Model_ID)+","+str(class_ID)+",0)"
                    connector.Update(insert_label_thresholds_q)


        else:
            # print(K.eval(parallel_model.optimizer.lr * 1. / (1. + parallel_model.optimizer.decay*tf.cast(parallel_model.optimizer.iterations,tf.float32))))
            # print("Saving to local")
            # parallel_model.save("/home/tbritton/Hydra_temp/"+model_name)
            # label_file=open("/home/tbritton/Hydra_temp/"+model_name+"_LABELS","w+")
            # label_file.write(str(labels))
            parallel_model.save(ROOT_MODEL_OUT+"/"+model_name)
            plt_ID=-1
            if not str(Plot_Type_ID).isnumeric():
                plt_ID=Plot_Type_ID[0]['ID']
            else:
                plt_ID=Plot_Type_ID
            inserted_model_q="INSERT into Models (Date,EarlyStopValue,Location,Name,MergedTrain,SamplingMethod,TensorFlowVersion,PythonVersion,KerasVersion,PlotType_ID,Labels,Epochs,EarlyStopQuantity,InputShape,LearningRate,AnnealEpochs) VALUES (NOW(),"+str(model_value)+",\""+str(ROOT_MODEL_OUT)+"\", \""+str(model_name)+"\","+str(mergeAll)+",\""+str(SAMPLING_SCHEME)+"\",\""+str(TF_VERSION)+"\",\""+str(PYVERSION)+"\",\""+str(KERAS_VERSION)+"\","+str(plt_ID)+",\""+str(labels)+"\","+str(Numepochs)+",\""+str(early_stopping_var)+"\",\""+str(imgshape)+"\","+str(learning_rate)+","+str(AnnealEpochs)+")"
            if(args["loadmodel"]):
                inserted_model_q="INSERT into Models (Date,Parent_Model_ID,EarlyStopValue,Location,Name,MergedTrain,SamplingMethod,TensorFlowVersion,PythonVersion,KerasVersion,PlotType_ID,Labels,Epochs,Parent_Model_ID,EarlyStopQuantity,InputShape,LearningRate,AnnealEpochs) VALUES(NOW(),"+str(loaded_model_ID)+","+str(model_value)+",\""+str(ROOT_MODEL_OUT)+"\", \""+str(model_name)+"\","+str(mergeAll)+",\""+str(SAMPLING_SCHEME)+"\",\""+str(TF_VERSION)+"\",\""+str(PYVERSION)+"\",\""+str(KERAS_VERSION)+"\","+str(Plot_Type_ID)+",\""+str(labels)+"\","+str(Numepochs)+",\""+str(early_stopping_var)+"\",\""+str(imgshape)+"\","+str(learning_rate)+","+str(AnnealEpochs)+")"
            
            print("Model insert Query: ", inserted_model_q)
            print("Successfully completed Debug run, not saving anything.")

        print("Training Complete")
        print("closing connection")

----------------------------------

removeLabelfromDataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def removeLabelfromDataset(dataset, label):
        #dataset = dataset[dataset['label'] != label]
        #iterate through pandas dataframe row and remove rows with label
        for index, row in dataset.iterrows():
            if row['label'] == label:
                dataset.drop(index, inplace=True)
        return dataset

------------------------------------

moveDataAllButOne
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def moveDataAllButOne(from_dataset,to_dataset,label):
    
    foundFirst = False
    for index, row in from_dataset.iterrows():
        if row['label'] == label and not foundFirst:
            foundFirst == True
        elif row['label'] == label and foundFirst:
            to_dataset=to_dataset.append(row, ignore_index=True)
            from_dataset.drop(index, inplace=True)
    return from_dataset,to_dataset


------------------------------------

moveDataOne
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def moveDataOne(from_dataset,to_dataset,label):
    foundFirst = False
    for index, row in from_dataset.iterrows():
        if row['label'] == label and not foundFirst:
            foundFirst == True
            to_dataset=to_dataset.append(row, ignore_index=True)
            from_dataset.drop(index, inplace=True)
            break
    return from_dataset,to_dataset

------------------------------------
