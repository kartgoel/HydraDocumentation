helpers
============



setTFConfig
--------------

This method configures the TensorFlow library settings along with configuring GPU settings.

.. code-block:: python
    def setTFConfig():
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        config.gpu_options.per_process_gpu_memory_fraction = 0.9
        tf.compat.v1.Session(config=config)

printSampleCounts
-----------------

This method prints the respective samples in the given data frames.


.. code-block:: python

    def printSampleCounts(plotClassifications, training_dataframe, validation_dataframe, test_dataframe=None):

Parameters
~~~~~~~~~~~~

- ''plotClassifications'': A list representing the classifications of the plots
- ''training_dataframe'': The dataframe of the training data
- ''validation_dataframe'': The dataframe of the validation data
- ''test_dataframe '': An optional data frame of the test data

getGenerator
------------

This method returns data generators for the validation, training, and testing datasets.
The pixels are normalized and the generator is configured to respective settings.
If a testing dataframe is unavailable, the validation dataframe is used to predict a possible dataframe.

.. code-block:: python

    def getGenerator(training_dataframe, validation_dataframe, test_dataframe=None, BS=32):

Parameters
~~~~~~~~~~~~~

- ''training_dataframe'': The dataframe of the training data
- ''validation_dataframe'': The dataframe of the validation data
- ''test_dataframe '': An optional data frame of the test data
- ''BS'': The generators' batch size which has a default value of 32.


