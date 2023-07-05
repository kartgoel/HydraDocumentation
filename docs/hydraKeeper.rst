hydra_keeper
===========

This file uses the EPICS library to evaluate whether to keep the plot and moves it to its respective output location. 
A File Handler handles all the log messages and exceptions while 'Hello Hydra' messages are sent after the socket binds with the constructed address.

KeeperAnnounce
-----------------

This method constantly announces the Keeper's activation in the system.

.. code-block:: python

    def KeeperAnnounce(context, announcePort)

Parameters
~~~~~~~~~~

- ``context ``: This ZMQ context represents the connections required for creating the sockets.
- ``announcePort ``: This integer represents the port on which the announcment for the keeper should be made.

----------------------------

getKeepPercent
--------------------

This method constructs and SQL query based on the parameters, executes the query, and processes the results of the query.

.. code-block:: python

    def getKeepPercent(DBConnector, fileName, fileType, isChunked)


Parameters
~~~~~~~~~~~~~~

- ``DBConnector``: An object represents the connector for the database that is responsible for executing queries
- ``fileName``: A string that represents name of the file.
- ``fileType``: A string that represents type of the file.
- ``isChunked``: A boolean representing whether the file is chunked or not.

---------------------------------------------------

ConfirmVerdict
---------------

This method retrieves the verdict and evaluates its confidence based upon the Confirmation Threshold.
The verdict and the confirmation status are returned.

.. code-block:: python

    def ConfirmVerdict(Model_config, AIReport, VerdictConfidence)

Parameters
~~~~~~~~~~~~

- ``Model_config``: A dictionary representing the configuration of the model.
- ``AIReport``: An AIReport object representing the AI Report
- ``VerdictConfidence``: A float representing the confidence percentage of the verdict

--------------------------

AnalyzeReport
----------------

This method analyzes the AI Report and updates the database accordingly along with handlng EPICS functionality if relevant.

.. code-block:: python

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

This method uses the AI model to decide whether to keep the plot or not.

.. code-block:: python

    def SetStore(DBConnector, Plot_Type_ID,chunkNum,item,percent,RunPeriod,RunNumber_padding,RunNumber,outputlocation,test_mode):

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
- ``test_mode``: A boolean representing if the script is active or not.

--------------------------

GetKeeperConfig
--------------

This method returns the configuration for the keeper from the database in the form of a dictionary.

.. code-block:: python

    GetKeeperConfig(DBConnector):

Parameters
~~~~~~~~~~~
- ``DBConnector``: An object representing the connector for the database that executes queries.

-----------------------

moveFile
------------

This method is responsible for moving a given file from its input location to its output location.

.. code-block:: python

    def moveFile(outputlocation, RunPeriod,RunNumber_padding, RunNumber, item):

Parameters
~~~~~~~~~~~
- ``item``: A string representing the file item.
- ``RunNumber_padding``: An integer representing the padding for the run number.
- ``RunNumber``: An integer representing the run number.
- ``RunPeriod``: A dictionary representing the metadata of the AI report.
- ``outputlocation``: A string representing the name of the output location.







