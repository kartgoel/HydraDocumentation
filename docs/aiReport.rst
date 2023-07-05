AIReport
=====================

This file includes the ``AIReport`` class, which provides methods for intializing the report, setting and retrieving metadata, performing analysis, and generating reports. 


Initialization
-------------------

The ``__inut__`` method initializes the ``AIReport`` object. 

.. code-block:: python 

     def __init__(self,reportType="classification",reportMetaData=[]):
        

Parameters
~~~~~~~~~~~~~~~~~~~~

- ``reportType``: A string representing the type of report. Default is "classification". 
- ``reportMeta``: A list of strings representing metadata keys. Default is an empty list. 


setMetaDataVal
-------------------

This method sets the value of a specific metadata key. 

.. code-block:: python 

    def setMetaDataVal(self,key,value):
        self.metaData[key]=value


Parameters
~~~~~~~~~~~~~~~~~~~~~~

- ``key``: A string representing the metadata key.
- ``value``: A value to set for the metadata key. 


--------------------------------------------------------------------

setMetaData
------------------

This method sets the metadata using a dictionary.

.. code-block:: python 

    def setMetaData(self,dict):


Parameter
~~~~~~~~~~~~~~~~~~~~

- ``dict``: A dictionary containing the metadata key-value pairs. 


Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    report.setMetaData(metaData)


-------------------------------------------------

Result
---------------------

This method sets the analysis results. 


.. code-block:: python

    def Result(self,confidences,labels={}):


Parameters
~~~~~~~~~~~~~~~~~~~~~~~

- ``confidences``: A list of confidence values. 
- ``labels``: An optional dictionary of labels.


--------------------------------------------

getTopN
----------------

This method returns a certain number of labels, N, based on the analysis results. 

.. code-block:: python 

    def getTopN(self,n):


Parameter
~~~~~~~~~~~~~~~~~~

- ``n``: An integer representing the number of top labels. 


Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    return label in self.getTopN(n)


--------------------------------------------------

inTopN
-------------

This method checks if a label in found in a certain number, N, of the top labels. 

.. code-block:: python 

    def inTopN(self,label,n):


Parameters 
~~~~~~~~~~~~~

- ``label``: A string representing which label to check.
- ``n``: An interger representing the number of top labels. 


----------------------------------------------------

Write 
---------------

This method generates a report based on the specified format: JSON or XML. 

.. code-block:: python 

    def Write(self,format):


Parameters
~~~~~~~~~~~~~~~~~~~

- ``format``: A string representing the format of the saved report. 


------------------------------------------------

Load
------------------

This method loads a saved report in the specified format: JSON or XML. 

.. code-block:: python 

    def Load(self,savedReport,format):


Parameters
~~~~~~~~~~~~~~~~~~~~

- ``savedReport``: A string representing the saved report. 
- ``format``: A string representing the format of the saved report. 