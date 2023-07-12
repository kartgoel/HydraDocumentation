hydra_train
======================

This file trains Hydra models based on GPU availability.
It prepares the data by normalizing pixel values and loads the models on available GPUs.
The loss of training and validation accuracy are used to evaluate training. 

removeLabelfromDataset
-----------------------

This method removes a given label from a given dataset.

.. code-block:: python

    def removeLabelfromDataset(dataset, label):
    for index, row in dataset.iterrows():
        if row['label'] == label:
            dataset.drop(index, inplace=True)
    return dataset

Parameters
~~~~~~~~~~~

- ``dataset``: A Pandas DataFrame representing the rows from which labels need to be removed.
- ``label``: A string representing the label that needs to be removed from the data set.

-------------------

moveDataAllButOne
-------------------

This method moves data from an input location to an output location excluding a given label.

.. code-block:: python

    def moveDataAllButOne(from_dataset,to_dataset,label):
        
        foundFirst = False
        for index, row in from_dataset.iterrows():
            if row['label'] == label and not foundFirst:
                foundFirst == True
            elif row['label'] == label and foundFirst:
                to_dataset=to_dataset.append(row, ignore_index=True)
                from_dataset.drop(index, inplace=True)
        return from_dataset,to_dataset


Parameters
~~~~~~~~~~~

- ``from_dataset``: A Pandas DataFrame representing the input location of the data.
- ``to_dataset``: A Pandas DataFrame representing the output location of the data.
- ``label``: A string representing the label to avoid moving.

----------------------

moveDataOne
--------------------

This method moves data from an input location to an output location that matches a given label.

.. code-block:: python

    def moveDataOne(from_dataset,to_dataset,label):
        foundFirst = False
        for index, row in from_dataset.iterrows():
            if row['label'] == label and not foundFirst:
                foundFirst == True
                to_dataset=to_dataset.append(row, ignore_index=True)
                from_dataset.drop(index, inplace=True)
                break
        return from_dataset,to_dataset
  
Parameters
~~~~~~~~~~~

- ``from_dataset``: A Pandas DataFrame representing the input location of the data.
- ``to_dataset``: A Pandas DataFrame representing the output location of the data.
- ``label``: A string representing the label to move.
