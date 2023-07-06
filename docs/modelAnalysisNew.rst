model_analysis
======================

This file analyzes and reports various characteristics about the trained AI model. 

It ensures that the trained AI model is consistently labeling the same plots  

It compares the classification of plots by Experts versus the trained AI model to identify agreements and discrepancies. 
This data is added to an array that contains the Expert’s opinion (Good/Bad) on one axis and the AI’s label (Good/Bad) on the other, and number of overlaps are seen in each cell. 
The data on each cell of the array is also visualized with histograms.  

It quantifies the number of true/false positives/negatives and uses these values to calculate and analyze the AI model’s precision, accuracy, recall, and F1 score.  


LookAtDifferences
--------------

This method comapres the classificiation of the plot by Experts vs AI to determine the accuracy of a trained model. 

.. code-block:: python 

    def LookAtDifferences(id,difference_list,zpad):
     
     differences_list=difference_list

     if(len(difference_list)==0):
     
          differences_list_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID=Plot_Types.ID WHERE Users_Plots.Plot_Classification_ID != AIP.Plot_Classification_ID AND Users_Plots.Plot_Classification_ID != 6 AND AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber ASC;"
          dbcursor.execute(differences_list_q)
          differences_list= dbcursor.fetchall()

     list_length=len(differences_list)

     AI_plots_q="SELECT Count(*) from AI_Plots where Model_ID="+str(id)+";"
     dbcursor.execute(AI_plots_q)
     AI_plots=dbcursor.fetchone()
     AI_plots_count=AI_plots["Count(*)"]

     if(AI_plots_count==0):
          print("no inference run for this model")
          print("rerun with -I flag to run inference")
          exit(1)
     print("AI plots count:", AI_plots_count)
     print("difference list length:", list_length)
     
     if list_length==0:
          print("100% accurate!!")
          return

     print("           name                "+"  |  "+"Expert label"+" v "+"AI label"+" @ "+"AI confidence")
     for row in differences_list:
          print(row["RunPeriod"]+str(row["RunNumber"]).zfill(zpad)+"/"+str(row["Name"])+"_"+str(row['Chunk']).zfill(4)+"  |  "+row["UClass"]+" v "+row["AIClass"]+" @ "+str(row["Confidence"]))
     

Parameters 
~~~~~~~~~~~~~~~~

- ``id``: An integer representing a model ID. 
- ``difference_list``: A list of  
- ``zpad``: An integer representing the number of digits to use for zero-padding.

Example Usage
~~~~~~~~~~~~~~~

.. code-block:: python 

    LookAtDifferences(model_line["ID"],differences_list,RunNumber_padding)


-----------------------------------------------

ViewAll 
-----------------

This method retrieves classification information about all of the plots for a trained AI model and reports it. 

*Note: This function has been commented out in the main argument.* 

.. code-block:: python 

    def ViewAll(id):
     differences_list_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID = Plot_Types.ID WHERE AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber desc;"
     print(differences_list_q)
     dbcursor.execute(differences_list_q)
     differences_list= dbcursor.fetchall()

     list_length=len(differences_list)

     i=0

     print(list_length)
     
     for row in differences_list:
          print(row["RunPeriod"]+"/"+str(row["RunNumber"])+"  |  "+row["UClass"]+" v "+row["AIClass"]+" @ "+str(row["Confidence"]))
     
Parameter
~~~~~~~~~~~~~~~~~~

- ``id``: An integer representing a model ID.


-----------------------------------------

MakeConfusionMatrix
------------------

This method returns a 2D array confusion matrix along with a list of the labels given to the plots analyzed by the AI. 

*Note: This function has been commented out of the main argument.*

.. code-block:: python 

    #Extended code available on GitHub
    def MakeConfusionMatrix(id,labels,doScaling):


Parameters
~~~~~~~~~~~~~~~~~~

- ``id``: An integer representing a model ID.
- ``labels``: A list of plot labels. 
- ``doScaling``: A boolean value indicatin whether scaling should be applied. 


--------------------------------------------

MakeConfidenceDistributionMatrix
------------

This method creates a confusion matrix based on the confidence levels of AI classificaions for an AI model. 
The data is displayed on histograms based on the figure of a 2D array.

.. code-block:: python 

    #Extended code available on GitHub
    def MakeConfidenceDistributionMatrix(id,labels):


Parameters 
~~~~~~~~~~~~~~

- ``id``: An integer representing a model ID. 
- ``labels``: A list of plot labels.  


Example Usage
~~~~~~~~~~~~~~

.. code-block:: python 

     test = MakeConfidenceDistributionMatrix(model_line["ID"],valid_labels)


----------------------------------------

DoThresholdOptimization
---------------

This method labels the plots based on whether they were a true/false positive/negative. 
It uses these values to analyze the precision, accuracy, recall, and F1 score. 
These evalutation metrics are them plotted as an array. 

.. code-block:: python 

    #Extended code available on GitHub
    def DoThresholdOptimization(data2d, Labels_list):


Parameters 
~~~~~~~~~~~~~~~

- ``data2d``: A dictionary containing data of confidence levels.
- ``Labels_list``: A list containing the labels for plots. 

Example Usage 
~~~~~~~~~~~~~

.. code-block:: python 

    results = DoThresholdOptimization(test[0],valid_labels)


-----------------------------------------------

MakeDanielConfidenceDistributionMatrix
--------------

This method  is a tool for developers to see what plots are being excluded from the confusion matrix. 

*Note: This function has been commented out of the main argument.* 

.. code-block:: python 

    #Extended code available on GitHub
    def MakeDanielConfidenceDistributionMatrix(id,labels):


Parameters
~~~~~~~~~~~~~~~~~~~

- ``id``: An integer representing a model ID.
- ``labels``: A list of plot labels. 


---------------------

DoInference
----------------

This method reaches a conclusion about the model's performance using the validation generator and inserts results into the database. 

.. code-block:: python 

    #Extended code available on GitHub
    def DoInference(modelInstance,model_line,DBConnector,RunNumber_padding):


Parameters 
~~~~~~~~~~~~~~~

- ``modelInstance``: An object representing an AI model. 
- ``model_line``: A dictionary containing information about the AI model. 
- ``DBConnector``: An object represents the connector for the database that is responsible for executing queries.
- ``RunNumber_padding``: An integer representing the padding for the run number. 

Example Usage 
~~~~~~~~~~~~~~~

.. code-block:: python 

    if(args["inference"]):
      DoInference(modelInstance,model_line,DBConnector,RunNumber_padding)

