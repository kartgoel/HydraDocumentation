hydra_keeper
===========

This file uses the EPICS library to evaluate whether to keep the plot and moves it to its respective output location. 
A File Handler handles all the log messages and exceptions while 'Hello Hydra' messages are sent after the socket binds with the constructed address.

KeeperAnnounce
-----------------

This method constantly announces the Keeper's activation in the system.

.. code-block:: python

    """ To Announce Keeper """

    def KeeperAnnounce(context,announcePort):
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

Parameters
~~~~~~~~~~

- ``context``: A ZMQ context representing the connections required for creating the sockets.
- ``announcePort``: An integer representing the port on which the keeper's announcement should be made.

----------------------------

getKeepPercent
--------------------

This method constructs and SQL query based on the parameters, executes the query, and processes the results of the query.

.. code-block:: python

    def getKeepPercent(DBConnector, fileName,fileType,isChunked):
        """ Returns Plot Id and fraction of data to keep """

        Percent_q="SELECT CollectPercent,ID FROM Plot_Types where Name=\""+fileName+"\" && FileType=\""+fileType+"\" && IsChunked is NULL"
        if(isChunked):
            Percent_q="SELECT CollectPercent,ID FROM Plot_Types where Name=\""+fileName+"\" && FileType=\""+fileType+"\" && IsChunked is not NULL"

        print(Percent_q)

        try:
            CollectPercent = DBConnector.FetchAll(Percent_q)
            #print(CollectPercent)
            #print(CollectPercent[0])
            if(len(CollectPercent)==1):
                return CollectPercent[0]["ID"],float(CollectPercent[0]["CollectPercent"])
            else:
                return CollectPercent[0]["ID"],-1.0
        except Exception as e:
            print(e)
            return -1,-1

Parameters
~~~~~~~~~~~~~~

- ``DBConnector``: An object representing the connector for the database that is responsible for executing queries
- ``fileName``: A string representing name of the file.
- ``fileType``: A string representing type of the file.
- ``isChunked``: A boolean representing whether the file is chunked or not.

---------------------------------------------------

ConfirmVerdict
---------------

This method retrieves the verdict and evaluates its confidence based upon the Confirmation Threshold.
The verdict and the confirmation status are returned.

.. code-block:: python

   def ConfirmVerdict(Model_config, AIReport, VerdictConfidence):
        """ To confirm the verdict from the model """
        verdict=AIReport.getVerdict()
        ConfirmationThreshold = Model_config['Thresholds'][verdict]
        if(VerdictConfidence>=ConfirmationThreshold):
            return "Confirmed", verdict
        else:
            return "Unconfirmed", verdict

Parameters
~~~~~~~~~~~~

- ``Model_config``: A dictionary representing the configuration of the model.
- ``AIReport``: An AIReport object representing the AI Report. 
- ``VerdictConfidence``: A float representing the confidence percentage of the verdict. 

--------------------------

AnalyzeReport
----------------

This method analyzes the AI Report and updates the database accordingly along with handlng EPICS functionality if relevant.

.. code-block:: python

    # Extended code available on Github
    def AnalyzeReport(DBConnector, Model_config, AIReport, outputlocation, RunPeriod, RunNumber_padding, RunNumber, reportMetaData, beam_current_name, beam_current_threshold, epics_root)

Parameters
~~~~~~~~~~~~~~

- ``DBConnector``: An object representing the connector for the database that executes queries.
- ``Model_config``: A dictionary containing the configuration for the model.
- ``AIReport``: An AIReport object representing the AI report.
- ``outputlocation``: A string representing the output location.
- ``RunPeriod``: A string representing the run period.
- ``RunNumber_padding``: An integer representing the padding for the run number.
- ``RunNumber``: An integer representing the run number.
- ``reportMetaData``: A dictionary representing the metadata of the AI report.
- ``beam_current_name``: A string representing the name of the beam current.
- ``beam_current_threshold``: A float representing the current beam threshold value.
- ``epics_root``: A string representing the root for the EPICS library.

-------------------------

SetStore
------------

This method uses the AI model to decide whether or not to keep the plot.

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

Parameters
~~~~~~~~~~~
- ``DBConnector``: An object representing the connector for the database that executes queries.
- ``Plot_Type_ID``: An integer representing the ID of the type of plot.
- ``chunkNum``: An integer representing the chunk number of the file.
- ``item``: A string representing the file item.
- ``percent``: A float representing the threshold percentage for the file being kept.
- ``RunNumber_padding``: An integer representing the padding for the run number.
- ``RunNumber``: An integer representing the run number.
- ``RunPeriod``: A dictionary representing the metadata of the AI report.
- ``outputlocation``: A string representing the name of the output location.
- ``test_mode``: A boolean representing whether the script is active.

--------------------------

GetKeeperConfig
--------------

This method returns the configuration for the keeper from the database in the form of a dictionary.

.. code-block:: python

    def GetKeeperConfig(DBConnector):
        """ To get the keeper config from the database """

        json_dict={}

        json_dict["Models"]={}
        models_q="SELECT Distinct Model_ID from ModelThresholds order by Model_ID asc;"
        models=DBConnector.FetchAll(models_q)
        for m in models:
            #print(m["Model_ID"])
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

Parameters
~~~~~~~~~~~
- ``DBConnector``: An object representing the connector for the database that executes queries.

-----------------------

moveFile
------------

This method is responsible for moving a given file from its input location to its output location.

.. code-block:: python

    def moveFile(outputlocation, RunPeriod,RunNumber_padding, RunNumber, item):
        """ To move file from input location to outputlocation """

        if(outputlocation!="NULL"):
            os.makedirs(outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/",exist_ok=True)
            print("Copying %s to %s" % (item['inDATA'],outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/"+item['inDATA'].split("/")[-1]))
            copyfile(item['inDATA'],outputlocation+str(RunNumber).zfill(RunNumber_padding)+"/"+item['inDATA'].split("/")[-1])
        else:
            print("I should copy this file but don't know where to copy it to....please supply outputlocation via -ol")

Parameters
~~~~~~~~~~~
- ``item``: A string representing the file item.
- ``RunNumber_padding``: An integer representing the padding for the run number.
- ``RunNumber``: An integer representing the run number.
- ``RunPeriod``: A dictionary representing the metadata of the AI report.
- ``outputlocation``: A string representing the name of the output location.







