AIReport
=====================

This file includes the ``AIReport`` class, which provides methods for intializing a report, setting and retrieving metadata, performing analysis, and generating reports using JSON or 0MQ formatting. 


Initialization
-------------------

The ``__init__`` method initializes the ``AIReport`` object. 

.. code-block:: python 

     def __init__(self,reportType="classification",reportMetaData=[]):
        self.reportType=reportType

        #need a block for meta data RunNumber/RunPeriod etc
        self.metaDataKeys=reportMetaData
        self.metaData={}
        #intialize empty metadata dictionary. The metaDataKeys should be fixed and the dictionary itself resetable and mutable
        for key in self.metaDataKeys: 
            self.metaData[key] = None

        #need a block for analysis
        self.analysisKeys=[]

        if reportType.upper() == "CLASSIFICATION":
            self.analysisKeys=["Labels","Confidences"]
        elif reportType.upper() == "REGRESSION":
            self.analysisKeys=["Result"]

        self.analysis={}
        for key in self.analysisKeys:
            self.analysis[key]=None


Parameters
~~~~~~~~~~~~~~~~~~~~

- ``reportType``: A string representing the type of report. Default is "classification". 
- ``reportMeta``: A list of strings representing metadata keys. Default is an empty list. 

------------------------

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
        for key in dict:
            self.metaData[key]=dict[key]


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
        if self.reportType.upper() == "CLASSIFICATION":
            self.analysis["Labels"]=labels
            self.analysis["Confidences"]=confidences
        elif self.reportType.upper() == "REGRESSION":
            self.analysis["Result"]=confidences


Parameters
~~~~~~~~~~~~~~~~~~~~~~~

- ``confidences``: A list of confidence values. 
- ``labels``: An optional dictionary of labels.

--------------------------------------------------------

getModelLabels
------------------------

This method returns the labels used in the analysis. 

.. code-block:: python

     def getModelLabels(self):
        if self.reportType.upper() == "CLASSIFICATION":
            return self.analysis["Labels"]
        else:
            return "NA"



Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    model_labels = AIReport.getModelLabels()


--------------------------------------------

getConfidences
--------------------

This method returns the confidence values or result value from the analysis.

.. code-block:: python 
    
    def getConfidences(self):
        if self.reportType.upper() == "CLASSIFICATION":
           return self.analysis["Confidences"]
        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]



Example Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    reportConfidences=AIReport.getConfidences()


----------------------------------------------

getVerdict
-------------

This method retrieves the verdict label for a classification or regression report. 

.. code-block:: python 

    def getVerdict(self):
        if self.reportType.upper() == "CLASSIFICATION":
            max_value = max(self.analysis["Confidences"])
            verdictLabel = self.analysis["Labels"][self.analysis["Confidences"].index(max_value)]
            return verdictLabel

            
        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]


Example Usage
~~~~~~~~~~~~~~~~

.. code-block:: python 

    verdict=AIReport.getVerdict()


------------------------------------------------------


printVerdict
--------------

This method prints the verdict label and confidence for classification and regression reports.

.. code-block:: python 

    def printVerdict(self):
        if self.reportType.upper() == "CLASSIFICATION":
            print(self.getVerdict(),"@",self.getVerdictConfidence())
        elif self.reportType.upper() == "REGRESSION":
            print(self.analysis["Result"])


-------------------------------------------------------

getVerdictConfidence
----------------

This method returns the confidence value for the verdict label in classification or regression reports. 

.. code-block:: python 

     def getVerdictConfidence(self):
        if self.reportType.upper() == "CLASSIFICATION":
            return max(self.analysis["Confidences"])

        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]


-------------------------------------------------

getTopN
----------------

This method returns a certain number of labels, N, based on the analysis results. 

.. code-block:: python 

    def getTopN(self,n):
        if self.reportType.upper()=="Regression":
            return [self.analysis["Result"]]

        #need to be ablew to mutate this list to not return the topo repeatedly
        mutable_confidences=self.analysis["Confidences"].copy()

        #to be returned
        topN=[]
        #faster way to do the append
        App=topN.append

        #while you still need more in your top N
        while(len(topN)<n):

            #if there are no results or n>then all labels break.  Because confidences must by definition be greater than 0 we set the mutable
            #confidence to -1. If max() ever returns -1 we have returned everything; so stop 
            if(len(mutable_confidences)==0 or max(mutable_confidences)==-1):
                break

            #get the index of the biggest confidence
            max_index=mutable_confidences.index(max(mutable_confidences))

            #append to the to be returned topN
            App(self.analysis["Labels"][max_index])
            
            #to keep the values and dictionary of labels aligned we set the mutable confidences to -1
            mutable_confidences[max_index]=-1
            

        return topN


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
        return label in self.getTopN(n)


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
        datum={}
        datum["MetaData"]=self.metaData
        datum["Analysis"]=self.analysis
        conf = datum["Analysis"]["Confidences"]
        if type(conf) is np.ndarray:
            datum["Analysis"]["Confidences"] = [float(x) for x in conf]
        if(format.upper()=="JSON"):
            print("DATUM: ", datum)
            return json.dumps(datum)
        elif(format.upper()=="XML"):
            elem = Element("Report")
            for key, val in datum.items():
                child = Element(key)
                child.text = str(val)
                elem.append(child)
                for ckey, cval in child.items():
                    gchild = Element(ckey)
                    gchild.text = str(cval)
                    child.append(gchild)
                    for gckey, gcval in gchild.items():
                        ggchild = Element(gckey)
                        ggchild.text = str(gcval)
                        gchild.append(ggchild)

            return tostring(elem)


Parameters
~~~~~~~~~~~~~~~~~~~

- ``format``: A string representing the format of the saved report. 


------------------------------------------------

Load
------------------

This method loads a saved report in the specified format: JSON or XML. 

.. code-block:: python 

    def Load(self,savedReport,format):
        if(format.upper()=="JSON"):
            loaded=json.loads(savedReport)

            self.metaDataKeys=loaded["MetaData"].keys()
            self.setMetaData(loaded["MetaData"])

            #need a block for analysis
            self.analysisKeys=loaded["Analysis"].keys()
            
            if "Result" in self.analysisKeys:
                self.reportType="REGRESSION"
            else:
                self.reportType="CLASSIFICATION"

            self.analysis=loaded["Analysis"]

            self.analysis["Labels"]={int(k):v for k,v in self.analysis["Labels"].items()}

Parameters
~~~~~~~~~~~~~~~~~~~~

- ``savedReport``: A string representing the saved report. 
- ``format``: A string representing the format of the saved report. 