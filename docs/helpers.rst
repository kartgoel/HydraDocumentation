Helpers
===================

This file provides several functions to prepare data and create data generators for training, validation, and test datasets. 

------------------

setTFConfig
~~~~~~~~~~~~~~~~~~~

This function delegates an appropriate amount of tasks to GPU and assigns memory space. 

.. code-block:: python 

    def setTFConfig():
        config = tf.compat.v1.ConfigProto()
        # Don't pre-allocate memory; allocate as-needed
        config.gpu_options.allow_growth = True
        # Only allow a total of half the GPU memory to be allocated
        config.gpu_options.per_process_gpu_memory_fraction = 0.9
        tf.compat.v1.Session(config=config)

-----------------------------

printSampleCounts
~~~~~~~~~~~~~~~~~~~~

This function outputs training, validation, and testing counts. 

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
            if validCount == 0:
                print("Missing example for "+str(className)+" exiting")
                exit(1)

--------------------------------

getGenerator 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function creates the training, validation, and testing generators. 

.. code-block:: python 

    def getGenerator(training_dataframe, validation_dataframe, test_dataframe=None, BS=32):
   
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

        imgshape=cv2.imread(str(training_dataframe.iloc[0]["img"])).shape
        imgheight=imgshape[0]
        imgwidth=imgshape[1] 

        train_generator=train_datagen.flow_from_dataframe(
            dataframe=training_dataframe, 
            directory=None, 
            x_col="img", y_col="label", 
            class_mode="categorical", 
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=BS,
            shuffle=True,
            seed=42)

        validation_generator=valid_datagen.flow_from_dataframe( 
            dataframe=validation_dataframe, 
            directory=None, 
            x_col="img", y_col="label", 
            class_mode="categorical", 
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=1,
            shuffle=True,
            seed=42)
        
        if test_dataframe == None:
            to_pred=pd.DataFrame(columns=["plot"])
            for f in validation_generator.filenames:
                to_pred=to_pred.append({"plot":f}, ignore_index=True)
            test_dataframe = to_pred

        test_generator = test_datagen.flow_from_dataframe(
        dataframe=test_dataframe,
            directory=None,
            x_col="plot",
            target_size=(imgheight,imgwidth),
            color_mode="rgb",
            batch_size=1,
            class_mode=None,
            shuffle=False
        )
        test_generator.reset()

        return train_generator, validation_generator, test_generator
