DataPreprocessing
======================

This library retrieves labels and correlates them with the plots. 

.. code-block:: python 

    class DataPreparation:
    """Train and Test Data

    Attributes
    -----------
    
    Methods
    -------
  
    """

    def train_test_split(self, all_df,trainamt,BS,type="normal"):
        """Balanced split to train, test and val sets.

        Label balancing is done based on number of bad examples.

        Parameters
        --------------------
        all_df : Pandas DataFrame, required
            DataFrame containing all the available data that can be split into train, test and validation sets

        trainamt : Float (0-1), required
            Fraction of the data to be used as training data
        
        BS: int, required
            Batch size


		"""
		
        

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
          
                          # Find number of samples that has label as bad
        print("Number of samples in training set labeled bad: ", ncat_bal)
        ncat_bal = math.ceil(ncat_bal/BS)*BS                        #Make even multiple of batchsize
        print("Resetting number of bad samples to: ", ncat_bal)
        train_df = train_df.groupby('label', as_index=False).apply(lambda g:  g.sample(ncat_bal, replace=True, random_state=24)).reset_index(drop=True)
        return train_df, test_df