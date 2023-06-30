Hydra Predict
=======================================

This file...

.. code-block:: python

    def main(argv):
    """

    """
    printVersions()

    pidf = open("/tmp/hydrapid",'w')
    pidf.write(str(os.getpid()))
    pidf.close()

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-D", "--data", required=True,
    help="Path of image or directory containing the images to be analyzed")
    ap.add_argument("-d", "--debug", required=False,action="store_true",
    help="the mode of operation.  Either production or debug")
    # ----------------------------------------------------------------
    ap.add_argument("-r", "--runnumber", required=False,
    help="the run number of the datum")
    ap.add_argument("-R", "--runperiod", required=False,
    help="the run period of the datum")
    # ----------------------------------------------------------------
    ap.add_argument("-mp", "--modelrootpath", required=False, default="DB",
    help="the root path to the directory containing the models")
    ap.add_argument("-o", "--outfile", required=False, default="",
    help="the outputfile the report file will be written/appended to")
    ap.add_argument("-od", "--outputdirectory", required=False, default="",
    help="the outputdirectory the images will be moved to in watch mode")
    ap.add_argument("-cp", "--configpath", required=False, default="../Hydra.cfg",
    help="the path to the hydra params file (default set to '../Hydra.cfg'")

    ap.add_argument("-fm", "--forcedmodelid", required=False, default=-1,
    help="the id of the model you are forcing to be used (default set to '-1' (auto)")

    args = vars(ap.parse_args())

    debug_mode = args["debug"]
    if(not debug_mode):
        pidf = open("/tmp/hydrapid",'w')
        pidf.write(str(os.getpid()))
        pidf.close()

    configPath = str(args['configpath'])
    try:
        with open(configPath) as parms_json:
            parms=json.load(parms_json)

        transmitPort=parms["COMMUNICATIONS"]["ReportTransmission_Port"]
        keeperHost=parms["COMMUNICATIONS"]["ReportReceiver_Host"]
        keeperPort=parms["COMMUNICATIONS"]["Announce_Port"]

        breakfast_path=parms["DATA_LOCATION"]["Breakfast"]

    except Exception as e:
        print(e)
        exit(1)
    hydraHeads = {}

    DBConnector = connector.DBManager(configPath)

    ModelRootPath = args["modelrootpath"]
    socket.bind("tcp://*:%s" % transmitPort)

    # Need to decide --->  Parse from filename!
    #if(args["runperiod"]):
    #    RunPeriod.value=args["runperiod"].encode('utf-8')
    #RunNumber.value=-1
    #if(args["runnumber"]):
    #    RunNumber.value=int(args["runnumber"])

    inputDirectory = args["data"]
    outfile=args["outfile"]

    if args["outputdirectory"]=="":
        print("ERROR: You have requested Hydra watch a directory but have not given an output directory.  Please supply an output directory (-od) ")
        return 1
    elif args["outputdirectory"].upper()=="DELETE":
        outdir="DELETE"
    else:
        outdir=args["outputdirectory"]
        if outdir[-1] != "/":
            outdir=outdir+"/"
        try:
            os.makedirs(outdir)
        except FileExistsError:
            pass
   
    OutDir.value=outdir.encode('utf-8')

    parmDict={}
    parmDict['Input']=args['data']
    parmDict['OutDir']=str(OutDir.value,'utf-8')\

    with open('.hydra_parms.cfg', 'w') as parmsconf:
        json.dump(parmDict,parmsconf)
        parmsconf.close()
   
    spawns=[]
    p=Process(target=CheckForKeeper,args=(hasKeeper, keeperHost, keeperPort))
    p.daemon = True
    spawns.append(p)
    spawns[0].start()
        
    hydraHeads = PreloadModels(DBConnector, ModelRootPath)
    print("Model preloading finished...")
    print(hydraHeads)
   
    for head in hydraHeads.keys():
        print("feeding",head)
        Breakfast(hydraHeads, head, breakfast_path)
   
   print("done feeding hydra")
    file_check=args["data"].split("/")[-1]
    if file_check != "":
        args["data"] += "/"
    
    if(os.path.isdir(args["data"])):
        InDir.value=args["data"].encode('utf-8')
        while True:
            try:
                with open('.hydra_parms.cfg', 'r') as hydraParams:
                    parms=json.load(hydraParams)
                    if 'OutDir' in parms.keys():
                        OutDir.value=parms['OutDir'].encode('utf-8')
                    if 'Input' in parms.keys():
                        InDir.value=parms['Input'].encode('utf-8')
            except Exception as e:
                print(e)
                with open('.hydra_parms.cfg', 'w') as hydraParams:
                    parms={}
                    parms['OutDir']=str(OutDir.value,'utf-8')
                    parms['Input']=str(InDir.value,'utf-8')
                    json.dump(parms,hydraParams)
                    hydraParams.close()
                pass
            try:
                os.makedirs(str(OutDir.value,'utf-8').strip())
            except FileExistsError:
                pass
            now = int(time.time()*1000)

            if(not os.path.exists(str(InDir.value,'utf-8'))):
                # logging.warning("Input directory not found.  Sleeping 5s...")
                print("Input directory not found.  Sleeping 5s...")
                time.sleep(5)
            else:
                #print("TO INF", InDir.value)
                # print("TO INF", InDir.value)
                then = int(time.time()*1000)
                #print current datetime
                #print(datetime.now())
                #print("Running inference engine on "+str(InDir.value,'utf-8'))
                try:
                    inferences = InferenceEngine(DBConnector, InDir.value, hydraHeads=hydraHeads, ForceModel_ID=args["forcedmodelid"]).ANAset
                except Exception as e:
                    print(e)
                    continue
                now = int(time.time()*1000)
                t_totalInferences = now - then 
                if inferences == None:
                    # logging.info("Total inference time for No images is: "+str(t_totalInferences)+" ms")
                    #print("Inferences are None!")
                    continue
                    
                print("Entering report sending loop...")
                total_images = 0
                
                print("Inferences: ", inferences)
                for result in inferences:
                    print("Result: ", result)
                    model_ID = result[0]
                    plotType_ID=-1
                   
                    if model_ID>0:
                        plotType_ID_q="SELECT PlotType_ID FROM Models WHERE ID="+str(model_ID)
                        print("PlotType_ID_q: ", plotType_ID_q)
                        plotType_ID_result=DBConnector.FetchAll(plotType_ID_q)
                        print("PlotType_ID_result: ", plotType_ID_result)
                        try:
                            plotType_ID=plotType_ID_result[0]['PlotType_ID']
                            headname_q="SELECT Name,IsChunked from Plot_Types where ID="+str(plotType_ID)
                            headname_result=DBConnector.FetchAll(headname_q)
                            headname=headname_result[0]['Name']
                            if(headname_result[0]['IsChunked']==1):
                                headname+="_1"
                            
                            modelused=hydraHeads[headname].model

                            
                        except Exception as e:
                            print(e)
                            pass

                    labels_of_model = result[2] 
                    to_pred = list(result[1]['datum'])
                    print(to_pred)
                    for i in range(len(to_pred)):
                        total_images += 1
                        preds = result[3][i]
                        if(USING_GRADCAM):
                            try:
                                gradCAM=GradCAM(modelused,layer_name='mixed10')
                                gradCAMheatmap,gradpreds,top_pred_index=gradCAM.get_heatmap(to_pred[i])
                            except Exception as e:
                                print(e)
                                gradCAMheatmap=None
                                pass

                        WriteReport(plotType_ID,model_ID,to_pred[i],preds,labels_of_model,outfile,OutDir.value,gradCAMheatmap,debug_mode)
    else:
        # logging.error("Provided input path is not a directory. Please provide a directory path.")
        print("Provided input path",args["data"]," is not a directory. Please provide a directory path.")

-----------------------------------------------------------

WriteReport
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function...

.. code-block:: python 

    def WriteReport(plotType_ID,model_ID,to_pred,preds,labels_of_model,outfile,outdir,gradCAMheatmap,debug_mode=False):
   
    print("Writing Report!")
    report = AIReport("classification")
    # parse filePath i.e. to_pred to get RunNumber and RunPeriod
    fileName = to_pred.split('/')[-1]
    parseIn=to_pred.split("/")

    runNumber=-1
    runPeriod="NA"

    for bit in parseIn:
        if ("Run" in bit and not "RunPeriod" in bit) or bit.isnumeric():
            runNumber=int(bit.replace("Run",""))
        if "RunPeriod" in bit:
            runPeriod=bit


    try:
        create_time = datetime.fromtimestamp(os.path.getctime(to_pred))
    except Exception as e:
        print(e)
        create_time = datetime.now()
        pass
    
    print("hasKeeperValue: ", hasKeeper.value)
    if hasKeeper.value != 1 and str(outdir, "utf-8").lower() == "delete":
        print("keeper not found deleting file: ", to_pred)
        os.remove(to_pred)
    
    
   metaData={"plotType_ID":plotType_ID,"modelID":model_ID, "inDATA":to_pred, "runNumber":runNumber, "runPeriod":runPeriod, "outDir":str(outdir,"utf-8"), "datetime":str(create_time) }
    if(gradCAMheatmap is not None):
        heatmap_bytes = np.uint8(255 * gradCAMheatmap).tobytes()
        _, imgbuffer = cv2.imencode('.png', heatmap_bytes)
    
        encoded_gradcam=base64.b64encode(imgbuffer)
        metaData["gradCAMheatmap"]=str(encoded_gradcam,"utf-8")
    else:
        metaData["gradCAMheatmap"]=""
    report.setMetaData(metaData)
    preds = [float(x) for x in preds]
    report.Result(preds, ast.literal_eval(str(labels_of_model,"utf-8")))
    jsonReport = report.Write("json")

    if(not debug_mode):
        print("Sending Msg: ")
        socket.send_string("HydraReport"+' '+jsonReport)

--------------------------------------

Breakfast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function...

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

--------------------------------------

CheckForKeeper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function...

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

--------------------------------------

PreloadModels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function...

.. code-block:: python 
    
    def PreloadModels(DBConnector, ModelRootPath):
        print("Model preloading started...")
        hydraHeads = {}
        then=int(time.time()*1000.0)
        data_to_analyze_q="SELECT * FROM Plot_Types where Active_Model_ID IS NOT NULL;"
        data_to_analyze = DBConnector.FetchAll(data_to_analyze_q)
        for d in data_to_analyze:
            headkey=str(d["Name"])
            if(d["IsChunked"] == 1):
                headkey += "_1"
            modelInstance = Model(DBConnector, modelID=d["Active_Model_ID"], modelRootPath=ModelRootPath)
            if modelInstance.model == None:
                print("Model could not be loaded with ID ", d["Active_Model_ID"])
            else:
                hydraHeads[headkey] = modelInstance
        return hydraHeads