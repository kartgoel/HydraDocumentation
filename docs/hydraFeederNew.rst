hydra_feeder
==============

This file formats existing images and directories to desired properties by connecting to the server and using a parser.
The resized files are stored for hydra_predict to reference and the original files are deleted.

find_files
------------

This method returns all files in a given directory through the use of a generator.

.. code-block:: python

    def find_files(root):
    for d, dirs, files in os.walk(root):
        for f in files:
            yield os.path.join(d, f)

Parameter
~~~~~~~~~~
- ``root``: A directory from which the files need to be retrieved

Example Usage
~~~~~~~~~~~~~~

.. code-block:: python

    walkfiles=find_files(args["img"])

ResizeAndSave
---------------

This method

Parameters
~~~~~~~~~~~~~~

- ``orig_img``: A string that represents the path to the file original image
- ``model_to_use``: A string representing a model ID or enter "AUTO" to use the databse settings
- ``force_x``: A string representing the width of the resized image
- ``force_y``: A string representing the height of the resized image
- ``outputloc``: A string representing the location where the output file will be placed

Example Usage
~~~~~~~~~~~~~~

.. code-block:: python

     ResizeAndSave(args["img"],args["model"],args["xsize"],args["ysize"],args["output"])

