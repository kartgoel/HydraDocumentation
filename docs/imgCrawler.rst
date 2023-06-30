imgCrawler
=================

This file scans present directories for plots to analyze in the JLab halls. 

.. code-block:: python 
    
    def main(argv):
    ap = argparse.ArgumentParser()

    ap.add_argument("-R", "--runperiod", required=False,
                    help="Run a scan over a given Run Period and the simulated directory only")

    args = vars(ap.parse_args())

    crawlerRunning = False
    cpid = -1
    crawler_pidFile = "/tmp/gluex_img_crawler_pid"

    if (os.path.exists(crawler_pidFile)):
        try:
            cpidf = open(crawler_pidFile, "r")
            cpid = cpidf.readline().strip()
            print(cpid)

            cpidf.close()
            os.kill(int(cpid), 0)
        except OSError:
            pass
        else:
            crawlerRunning = True

    if (crawlerRunning):
        print("crawler is already running")
        exit(0)
    else:
        pidf = open(crawler_pidFile, 'w')
        pidf.write(str(os.getpid()))
        pidf.close()

    root_loc = "/work/halld/online_monitoring/AI/keeper/"

    RunPeriod_to_scan = ""
    if (args["runperiod"]):
        RunPeriod_to_scan = args["runperiod"]

    locations_to_scan = []
    if RunPeriod_to_scan == "":
        locations_to_scan = os.listdir(root_loc)
    elif RunPeriod_to_scan == "none":
        locations_to_scan = ["simulated"]
    else:
        locations_to_scan = [RunPeriod_to_scan, "simulated"]

    print(locations_to_scan)
    ScanLocations(root_loc, locations_to_scan)



-----------------

ScanLocations
~~~~~~~~~~~~~~~~

This function scans locales for image retrieval in different halls at JLab. 

.. code-block:: python

    def ScanLocations(root_loc, locations):

        for locale in locations:
            print(locale)
            if locale[0:3] == "Run":
                subloc = root_loc+"/"+locale+"/rawdata_ver00/"
                Runs_list = os.listdir(subloc)
                for Run in Runs_list:

                    if (not str(Run.replace("Run", "")).isnumeric()):
                        print("continuing")
                        continue

                    RunNumber = int(Run.replace("Run", ""))
                    if RunNumber < 10000:
                        continue

                    plots_list = os.listdir(subloc+Run)
                    for plot in plots_list:
                        Name = plot.split(".")[0]
                        FileType = plot.split(".")[1]
                        chunked = False
                        if Name.split("_")[-1].isnumeric():
                            chunked = True
                            Name = "_".join(Name.split("_")[:-1])

                        if ("-" in Name):
                            padNum = Name.rsplit("-", 1)[1]
                            if (padNum.isnumeric()):
                                Name = "-".join(Name.split("-")[:-1])

                        print("EXTRACTED NAME", Name)
                        if chunked:
                            Plot_Type_ID_q = "SELECT ID FROM Plot_Types where Name=\""+Name + \
                                "\""+" && FileType=\""+FileType+"\" && IsChunked is not NULL"
                        else:
                            Plot_Type_ID_q = "SELECT ID FROM Plot_Types where Name=\"" + \
                                Name+"\""+" && FileType=\""+FileType+"\" && IsChunked is NULL"

                        print(Plot_Type_ID_q)
                        dbcursor.execute(Plot_Type_ID_q)
                        Plot_Type_ID = dbcursor.fetchall()
                        print(Plot_Type_ID)
                        if (len(Plot_Type_ID) != 1):
                            continue

                        already_inserted = False
                        if chunked:
                            chunkNum = int(plot.split(".")[0].split("_")[-1])
                        else:
                            chunkNum = 0

                        already_inserted_q = "SELECT * from Plots where Plot_Types_ID=" + \
                            str(Plot_Type_ID[0]["ID"])+" && RunNumber="+str(RunNumber) + \
                            " && RunPeriod=\""+subloc+"Run" + \
                            "\" && Chunk="+str(chunkNum)
                        dbcursor.execute(already_inserted_q)
                        Plot = dbcursor.fetchall()
                        print("check if already inserted, plots found:", len(Plot))
                        if (len(Plot) == 0):
                            insert_plot_q = "INSERT into Plots (Plot_Types_ID,RunPeriod,RunNumber,Chunk) VALUES("+str(
                                Plot_Type_ID[0]["ID"])+", \""+subloc+"Run"+"\","+str(RunNumber)+","+str(chunkNum)+")"
                            print(insert_plot_q)
                            dbcursor.execute(insert_plot_q)
                            dbcnx.commit()

            elif locale[0:3] == "sim":
                print("current locale", locale)
                root_loc = "/work/halld2/data_monitoring/"

                Plot_Types_list = os.listdir(
                    "/work/halld2/data_monitoring/"+locale)
                for plot_type in Plot_Types_list:
                    Name = plot_type
                    chunked = False
                    RunNum = "0"
                    if Name.split("_")[-1].isnumeric() and Name.split("_")[-2].isnumeric():
                        chunked = True
                        RunNum = "-"+Name.split("_")[-2]
                        Name = "_".join(Name.split("_")[:-1])

                    if ("-" in Name):
                        padNum = Name.rsplit("-", 1)[1]
                        if (padNum.isnumeric()):
                            Name = "-".join(Name.split("-")[:-1]) 
                    print("EXTRACTED NAME:", Name)
                    if chunked:

                        Plot_Type_ID_q = "SELECT ID FROM Plot_Types where Name=\"" + \
                            Name+"\""+" && IsChunked is not NULL"
                    else:
                        Plot_Type_ID_q = "SELECT ID FROM Plot_Types where Name=\"" + \
                            Name+"\""+" && IsChunked is NULL"

                    print(Plot_Type_ID_q)

                    dbcursor.execute(Plot_Type_ID_q)
                    Plot_Type_ID = dbcursor.fetchall()
                    if (len(Plot_Type_ID) != 1):
                        continue

                    print(Plot_Type_ID[0]["ID"])
                    print("getting images from:", root_loc+locale+"/"+plot_type)
                    plots_list = os.listdir(root_loc+locale+"/"+plot_type)
                    print(plots_list)
                    for plot in plots_list:
                        already_inserted = False
                        if chunked:
                            chunkNum = int(plot.split["_"][-1])
                        else:
                            chunkNum = 0

                        RunPeriod = Name+"/"+plot.split(".")[0]

                        already_inserted_q = "SELECT * from Plots where Plot_Types_ID=" + \
                            str(Plot_Type_ID[0]["ID"])+" && RunNumber="+RunNum + \
                            " && RunPeriod=\"" + \
                            root_loc+"/simulated/"+str(RunPeriod)+"\" && Chunk="+str(chunkNum)
                        dbcursor.execute(already_inserted_q)
                        Plot = dbcursor.fetchall()
                        if (len(Plot) == 0):
                            insert_plot_q = "INSERT into Plots (Plot_Types_ID,RunPeriod,RunNumber,Chunk) VALUES("+str(
                                Plot_Type_ID[0]["ID"])+", \""+root_loc+"/simulated/"+str(RunPeriod)+"\","+str(RunNum)+","+str(chunkNum)+")"
                            print(insert_plot_q)
                            dbcursor.execute(insert_plot_q)
                            dbcnx.commit()

