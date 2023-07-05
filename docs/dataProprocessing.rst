DataPreprocessing
======================

This file includes the ``DataPreparation`` class, which provides methods to split the data into train and test sets for machine learning tasks.


train_test_split
-----------------

This method splits the data into train and test sets. 
It can perform label balancing based on the number of bad examples. 

.. code-block:: python

    def train_test_split(self, all_df,trainamt,BS,type="normal"):


Parameters
~~~~~~~~~~~~~~~~~~~~~

- ``all_df``: A Pandas datafram containing all the available data that can be split into train and test sets. 
- ``trainamt``: A float value between 0 and 1 representing the fraction of the data to be used as training data. 
- ``BS``: An integer representing the batch size. 
- ``type``: An optional string specifying the type of split to perform. The options are "normal" (default), "undersample", "subsample", and "supersample". 


Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    training_dataframe, validation_dataframe = DataPreparation().train_test_split(DATA_dataframe,TrainFraction,BS,SAMPLING_SCHEME)


----------------------------------------------------

