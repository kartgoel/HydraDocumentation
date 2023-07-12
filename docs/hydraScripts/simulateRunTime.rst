simulate_RunTime
=========================

This file simulates runtime by generating random queues and queries. 
It randomly selects a subdirectory from the input image directory, retrieving a list of files. 
If the files are available, it randomly selects a file from the list. 
It then executes ``runGradCAM`` to simulate a runtime. 

.. note::

    Extended code available on Github