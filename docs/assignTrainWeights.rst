assign_train_weights
================

This file contains two methods which aid the machine learning algorithm by weighing plots differently and using these values to train AI models.

RandomTrainingTestingSplit
---------------------------

This method assigns training weights to random plots in the database which are used to train and test models.
The ``TrainingWeight`` column in the database will be updated with the calculated training weights.

.. code-block:: python

    def RandomTrainingTestingSplit(runPeriodSubstring,  Trainingfraction):

Parameters
~~~~~~~~~~~~~~~~~~

- ``runPeriodSubstring``: A string represnting desired run period from the database.
- ``Trainingfraction`` A float represnting a percentage of the data being used for training models. The remaining percentage of data will be utilized for testing the models.

Example Usage
~~~~~~~~~~~~~

.. code-block:: python
    RandomTrainingTestingSplit("CDC_occupancy/CDC_occ", 0.6)

------------------------------------

TrainTestSplit2
-----------------

This method assigns training weights to specific plots in the database which are used to train and test models.
The board information is retreived from the file and split into training and testing sets.
The ``TrainingWeight`` column in the database will be updated with the calculated training weights.

.. code-block:: python

    def TrainTestSplit2(logfileWithPath, trainingFraction):
    
Parameters
~~~~~~~~~~~~~~

- ``logfileWithPath``: A string representing the path of the file containg a log of the boards.
- ``trainingFraction`` A float representing the percentage of boards being used for training models. The remaining percentage of data will be utilized for testing the models.

Example Usage
~~~~~~~~~~~~~~~~

.. code-block:: python
    TrainTestSplit2("/work/halld2/home/davidl/2020.09.08.Hydra_CDC_Training/hydra_cdc/images/origin_log.txt", 0.6)

