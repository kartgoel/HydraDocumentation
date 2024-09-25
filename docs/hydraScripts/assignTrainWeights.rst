assign_train_weights
================

This file contains two methods which aid the machine learning algorithm by weighing plots differently and using these values to train AI models.

RandomTrainingTestingSplit
---------------------------

This method assigns training weights to random plots in the database which are used to train and test models.
The ``TrainingWeight`` column in the database will be updated with the calculated training weights.

.. code-block:: python

    def RandomTrainingTestingSplit(runPeriodSubstring,  Trainingfraction):
        # getNumberOfImages_query = 'SELECT count(*) FROM Plots where RunPeriod like "'+str(runPeriodSubstring)+'%"'
        # dbcursor.execute(getNumberOfImages_query)
        # result = dbcursor.fetchall()
        # n = result[0]['count(*)']

        getIds_query = 'SELECT ID FROM Plots where RunPeriod like "'+str(runPeriodSubstring)+'%"'
        dbcursor.execute(getIds_query)
        result = dbcursor.fetchall()
        # print(result)
        n = len(result)
        numTrainingSamples = int(n*Trainingfraction)
        numTestingSamples = n - numTrainingSamples
        
        # IDs to be used as testing data
        randlist = random.sample(range(0, n), numTestingSamples)

        testingIds = []
        trainingIds = []
        for i in range(n):
            if i in randlist:
                testingIds.append(result[i]['ID'])
            else:
                trainingIds.append(result[i]['ID'])

        # print("Testing ids length: ", len(testingIds))
        # print("Testing ids: ", testingIds)

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=0 WHERE ID in '+str(tuple(testingIds))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=1 WHERE ID in '+str(tuple(trainingIds))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

Parameters
~~~~~~~~~~~~~~~~~~

- ``runPeriodSubstring``: A string representing the desired run period from the database.
- ``Trainingfraction``: A float represnting a percentage of the data being used for training models. The remaining percentage of data will be utilized for testing the models.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

    RandomTrainingTestingSplit("CDC_occupancy/CDC_occ", 0.6)

------------------------------------

TrainTestSplit2
-----------------

This method assigns training weights to specific plots in the database which are used to train and test models.
The board information is retrieved from the file and split into training and testing sets.
The ``TrainingWeight`` column in the database will be updated with the calculated training weights.

.. code-block:: python

    def TrainTestSplit2(logfileWithPath, trainingFraction):
    
Parameters
~~~~~~~~~~~~~~

- ``logfileWithPath``: A string representing the path of the file containg a log of the boards.
- ``trainingFraction``: A float representing the percentage of boards being used for training models. The remaining percentage of data will be utilized for testing the models.

Example Usage
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Extended code available on Github
    TrainTestSplit2("/work/halld2/home/davidl/2020.09.08.Hydra_CDC_Training/hydra_cdc/images/origin_log.txt", 0.6)

