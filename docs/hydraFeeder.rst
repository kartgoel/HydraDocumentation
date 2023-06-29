Hydra Feeder
=====

This file formats existing images and directories to desired properties by connecting to the server and using a parser.
The resized files are stored for Hydra Predict to reference.


---------------------------------------------------------------------------------


find_files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function retrieves the files from the image directory and converting them to an absolute pathname.

-----------------------------------------------------------------------------------


ResizeAndSave
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function formats the image path and file name to assign an apropriate Active Model ID based upon the model. 
The shape of the image is resized based upon the Active Model ID in both the x and y dimensions.


--------------------------------------------------------------




