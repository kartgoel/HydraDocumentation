start_hydra
=====================

This file loads the Hydra installer environment to boot Hydra, Feeder, and Keeper.

.. code-block:: python 

    def main(argv):

        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()

        ap.add_argument("-R", "--runperiod", required=False,
        help="the run period of the datum")
        ap.add_argument("-r", "--runnumber", required=False,
        help="the run number of the datum")
        ap.add_argument("-mp", "--modelrootpath", required=False,
        help="model root path of the directory containing the models to load")
        ap.add_argument("-e", "--end", required=False,action="store_true",
        help="DAQ end")
        ap.add_argument("-k", "--kill", required=False,action="store_true",
        help="kill all")
        ap.add_argument("-ol", "--outputlocation", required=False,
        help="path to root directory where the keeper will copy files")

        ap.add_argument("-i", "--inputlocation", required=False,
        help="path to initial input directory")
        
        ap.add_argument("-jd", "--jointdir", required=False,help="path to the feeder/hydra joint directory")
        
        ap.add_argument("-c", "--config", required=True,
        help="Full path to Hydra config file")

        ap.add_argument("-t", "--test", required=False, action='store_true',
        help="turn on test mode which will not write to the DB")

        args = vars(ap.parse_args())

        location="/group/halld/hydra/"
        if(os.getenv('HYDRA_INSTALL')):
            location=os.getenv('HYDRA_INSTALL')

        if("scripts" in location):
            location.replace("scripts","")

        feeder_hydra_jointDir=""
        inputLoc=""

        test_mode = False
        if(args["test"]):
            test_mode=True

        RunPeriod=""

        if(os.getenv('RUN_PERIOD')):
            RunPeriod=os.getenv('RUN_PERIOD')
        
        if(args["inputlocation"]):
            inputLoc=args["inputlocation"]

        if(args["jointdir"]):
            feeder_hydra_jointDir=args["jointdir"]

        if(args["runperiod"]):
            RunPeriod=args["runperiod"]
        
        if(RunPeriod==""):
            print("ERROR: no run period found or given use -R or set $RUN_PERIOD")
            exit(1)

        RunNumber=args["runnumber"]

        hydrapidFile="/tmp/hydrapid"
        keeperpidFile="/tmp/keeperpid"
        feederpidFile="/tmp/feederpid"

        HydraRunning=False
        keeperRunning=False
        feederRunning=False

        ModelRootPath="DB"
        if(args["modelrootpath"]):
            ModelRootPath=args["modelrootpath"]

        outputlocation="./"
        if(args["outputlocation"]):
            outputlocation=args["outputlocation"]

        hpid=-1
        kpid=-1
        fpid=-1
        
        if(os.path.exists(hydrapidFile)):
            try:
                hpidf=open(hydrapidFile,"r")
                hpid=hpidf.readline().strip()
                print(hpid)

                hpidf.close()
                os.kill(int(hpid),0)
            except OSError:
                pass
            else:
                HydraRunning=True
        

        if(os.path.exists(keeperpidFile)):
            try:
                kpidf=open(keeperpidFile,"r")
                kpid=kpidf.readline().strip()
                print(kpid)

                kpidf.close()
                os.kill(int(kpid),0)
            except OSError:
                #print(ose)
                pass
            else:
                keeperRunning=True

        if(os.path.exists(feederpidFile)):
            try:
                fpidf=open(feederpidFile,"r")
                fpid=fpidf.readline().strip()
                print(fpid)

                fpidf.close()
                os.kill(int(fpid),0)
            except OSError:
                pass
            else:
                feederRunning=True
        
        if(not args["kill"]):
            if(not args["runnumber"]):
                print("ERROR: must supply a run number via -r")
                exit(1)
                
            if(HydraRunning):
                print("UPDATE CONFIG")
                try:
                    with open("hydra_parms.cfg") as parms_json:
                        Parms=json.load(parms_json)
                except Exception as e:
                    print("ERROR: failed to load hydra_parms.cfg")
                    print(e)
                    print("hydra_parms.cfg either does not exist or is not valid JSON (empty)")
                    print("please create hydra_parms.cfg with the following keys:")
                    print("Input, OutDir")
                    print("Typically OutDir is set to 'DELETE' and optionally both RunPeriod and RunNumber may be provided.  If not they will be created and set automatically when the above keys are valid")
                    print("exiting")
                    exit(1)

                Parms['RunPeriod']=RunPeriod
                Parms['RunNumber']=RunNumber

                with open("hydra_parms.cfg", 'w') as outfile:
                    json.dump(Parms,outfile)
            else:
                print("Start Hydra")
                hostname=os.environ["HOST"].split(".")[0]
                #hostname.replace(".jlab.org","")
                #command_for_predict="hdlog -c -o /gluex/log/hydra_predict.py."+hostname+".log -r 10 "+location+"hydra_predict.py -R "+RunPeriod+" -r "+str(RunNumber)+" -w -p -od delete -D /gluonraid2/monitoring/AI/hydra_in/ -mp "+ModelRootPath+" &"
                command_for_predict="hdlog -c -o /gluex/log/hydra_predict.py."+hostname+".log -r 10 python3 "+location+"/scripts/hydra_predict.py "+"-od delete -D "+feeder_hydra_jointDir+"/ -mp "+ModelRootPath+" -cp "+args["config"] +" &"
                print(command_for_predict)
                subprocess.call(command_for_predict,shell=True)
                time.sleep(5)

            if(keeperRunning):
                print("keeper detected")
                print("kill and restart keeper")
                try:
                    os.kill(int(kpid),signal.SIGKILL)

                    #kill all keepers!
                    subprocess.call("pkill -f hydra_keeper",shell=True)
                except Exception as e:
                    print(e)
                    pass

                hostname=os.environ["HOST"].split(".")[0]
                
                command_for_keeper="hdlog -c -o /gluex/log/hydra_keeper.py."+hostname+".log -r 10 python3 "+location+"/scripts/hydra_keeper.py -c "+location+"/scripts/keeper_config.cfg -ol "+outputlocation+"/"+str(RunPeriod)+"/rawdata_ver00/Run"+" -cp "+args["config"]
                if(test_mode):
                    command_for_keeper+=" -t"
                command_for_keeper+=" &"
                print(command_for_keeper)
                subprocess.call(command_for_keeper,shell=True)
                time.sleep(5)
                #subprocess.call("hdlog -r 10 "+location+"hydra_keeper.py -c /group/halld/hydra/scripts/keeper_config.cfg &",shell=True)
            else:
                print("Start keeper")
                print("kill and restart keeper")
                try:
                    os.kill(int(kpid),signal.SIGKILL)

                    #kill all keepers!
                    subprocess.call("pkill -f hydra_keeper",shell=True)
                except Exception as e:
                    print(e)
                    pass
                hostname=os.environ["HOST"].split(".")[0]
                
                command_for_keeper="hdlog -c -o /gluex/log/hydra_keeper.py."+hostname+".log -r 10 python3 "+location+"/scripts/hydra_keeper.py -c "+location+"/scripts/keeper_config.cfg -ol "+outputlocation+"/"+str(RunPeriod)+"/rawdata_ver00/Run"+" -cp "+args["config"]
                if(test_mode):
                    command_for_keeper+=" -t"
                command_for_keeper+=" &"
                print(command_for_keeper)
                subprocess.call(command_for_keeper,shell=True)
                time.sleep(5)

            if(feederRunning):
                print("feeder detected")
                #print("kill and restart keeper")
                try:
                    os.kill(int(kpid),signal.SIGKILL)
                except Exception as e:
                    print(e)
                    pass
                
                subprocess.call("pkill -f hydra_feeder",shell=True)

                command_for_feeder="hdlog -c -o  /gluex/log/hydra_feeder.py."+hostname+".log -r 10 python3 "+location+"/scripts/hydra_feeder.py -i "+inputLoc+"/ -o "+feeder_hydra_jointDir+"/"+str(RunPeriod)+"/"+" -M auto --config "+args["config"]+" &"
                print(command_for_feeder)
                subprocess.call(command_for_feeder,shell=True)
                #subprocess.call("hdlog -r 10 "+location+"hydra_keeper.py -c /group/halld/hydra/scripts/keeper_config.cfg &",shell=True)
            else:
                print("Start feeder")
                hostname=os.environ["HOST"].split(".")[0]

                subprocess.call("pkill -f hydra_feeder",shell=True)

                command_for_feeder="hdlog -c -o /gluex/log/hydra_feeder.py."+hostname+".log -r 10 python3 "+location+"/scripts/hydra_feeder.py -i "+inputLoc+"/ -o "+feeder_hydra_jointDir+"/"+str(RunPeriod)+"/"+" -M auto --config "+args["config"]+" &"
                print(command_for_feeder)
                subprocess.call(command_for_feeder,shell=True)
                time.sleep(5)
            #print(HydraRunning)
            #python -W ignore /group/halld/hydra/scripts/hydra_predict.py -R RunPeriod -r runnum -D INDIR -od OUTDIR -w
            # python -W ignore /group/halld/hydra/scripts/hydra_keeper.py -c /group/halld/hydra/scripts/keeper_config.cfg 
        else:
            print("Killing Hydra")
            try:
                if(hpid!=-1):
                    #os.killpg(int(hpid),signal.SIGKILL) # hdlog ruins this
                    subprocess.call("pkill -9 -f hydra_predict",shell=True)
            except Exception as e:
                print("could not kill Hydra")
                print(e)
                pass
            print("Killing Keeper")
            try:
                if(kpid != -1):
                    #os.killpg(int(hpid),signal.SIGKILL)
                    subprocess.call("pkill -9 -f hydra_keeper",shell=True)
            except Exception as e:
                print("could not kill Keeper")
                print(e)
            print("Killing Feeder")
            try:
                print("feeder pid",fpid)
                if(fpid != -1):
                    #os.killpg(int(hpid),signal.SIGKILL)
                    subprocess.call("pkill -9 -f hydra_feeder",shell=True)
            except Exception as e:
                print("could not kill feeder")
                print(e)