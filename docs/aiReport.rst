AIReport
=================

This library establishes infrastructure for the retrieval of the results of AI models. 

.. code-block:: python

    class AIReport:
    """A python class for a generic AI report using json and 0MQ"""

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
    

    def printType(self):
        print(self.reportType)
    
    def printMetaData(self):
        print(self.metaData)
    
    def getMetaData(self):
        return(self.metaData)

    def setMetaDataVal(self,key,value):
        self.metaData[key]=value
    
    def setMetaData(self,dict):
        for key in dict:
            self.metaData[key]=dict[key]
    
    def Result(self,confidences,labels={}):
        if self.reportType.upper() == "CLASSIFICATION":
            self.analysis["Labels"]=labels
            self.analysis["Confidences"]=confidences
        elif self.reportType.upper() == "REGRESSION":
            self.analysis["Result"]=confidences

    def printAnalysis(self):
        print(self.analysis)
    
    def getModelLabels(self):
        if self.reportType.upper() == "CLASSIFICATION":
            return self.analysis["Labels"]
        else:
            return "NA"

    def getConfidences(self):
        if self.reportType.upper() == "CLASSIFICATION":
           return self.analysis["Confidences"]
        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]

    def getVerdict(self):
        if self.reportType.upper() == "CLASSIFICATION":
            max_value = max(self.analysis["Confidences"])
            verdictLabel = self.analysis["Labels"][self.analysis["Confidences"].index(max_value)]
            return verdictLabel

        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]

    def printVerdict(self):
        if self.reportType.upper() == "CLASSIFICATION":
            print(self.getVerdict(),"@",self.getVerdictConfidence())

        elif self.reportType.upper() == "REGRESSION":
            print(self.analysis["Result"])

    
    def getVerdictConfidence(self):
        if self.reportType.upper() == "CLASSIFICATION":
            return max(self.analysis["Confidences"])

        elif self.reportType.upper() == "REGRESSION":
            return self.analysis["Result"]

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
    
    def inTopN(self,label,n):
        return label in self.getTopN(n)

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
    
    def Load(self,savedReport,format):
        if(format.upper()=="JSON"):
            loaded=json.loads(savedReport)
            #print(loaded)

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
