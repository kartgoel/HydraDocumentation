Hydra Docs
=========

.. image:: img/hydra_logo.png
  :alt: Hydra


.. image:: img/white_space.png
   :alt: Space


Welcome to Hydra's documentation! **Hydra** is an extensible framework for training, managing and 
deploying machine learning models for real time data quality monitoring.

Check out the Github for further information.

.. grid:: 2

   .. grid-item-card:: HTML Scripts
      :link: docs/labeler.rst
      :link-type: doc

      All the webpages visible to the user on the front end of Hydra.

   .. grid-item-card:: HTML Integrations
      :link: docs/populateSelectors.rst
      :link-type: doc

      These scripts responsible for integrating Hydra backend with the frontend.


.. grid:: 2

   .. grid-item-card:: HTML Utils
      :link: docs/help.rst
      :link-type: doc

      The formatting of different html elements on the Hydra webpages.

   .. grid-item-card:: Hydra libraries
      :link: docs/connectToDB.rst
      :link-type: doc

      These libraries are responsible for helping Hydra's backend operate. 

.. grid:: 2

   .. grid-item-card:: Hydra Scripts
      :link: docs/schemaSync.rst
      :link-type: doc

      These scripts run the main backend processes of Hydra.

   .. grid-item-card:: Hydra Utils
      :link: docs/dependencies.rst
      :link-type: doc

      These utils are used throughout Hydra's backend for connections to standard libraries and the database.

.. note::

   This project is under active development.


.. toctree::
   :hidden:
   :caption: 🧑User Interface

   labelerFE


.. toctree::
   :hidden:
   :caption: 📄HTML Pages

   labeler
   library
   hydraRun


.. toctree::
   :hidden:
   :caption: 🤖HTML Integrations

   populateSelectors
   getLeaderBoard
   login


.. toctree::
   :hidden:
   :caption: 🖥️HTML Utils

   help
   label


.. toctree::
   :hidden:
   :caption: 📚Hydra Libraries
   
   connectToDB
   aiReport
   dataPreprocessing
   inferenceEngine
   gradcam


.. toctree::
   :hidden:
   :caption: 📝Hydra Scripts  

   schemaSync
   startHydra
   hydraTrain
   hydraCleaner
   hydraFeeder
   hydraPredict
   hydraKeeper
   helpers
   imgCrawler
   runGradCAM
   modelAnalysis
   assignTrainWeights
   simulateRunTime
   test

.. toctree::
   :hidden:
   :caption: 🔧Hydra Utils

   dependencies
   databaseConfig
   establishingDBConnection

