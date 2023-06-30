assign_train_weights
=======================================

This file contains methods that assign varying weights to plots based on their importance. 

-------------------------------------------

RandomTrainingTestingSplit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function executes training weight queries and assigns valuable plots more influence over the report. Plots that are deemed more important are present more times than typical plots. 

.. code-block:: python

    def RandomTrainingTestingSplit(runPeriodSubstring,  Trainingfraction):

        getIds_query = 'SELECT ID FROM Plots where RunPeriod like "'+str(runPeriodSubstring)+'%"'
        dbcursor.execute(getIds_query)
        result = dbcursor.fetchall()
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

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=0 WHERE ID in '+str(tuple(testingIds))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=1 WHERE ID in '+str(tuple(trainingIds))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

---------------------------------------------

TrainTestSplit2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function executes training weight queries based upon training and testing boards. 

.. code-block:: python

    def TrainTestSplit2(logfileWithPath, trainingFraction):

        f = open(logfileWithPath, 'r')
        lines = f.read().split('\n')
        id_board = {}
        for line in lines[1:]:
            if len(line) <= 0:
                break
            words = line.split(' ')
            board = words[5][3:]
            name = words[0]
            name = 'CDC_occupancy/'+name[:-4]
            if board not in id_board:
                id_board[board] = [name]
            else:
                id_board[board].append(name)

        numberOfBoards = len(id_board.keys())
        boardKeys = list(id_board.keys())
        numberOfTrainingBoards = int(numberOfBoards*trainingFraction)
        trainingBoards_index = random.sample(range(numberOfBoards), numberOfTrainingBoards)
        print("Training Boards indices: ", trainingBoards_index)
        trainingNames = []
        testingNames = []
        trainingBoards = []
        testingBoards = []
        for i in range(numberOfBoards):
            if i in trainingBoards_index:
                trainingNames.extend(id_board[boardKeys[i]])
                trainingBoards.append(boardKeys[i])
            else:
                testingNames.extend(id_board[boardKeys[i]])
                testingBoards.append(boardKeys[i])
        
        print("Boards set to 1: ", trainingBoards)
        print("Boards set to 0: ", testingBoards)
        
        print("Training: ", trainingNames)
        print("Testing: ", testingNames)

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=1 WHERE RunPeriod in '+str(tuple(trainingNames))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

        updateTrainingWeights_query = 'UPDATE Plots SET TrainingWeight=0 WHERE RunPeriod in '+str(tuple(testingNames))
        dbcursor.execute(updateTrainingWeights_query)
        dbcnx.commit()

        
        TrainTestSplit2("/work/halld2/home/davidl/2020.09.08.Hydra_CDC_Training/hydra_cdc/images/origin_log.txt", 0.6)
