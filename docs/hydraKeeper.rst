hydra_keeper
===========

This file uses the report from hydra_predict to evaluate whether to keep the plot and moves it to its respective output location. 

.. code-block:: python

   def main(argv):
    pidf= open("/tmp/keeperpid",'w')
    pidf.write(str(os.getpid()))
    pidf.close()

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    
    ap.add_argument("-i", "--input", required=False,
    help="Report from hydra to be processed")

    ap.add_argument("-c", "--config", required=False, default="keeper_config.cfg",
    help="config file defining thresholds etc")
    
    ap.add_argument("-tp", "--transmitport", required=False, default=5559,
    help="the port the keeper anounces will be transmitted on (default 5559)")
    
    ap.add_argument("-hh", "--hydrahost", required=False, default="localhost",
    help="the host of the hydra (default localhost)")

    ap.add_argument("-ol", "--outputlocation", required=False, default="NULL",
    help="the root directory keeper should put snagged files")

    ap.add_argument("-hp", "--hydraport", required=False, default=5556,
    help="the port of the reports from hydra will announce on (default 5556)")

    ap.add_argument("-t", "--test", required=False, action='store_true',
    help="turn on test mode which will not write to the DB")

    ap.add_argument("-cp", "--configpath", required=False, default="../Hydra.cfg",
    help="the path to the hydra params file (default set to '../Hydra.cfg'")

    args = vars(ap.parse_args())

    configPath=args["configpath"]
    try:
        print("configuring with parameters from ",configPath)
        with open(configPath) as parms_json:
            parms=json.load(parms_json)
    except Exception as e:
        print(e)
        pass

    RunNumber_padding=len(parms["TRAINING_PARAMS"]["RUN_NUMBER_FORM"])
    beam_current_name = parms["BEAM_CURRENT_NAME"]
    beam_current_threshold = parms["BEAM_CURRENT_THRESHOLD"]
    epics_root = parms["EPICS_ROOT"]
    test_mode = False
    if(args["test"]):
        test_mode=True

    outputlocation=args["outputlocation"]
    announcePort=args["transmitport"]
    hydraPort=args["hydraport"]
    hydraHost=args["hydrahost"]
    config_file=args["config"]
    configPath=args["configpath"]

    then = int(time.time()*1000)
    DBConnector = ConnectToDB.DBManager(configPath)
    now = int(time.time()*1000)
    logging.info("Keeper connected to DB in "+str(now-then)+" ms")

    config=GetKeeperConfig(DBConnector)

    print(config)

    context= zmq.Context()

    if(args["input"]):
        with open(args["input"]) as report_json:
            report=json.load(report_json)
        print(report)    
    else:
        spawns=[]
        p=Process(target=KeeperAnnounce, args=(context,announcePort))
        p.daemon = True
        spawns.append(p)
        spawns[0].start()

        
        port=hydraPort
        connection="tcp://"+hydraHost
        print("Listening to "+connection+" on port "+str(port))
        socket=context.socket(zmq.SUB)
        socket.setsockopt(zmq.SUBSCRIBE, b"")
        socket.connect(connection+":"+str(port))

        while True:
            message=str(socket.recv(),"utf8")
            message_parse=message.split(" ",1)
            if len(message_parse) > 0:
                logging.info("Message received from predict!")
            
            then = int(time.time()*1000)
            theReport=AIReport()
            theReport.Load(message_parse[1],"json")
            reportMetaData=theReport.getMetaData()
            now = int(time.time()*1000)
            logging.info("Report generated in "+str(now-then)+" ms")


            Header=message_parse[0]

            ifile=reportMetaData['inDATA'].split("/")[-1]
            print("-------------------------------------------------")
            print(Header)
            print(reportMetaData['inDATA']+"  "+theReport.getVerdict()+" @ "+str(theReport.getVerdictConfidence()))
            print( reportMetaData.keys())
            then = int(time.time()*1000)
            if('outDir' in reportMetaData.keys()):
                print("Output directory: ", reportMetaData['outDir'])
                if(reportMetaData['outDir']!="DELETE"):
                    os.rename(reportMetaData['inDATA'],reportMetaData['outDir']+"/"+ifile)
                    reportMetaData['inDATA']=reportMetaData['outDir']+"/"+ifile
                else:
                    os.makedirs("/tmp/keeper_tmpout",exist_ok=True)
                          
                try:
                    os.makedirs("/tmp/keeper_tmpout",exist_ok=True)
                    copyfile(reportMetaData['inDATA'], "/tmp/keeper_tmpout"+"/"+ifile)
                    try:
                        os.remove(reportMetaData['inDATA'])
                    except Exception as e:
                        print(e)
                        pass
                    print("I removed ", reportMetaData['inDATA'])
                    reportMetaData['inDATA']="/tmp/keeper_tmpout/"+"/"+ifile
                    if(reportMetaData['modelID'] != -1):
                        if(str(reportMetaData['modelID']) not in config["Models"]):
                            print("Model ID: "+str(reportMetaData['modelID'])+" not found in config file")
                            config=GetKeeperConfig(DBConnector)
                        Model_config=config["Models"][str(reportMetaData['modelID'])]
                    
                    ischunk=False
                    ifile=reportMetaData['inDATA'].rsplit("/",1)[1]
                    fileType=ifile.split(".")[1]
                    
                    chunkNum=str(ifile.split(".")[0].split("_")[-1])
                    print("chunk num?: "+chunkNum)
                    if(chunkNum.isnumeric()):
                        ischunk=True
                        rootfilename="_".join(ifile.split(".")[0].split("_")[:-1])
                    else:
                        ischunk=False
                        chunkNum=0
                        rootfilename=ifile.split(".")[0]

                    if("-" in rootfilename):
                        padNum=rootfilename.rsplit("-",1)[1]
                        if(padNum.isnumeric()):
                            rootfilename="-".join(rootfilename.split("-")[:-1])

                    now = int(time.time()*1000)
                    logging.info("Directory check and file moving in "+str(now-then)+" ms")

                    print("GETTING keep percent",rootfilename)
                    then = int(time.time()*1000)
                    Plot_Type_ID, CollectPercent = getKeepPercent(DBConnector, rootfilename,fileType,ischunk)
                    print("got keep percent",Plot_Type_ID, CollectPercent, "for",rootfilename)
                    now = int(time.time()*1000)
                    logging.info("getKeeperPercent took "+str(now-then)+" ms")

                    RunPeriod = reportMetaData["runPeriod"]
                    RunNumber = reportMetaData["runNumber"]
                    print("Run Period: ", RunPeriod, " Run Number: ", RunNumber)

                    then = int(time.time()*1000)
                    beam_current=-1.0
                    try:
                        with open(reportMetaData['inDATA'], 'rb') as f:
                            plot_img = base64.b64encode(f.read())

                        beam_current=-1.0
                        if(EPICS):
                            try:
                                current_beam_current=caget(beam_current_name)

                                if(current_beam_current):
                                    beam_current=current_beam_current

                            except Exception as e:
                                beam_current=-1.0
                                print("Error getting beam current: ",e)
                                pass

                        isConfirmed=1
                        if(reportMetaData["modelID"]>0):
                            if "Unconfirmed" in ConfirmVerdict(Model_config, theReport, theReport.getVerdictConfidence()):
                                isConfirmed=0
                        print("plot Time",reportMetaData["datetime"])
                        print("BEAM CURRENT IS: ",beam_current)
                        insert_q="INSERT into RunTime (HydraHostName,DateTime,BeamCurrent,RunNumber,PlotType_ID,PlotName,IMG,gradCAM,ModelID,VerdictLabel,VerdictConfidence,Confirmed, PlotTime) VALUES (\""+str(hydraHost)+"\",\""+str(datetime.now())+"\","+str(beam_current)+","+str(RunNumber)+","+str(Plot_Type_ID)+",\""+str(reportMetaData['inDATA'].rsplit("/",1)[1])+"\",\""+str(plot_img,"utf-8")+"\",\""+str(reportMetaData["gradCAM"])+"\","+str(reportMetaData["modelID"])+",\""+str(theReport.getVerdict())+"\","+str(theReport.getVerdictConfidence())+","+str(isConfirmed)+",\""+str(reportMetaData["datetime"])+"\")"
                        print("INSERT",str(reportMetaData['inDATA'].rsplit("/",1)[1]) ,"INTO RUNTIME")
                        DBConnector.Update(insert_q)

                    except Exception as e:
                        print("FAILED TO INSERT")
                        print(e)
                        pass

                    now = int(time.time()*1000)
                    logging.info("Keeper insert into RunTime in "+str(now-then)+" ms")

                    then = int(time.time()*1000)
                    SetStore(DBConnector, Plot_Type_ID, chunkNum, reportMetaData, CollectPercent, RunPeriod, RunNumber_padding, RunNumber, outputlocation, test_mode)
                    now = int(time.time()*1000)
                    logging.info("SetStore in "+str(now-then)+" ms")

                    then = int(time.time()*1000)
                    AnalyzeReport(DBConnector, Model_config, theReport, outputlocation, RunPeriod, RunNumber_padding, RunNumber, reportMetaData, beam_current_name, beam_current_threshold, epics_root)
                    now = int(time.time()*1000)
                    print("AnalyzeReport done in "+str(now-then)+" ms")
                    logging.info("AnalyzeReport done in "+str(now-then)+" ms")

                    if(reportMetaData['outDir']=="DELETE"):
                        print("Removing "+reportMetaData['inDATA'])
                        os.remove(reportMetaData['inDATA'])
                except Exception as e:
                    print(e)
                    pass
            else:
                continue
---------------------------------

KeeperAnnounce
~~~~~~~~~~~~~~~~~~~

This function configures bindings and signifies the start of the keeper. 

.. code-block:: python

   def KeeperAnnounce(context,announcePort):
    """ To Announce Keeper """
    
    print("KEEPER ANNOUNCE")
    zmqport=announcePort
    zmqconnection="tcp://*"
    transcontext = context
    transsocket = transcontext.socket(zmq.PUB)
    toBind=zmqconnection+":%s" % str(zmqport)
    print(toBind)
    try:
        transsocket.bind(toBind)
    except Exception as e:
        print(e)


    while True:
        transsocket.send_string("Hello Hydra")
        time.sleep(.5)
    
    return
--------------------

getKeepPercent
~~~~~~~~~~~~~~~~~~~~~

This function calculates the percent of data that is valid.

.. code-block:: python

   def getKeepPercent(DBConnector, fileName,fileType,isChunked):
    """ Returns Plot Id and fraction of data to keep """

    Percent_q="SELECT CollectPercent,ID FROM Plot_Types where Name=\""+fileName+"\" && FileType=\""+fileType+"\" && IsChunked is NULL"
    if(isChunked):
        Percent_q="SELECT CollectPercent,ID FROM Plot_Types where Name=\""+fileName+"\" && FileType=\""+fileType+"\" && IsChunked is not NULL"

    print(Percent_q)

    try:
        CollectPercent = DBConnector.FetchAll(Percent_q)
        if(len(CollectPercent)==1):
            return CollectPercent[0]["ID"],float(CollectPercent[0]["CollectPercent"])
        else:
            return CollectPercent[0]["ID"],-1.0
    except Exception as e:
        print(e)
        return -1,-1
---------------------------

ConfirmVerdict
~~~~~~~~~~~~~~~~~~~~~~~

This function retrieves a report on whether or not the validated data should be kept.

.. code-block:: python

   def ConfirmVerdict(Model_config, AIReport, VerdictConfidence):
    """ To confirm the verdict from the model """
    verdict=AIReport.getVerdict()
    ConfirmationThreshold = Model_config['Thresholds'][verdict]
    if(VerdictConfidence>=ConfirmationThreshold):
        return "Confirmed", verdict
    else:
        return "Unconfirmed", verdict
-------------

AnalyzeReport
~~~~~~~~~~~~~~~~~~

This function uses the confidence of the AI report and ensures an acceptable confirmed verdict.

.. code-block:: python

    def AnalyzeReport(DBConnector, Model_config, AIReport, outputlocation, RunPeriod, RunNumber_padding,RunNumber, reportMetaData, beam_current_name, beam_current_threshold, epics_root):

    print("Analyzing report")
    reportConfidences=AIReport.getConfidences()
    Confirmation, verdict =ConfirmVerdict(Model_config, AIReport, max(reportConfidences))
    print("EPICS:",EPICS)
    print("REPORT META DATA:",reportMetaData)
    if(reportMetaData['plotType_ID']!=-1):

        print("FORMING HISTORY INSERT")
        result_dict={}
        labels_array=AIReport.getModelLabels()
        conf_array=AIReport.getConfidences()
        for k in labels_array.keys():
            result_dict[labels_array[k]]=conf_array[k]
        print("RESULT DICT",result_dict)
        RunHistory_q="INSERT INTO RunHistory (RunNumber,DateTime,PlotType_ID,Output,ModelThresholds) VALUES ("+str(reportMetaData['runNumber'])+",\""+reportMetaData["datetime"]+"\","+str(reportMetaData['plotType_ID'])+",\""+str(result_dict)+"\",\""+str(Model_config['Thresholds'])+"\")"
        print("RUNHIST_Q:",RunHistory_q)
        DBConnector.Update(RunHistory_q)

    if(EPICS):
        model_labels = AIReport.getModelLabels()
        print(model_labels)
        print(reportConfidences)
        index =  list(model_labels.keys())[list(model_labels.values()).index('Good')] 
        index_bad =  list(model_labels.keys())[list(model_labels.values()).index('Bad')]
        print("indicies:",index,index_bad)
        print("entering try")
        try:
            print(float(reportConfidences[index]),"-",float(reportConfidences[index_bad]))
            epics_value = (float(reportConfidences[index])-float(reportConfidences[index_bad]))
        
            print("Epics value: ", epics_value)
       
            filename_string="_".join(reportMetaData['inDATA'].rsplit("/",1)[1].split(".")[0].split("_")[:-1])
            print(filename_string, epics_value)
            if("-" in filename_string):
                padNum=filename_string.rsplit("-",1)[1]
                if(padNum.isnumeric()):
                    filename_string="-".join(filename_string.split("-")[:-1]) 
                    
            caput(epics_root+filename_string,epics_value)
        except Exception as e:
            print(e)
            pass

    print("Confirmation?",Confirmation)
    if(Confirmation == "Unconfirmed"):
        print("GET SECOND OPINION")
        print("Message:",reportMetaData['inDATA'])
        Plot_Type_ID=reportMetaData['plotType_ID']
        ChunkNumber=reportMetaData['inDATA'].split("/")[-1].split(".")[0].split("_")[-1]
        IsConfirmed=0
        last_row_q="SELECT * FROM MonitoringLog WHERE Plot_Type_ID="+str(Plot_Type_ID)+" ORDER BY ID DESC LIMIT 1"
        last_row=DBConnector.FetchAll(last_row_q)
        IsTransition=0

        if(last_row["VerdictLabel"]!=verdict or IsConfirmed!=last_row["IsConfirmed"] or int(ChunkNumber)!=int(last_row["ChunkNumber"])+1):
            IsTransition=1
            last_row_trans=last_row["IsTransition"]
            if(last_row_trans==0):
                last_row_trans=2
            elif(last_row_trans==1):
                last_row_trans=3
            
            update_q="UPDATE MonitoringLog SET IsTransition="+str(last_row_trans)+"WHERE ID="+str(last_row["ID"])
            DBConnector.Update(update_q)


        insert_log_q="INSERT INTO MonitoringLog (DateTime,RunPeriod,RunNumber,ChunkNumber,Plot_Type_ID,PlotName,ModelID,VerdictLabel,VerdictConfidence,IsConfirmed,IsTransition) VALUES (\""+reportMetaData["datetime"]+"\",\""+RunPeriod+"\","+str(RunNumber)+","+str(ChunkNumber)+","+str(Plot_Type_ID)+",\""+reportMetaData['inDATA'].split("/")[-1]+"\","+str(reportMetaData['modelID'])+",\""+verdict+"\","+str(max(reportConfidences))+","+str(IsConfirmed)+","+str(IsTransition)+")"
        DBConnector.Update(insert_log_q)
        moveFile(outputlocation, RunPeriod, RunNumber_padding,RunNumber, reportMetaData)
        
    elif(Confirmation == "Confirmed"):
        print("Confirmed Verdict")
        ConfirmedVerdict = verdict
        fileName = reportMetaData['inDATA'].rsplit("/",1)[1].split(".")[0]
        if("Bad" in ConfirmedVerdict):
            beam_current=-1.0
            if(EPICS):
                try:
                    beam_current=caget(beam_current_name)
                except Exception as e:
                    print(e)
                    pass

            print("Beam current is (-1 for no epics)", beam_current)
            print("ALARM if not ignored: "+fileName)
            
            Plot_Type_ID=reportMetaData['plotType_ID']
            ChunkNumber=reportMetaData['inDATA'].split("/")[-1].split(".")[0].split("_")[-1]
            IsConfirmed=1
            #get last row with this plot type id
            last_row_q="SELECT * FROM MonitoringLog WHERE Plot_Type_ID="+str(Plot_Type_ID)+" ORDER BY ID DESC LIMIT 1"
            last_row=DBConnector.FetchAll(last_row_q)
            IsTransition=0

            if(last_row["VerdictLabel"]!=verdict or IsConfirmed!=last_row["IsConfirmed"] or int(ChunkNumber)!=int(last_row["ChunkNumber"])+1):
                IsTransition=1
                last_row_trans=last_row["IsTransition"]
                if(last_row_trans==0):
                    last_row_trans=2
                elif(last_row_trans==1):
                    last_row_trans=3
            
                update_q="UPDATE MonitoringLog SET IsTransition="+str(last_row_trans)+"WHERE ID="+str(last_row["ID"])
                DBConnector.Update(update_q)
            insert_log_q="INSERT INTO MonitoringLog (DateTime,RunPeriod,RunNumber,ChunkNumber,Plot_Type_ID,PlotName,ModelID,VerdictLabel,VerdictConfidence,IsConfirmed,IsTransition) VALUES (\""+reportMetaData["datetime"]+"\",\""+RunPeriod+"\","+str(RunNumber)+","+str(ChunkNumber)+","+str(Plot_Type_ID)+",\""+reportMetaData['inDATA'].split("/")[-1]+"\","+str(reportMetaData['modelID'])+",\""+verdict+"\","+str(max(reportConfidences))+","+str(IsConfirmed)+","+str(IsTransition)+")"
            
            if(beam_current >= beam_current_threshold or beam_current == -1.0):
                print("log query:",insert_log_q)
                DBConnector.Update(insert_log_q)
            moveFile(outputlocation, RunPeriod, RunNumber_padding,RunNumber, reportMetaData)
        elif("Good" in ConfirmedVerdict or "Acceptable" in ConfirmedVerdict):
            print("ALARM OFF")
        elif("NoData" in ConfirmedVerdict):
            print("ROOTSPY ISSUES?!")
----------------------

SetStore
~~~~~~~~~~~~~~~~

This function decides whether or not to keep a file to prevent repeats. 

.. code-block:: python

   def SetStore(DBConnector, Plot_Type_ID,chunkNum,item,percent,RunPeriod,RunNumber_padding,RunNumber,outputlocation,test_mode):
    """ To keep or remove the file """

    print("Checking", Plot_Type_ID,"against", float(percent))
    if(random.random()>=float(percent) or test_mode):
        return
    else:
        already_exists_q="SELECT * FROM Plots where Plot_Types_ID="+str(Plot_Type_ID)+" && RunPeriod=\""+RunPeriod+"\" && RunNumber="+str(RunNumber)+" && Chunk="+str(chunkNum)
        Existing_entry = DBConnector.FetchAll(already_exists_q)

        if(len(Existing_entry)==0):
            print("moving",item,"-------------->",outputlocation)
            moveFile(outputlocation, RunPeriod, RunNumber_padding,RunNumber, item)
        else:
            print("already exists")
-----------------------------

GetKeeperConfig
~~~~~~~~~~~~~~~~

This function retrieves configurations of keeper files from the database such as labels and thresholds. 

.. code-block:: python

   def GetKeeperConfig(DBConnector):
    """ To get the keeper config from the database """

    json_dict={}

    json_dict["Models"]={}
    models_q="SELECT Distinct Model_ID from ModelThresholds order by Model_ID asc;"
    models=DBConnector.FetchAll(models_q)
    for m in models:
        json_dict["Models"][str(m["Model_ID"])]={}
        main_q="SELECT Model_ID,labels,Classification,Threshold from ModelThresholds as mt inner join Plot_Classifications as pc on pc.ID=mt.Plot_Classification_ID inner join Models on Model_ID=Models.ID where Models.ID="+str(m["Model_ID"])+";"
        thresholds=DBConnector.FetchAll(main_q)
        Thresholds_dict={}

        if(len(thresholds)>0):
            original_dict_string=str(thresholds[0]["labels"],'utf-8')
            original_dict = eval(original_dict_string)
            labels = {v: k for k, v in original_dict.items()}
            for t in thresholds:
                Thresholds_dict[t["Classification"]]=t["Threshold"]

            json_dict["Models"][str(m["Model_ID"])]["Labels"]=labels
            json_dict["Models"][str(m["Model_ID"])]["Thresholds"]=Thresholds_dict
    
    return json_dict
--------------------

moveFile
~~~~~~~~~

This function copies the file from the input location to the output location.

.. code-block:: python

   def moveFile(outputlocation, RunPeriod,RunNumber_padding, RunNumber, item):

    if(outputlocation!="NULL"):
        os.makedirs(outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/",exist_ok=True)
        print("Copying %s to %s" % (item['inDATA'],outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/"+item['inDATA'].split("/")[-1]))
        copyfile(item['inDATA'],outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/"+item['inDATA'].split("/")[-1])
    else:
        print("I should copy this file but don't know where to copy it to....please supply outputlocation via -ol")
-----------------------



   
