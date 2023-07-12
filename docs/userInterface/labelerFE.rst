.. _labelerFE:

How to Label Plots
=======================

This is Hydra's web-based labeler, which allows experts to label plots and assigns each plot type a label leader. 
Compete with other experts to dominate the leaderboard and be declared the Label Leader!

For a more indepth description on the **labeler.html** file, see here: :ref:`labelerHTML`

.. image:: img/Labelerwebsite.png
	:align: center

A 
~~~~~~~~~~~~~

After logging in, this area contains a drop-down menu of all available plot type with its dynamic palette of labels. 
If you do not have permission to label a certain plot, the palette will not exist, and you will be presented with a notification of the lack of permissions. 

B 
~~~~~~~~~~~~~~~~~

This is the grid of plots which need labeling (or all the plots in Editor mode; see **D**).
Simply choose a label from the palette located in **A**, and left click on the image to label it (mark the image with the associated color for the label). 
A number should appear next to the word "Apply" in **C**, which indicates how many plots have been assigned a label form the current batch but are yet to be recorded. 
It is recommended for efficiency purposes that users choose a single label and label all plots with that label; apply those using the button in **C**, and repeat until left with large blocks of single labels. 
To assign the selected label to multiple plots at once, click on an image and hold down the **Shift** key to assign all plots between two selected points the selected label (includes endpoint images.)

C 
~~~~~~~~~~~~~~~~

Click on "Apply" to record assigned labels and remove those images from the grid of yet-to-be-labeled images. 

D 
~~~~~~~~~~

This area contains several options affecting the resulting grid of images displayed in **B**. 

The topmost toggle labeled "Editor mode" replaces the grid of "to-be-labeled" images with all the images in the database, including their labels. 

.. note::

   It is **NOT** recommended to toggle editor mode on unless the run range is reasonable set.
   Failure to set the run range can, in the case of too many images, lead to marked performance hits up to and including browser crash. 
   It is in this mode where corrections can be made to the labels of already labeled images. 

   When editor mode is enabled, a series of labels will appear with a checkbox. 
   Simply checking a box will include those labeled images in the resulting grid. 
   This can be useful for quick relabeling of only subsets of images (i.e. A new label is introduced, so "Bad" images need to be split).

   Also note that all boxes checked and unchecked will yield the same grid. 

The grid can be filtered to display only those images in a given run range by using two inputs: the lower and upper limit of the run range. 

The "Columns" drop-down changes how mnay columns exist per row in the displayed grid. 
Depending on the screen size, sometimes the last column is cut off. 


