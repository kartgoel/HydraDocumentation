DataPreprocessing
======================

This file includes the ``DataPreparation`` class, which provides methods to split the data into train and test sets for machine learning tasks.


train_test_split
-----------------

This method splits the data into train and test sets. 
It can perform label balancing based on the number of bad examples. 

.. code-block:: python

    def train_test_split(self, all_df,trainamt,BS,type="normal"):
        train_df, test_df = train_test_split(all_df, test_size=1.-trainamt,random_state=24)

        #loop and find max number of label
        train_df_label_count = train_df.groupby('label').count()
        

        if type == "normal":
            return train_df, test_df
        elif type=="undersample" or type=="subsample":
            ncat_bal = train_df[train_df.label == "Bad"].shape[0]
        elif type=="oversample" or type=="supersample":
            ncat_bal=max(train_df_label_count['img'])
		# Split train to train and validation datasets
		#train_df, val_df = train_test_split(train_df, test_size=0.1, random_state=24)
		
		# ncat_bal = train_df['label'].value_counts().max()           
                          # Find number of samples that has label as bad
        print("Number of samples in training set labeled bad: ", ncat_bal)
        ncat_bal = math.ceil(ncat_bal/BS)*BS                        #Make even multiple of batchsize
        print("Resetting number of bad samples to: ", ncat_bal)
        train_df = train_df.groupby('label', as_index=False).apply(lambda g:  g.sample(ncat_bal, replace=True, random_state=24)).reset_index(drop=True)
        return train_df, test_df


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




