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

--------------------

printSampleCounts
-----------------

This method prints the respective samples in the given dataframes.


.. code-block:: python

    def printSampleCounts(plotClassifications, training_dataframe, validation_dataframe, test_dataframe=None):
        if test_dataframe != None:
            print("Class | Train | Valid | Test")
        else:
            print("Class | Train | Valid")

        for Class in plotClassifications:
            className = Class["Classification"]
            trainCount = training_dataframe.loc[training_dataframe.label == className].shape[0]
            validCount = validation_dataframe.loc[validation_dataframe.label == className].shape[0]
            row=className+"  |  "+str(trainCount)+" ("+str(float(trainCount)/float(training_dataframe.shape[0]))+")  |  "+str(validCount)+" ("+str(float(validCount)/validation_dataframe.shape[0])+")"
            if test_dataframe != None:
                testCount = test_dataframe.loc[test_dataframe.label == className].shape[0]
                row+" | "+str(testCount)+" ("+str(float(testCount)/test_dataframe.shape[0])+")"
            print(row)
            # logging.info(row)
            if validCount == 0:
                print("Missing example for "+str(className)+" exiting")
                # logging.error("Missing example for "+str(className)+" exiting")

Parameters
~~~~~~~~~~~~

- ``plotClassifications``: A list representing the classifications of the plots
- ``training_dataframe``: A Pandas DataFrame of the training data
- ``validation_dataframe``: A Pandas DataFrame of the validation data
- ``test_dataframe``: An optional dataframe of the test data

---------------

getGenerator
------------

This method returns data generators for the validation, training, and testing datasets.
The pixels are normalized and the generator is configured to respective settings.
If a testing dataframe is unavailable, the validation dataframe is used to predict a possible dataframe.

.. code-block:: python

    # Extended code available on Github
    def getGenerator(training_dataframe, validation_dataframe, test_dataframe=None, BS=32):

Parameters
~~~~~~~~~~~~~

- ``training_dataframe``: A Pandas DataFrame of the training data
- ``validation_dataframe``: A Pandas DataFrame of the validation data
- ``test_dataframe``: An optional dataframe of the test data
- ``BS``: The generators' batch size. Defaults to 32.


