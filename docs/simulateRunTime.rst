simulate_RunTime
=========================

This file 

.. code-block:: python 

    def main(argv):
    

    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=True, help="path to config file")
    ap.add_argument("-i", "--input", required=True, help="full path to root directory of input images")

    args = vars(ap.parse_args())

    # Set the path to your directory here
    directory_path = args["input"]

    DBConnector = connector.DBManager(args["config"])

    # Set the interval between file selections here (in seconds)
    interval = 0
    i=0
    while True:
        i+=1
        print('generating image '+str(i))
        # Get a list of all subdirectories in the main directory
        subdirectories = [os.path.join(directory_path, d) for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]
    
        # Randomly select a subdirectory
        selected_subdirectory = random.choice(subdirectories)
        print(selected_subdirectory)
        # Get a list of all files in the selected subdirectory
        files = [os.path.join(selected_subdirectory, f) for f in os.listdir(selected_subdirectory) if os.path.isfile(os.path.join(selected_subdirectory, f))]
    
        if len(files) > 0:
            # Randomly select a file from the list of files
            selected_file = random.choice(files)

            # Print the path of the selected file
            print(selected_file)
            file_parse=selected_file.split("/")
            file_type=file_parse[-1].split(".")[1]
            filename_parse=file_parse[-1].split(".")[0].split("_")
            #print(filename_parse)
            if(filename_parse[-1].isnumeric()):
                filename_parse=filename_parse[:-1]

            filename_subparse=filename_parse[-1].split("-")
            
            #print(filename_subparse)
            if(filename_subparse[-1].isnumeric()):
                filename_subparse=filename_subparse[:-1]

            filename_parse[-1]="-".join(filename_subparse)

            filename="_".join(filename_parse)

            model_ID_q="SELECT ID,Active_Model_ID from Plot_Types where Name=\""+filename+"\" && FileType=\""+file_type+"\" && IsChunked=1"
            #print(model_ID_q)
            model_id_r=DBConnector.FetchAll(model_ID_q)
            if(len(model_id_r)==1):
                model_id=model_id_r[0]["Active_Model_ID"]
                if(model_id==None):
                    model_id=-1

                cmmd_str="python3 runGradCAM.py -c "+args["config"]+" -i "+selected_file+" -M "+str(model_id)
                print(cmmd_str)
                os.system(cmmd_str)
            #
    
        # Wait for the specified interval before selecting another file
        #time.sleep(interval)


