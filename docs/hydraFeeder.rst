hydra_feeder
=====

This file formats existing images and directories to desired properties by connecting to the server and using a parser.
The resized files are stored for hydra_predict to reference.

.. code-block:: python

   def main(argv):
    pidf= open("/tmp/feederpid",'w')
    pidf.write(str(os.getpid()))
    pidf.close()

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--img", required=True,
    help="target image location")

    ap.add_argument("-x", "--xsize", required=False,
    help="desired x size")
    ap.add_argument("-y", "--ysize", required=False,
    help="desired y size")
    
    ap.add_argument("-M", "--model", required=False,
    help="take the desired shape from model or auto to look it up")

    ap.add_argument("-o", "--output", required=False,
    help="where feeder should save the resized images")


    args = vars(ap.parse_args())

    print("begin watch of",args["img"])

    if(os.path.isfile(args["img"])):
        ResizeAndSave(args["img"],args["model"],args["xsize"],args["ysize"],args["output"])
    elif(os.path.isdir(args["img"])):
        if(not args["output"]):
            print("To watch a directory you must supply an output -o")
            exit(1)
        while(1):
            files=[]
            walkfiles=find_files(args["img"])

            for thing in walkfiles:
                files.append(thing)

            if(len(files)==0):
                continue
        
            for f in files:
                print("==============================================")
                print(datetime.datetime.now())
                print("file: ", f.split("/"))
             
                outputLoc=args["output"]
                outputLoc="/".join(outputLoc.split("/")[:-1])+"/"+f.split("/")[-2]
                print("%s -------->  %s" % (f,outputLoc))

                status=ResizeAndSave(f,args["model"],args["xsize"],args["ysize"],outputLoc)
                os.remove(f)
        else:
            print("input not a found file or directory. exiting")
            exit(1)

---------------------------------------------------------------------------------


find_files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function retrieves the files from the image directory and converting them to an absolute pathname.

.. code-block:: python

   def find_files(root):
    for d, dirs, files in os.walk(root):
        for f in files:
            yield os.path.join(d, f)

-----------------------------------------------------------------------------------

ResizeAndSave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function formats the image path and file name to assign an apropriate Active Model ID based upon the model. 
The shape of the image is resized based upon the Active Model ID in both the x and y dimensions.

.. code-block:: python

   def ResizeAndSave(orig_img,model_to_use,force_x,force_y,outputloc):
    print("Resizing and saving")
    img_pth_parse=orig_img.split("/")
    fileName_full=img_pth_parse[-1].split(".")[0]
    print("full file name: ",fileName_full)
    print("split 1:", "_".join(fileName_full.split("_")[:-1]))
    fileName_parse="_".join(fileName_full.split("_")[:-1]).split("-") 

    
    if(len(fileName_parse)>1):
        if(fileName_parse[-1].isnumeric()):
            fileName="-".join(fileName_parse[:-1])
        else:
            fileName="-".join(fileName_parse)
    else:
        fileName=fileName_parse[0]

    print("filename=",fileName)
    chunked=False
    if(fileName_full.split("_")[-1].isnumeric()):
        chunked=True

    xsize=-1
    ysize=-1
    

    print("using sizing info from ", model_to_use)
    if(model_to_use):
        activeModelID=-1
        if(model_to_use.upper() == "AUTO"):
            print("finding model for:",fileName)
            activeID_query="Select Active_Model_ID from Plot_Types where Name=\""+fileName+"\" "

            if(chunked):
                activeID_query+="&& IsChunked=1"
            else:
                activeID_query+="&& IsChunked is NULL"

            print("active q:",activeID_query)
            dbcursor.execute(activeID_query)
            activeModelID_qr=dbcursor.fetchall()
            activeModelID=-1
            print("q result:",activeModelID_qr)
            if(len(activeModelID_qr)==1):
                activeModelID=activeModelID_qr[0]["Active_Model_ID"]
            else:
                return 1
            print("active model ID", activeModelID)
        else:
            activeModelID=model_to_use

        skip_q=False
        if(activeModelID is None):
            xsize=800
            ysize=600
            skip_q=True

        if(not skip_q):
            shapequery="SELECT InputShape from Models where ID="+str(activeModelID)
            dbcursor.execute(shapequery)
            shape= dbcursor.fetchall()[0]["InputShape"]
            print(shape)
            shape=shape.replace(")","")
            shape=shape.replace("(","")
            shape_parse=shape.split(",")
            xsize=int(shape_parse[1])
            ysize=int(shape_parse[0])
   

    if (force_x):
        xsize=int(force_x)

    if (force_y):
        ysize=int(force_y)

    if(xsize==-1 or ysize==-1):
        print("size not set! use -x -y or -M")
        exit(1)

    
    try:
        img = cv2.imread(orig_img, cv2.IMREAD_UNCHANGED)
        print("original shape: " , img.shape)
        print("Desired size is (%s,%s)" % (xsize,ysize))
    except Exception as e:
        print(e)
        return 1

    dim=(xsize,ysize)
    if(img.shape[0]!=ysize or img.shape[1]!=xsize):
        resized_img= cv2.resize(img,dim)

    if ( not outputloc ):
        cv2.imshow("Resized",resized_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        os.makedirs(outputloc,exist_ok=True)
        print("writing image to:",outputloc+"/"+img_pth_parse[-1])
        cv2.imwrite(outputloc+"/"+img_pth_parse[-1],resized_img)

    return 0

--------------------------------------------------------------




