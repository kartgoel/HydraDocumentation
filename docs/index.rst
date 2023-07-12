.. image:: img/hydra_logo.png
  :alt: Hydra


Welcome to Hydra's documentation! **Hydra** is an extensible framework for training, managing and 
deploying machine learning models for real time data quality monitoring.

Check out the Github for further information.

.. grid:: 1

   .. grid-item-card:: User Interface
      :link: userInterface/labelerFE
      :link-type: doc
      :text-align: center

      How to interact with Hydra's web-based pages. 

.. grid:: 2

   .. grid-item-card:: HTML Pages
      :link: htmlPages/labeler
      :link-type: doc

      The backend of Hydra's webpages.


   .. grid-item-card:: HTML Integrations
      :link: htmlIntegrations/getClassification
      :link-type: doc
       
      The link between Hydra's backend and frontend.  

.. grid:: 2

   .. grid-item-card:: HTML Utils
      :link: htmlUtils/help
      :link-type: doc
       
      Background scripts for the frontend of Hydra.

   .. grid-item-card:: Hydra Libraries
      :link: hydraLibraries/connectToDB
      :link-type: doc
      

      Background scripts for the backend of Hydra.

.. grid:: 2 

   .. grid-item-card:: Hydra Scripts
      :link: hydraScripts/schemaSync
      :link-type: doc
       
      The main scripts that run Hydra. 

   .. grid-item-card:: Hydra Utils
      :link: hydraUtils/dependencies
      :link-type: doc
      
      Different dependencies, configurations, and connections that Hydra uses. 


      



.. note::

   This project is under active development.


.. toctree::
   :hidden:
   :caption: 🧑User Interface

   userInterface/labelerFE
   userInterface/libraryFE
   userInterface/hydraRunFE

.. toctree::
   :hidden:
   :caption: 📄HTML Pages

   htmlPages/labeler
   htmlPages/library
   htmlPages/hydraRun
   htmlPages/hydraRunHelp


.. toctree::
   :hidden:
   :caption: 🤖HTML Integrations

   htmlIntegrations/getClassification
   htmlIntegrations/getLeaderBoard
   htmlIntegrations/getLog
   htmlIntegrations/getModelsInfo
   htmlIntegrations/getModels
   htmlIntegrations/getPlotTypes
   htmlIntegrations/getImages
   htmlIntegrations/libraryUtils
   htmlIntegrations/login
   htmlIntegrations/pollRunTime
   htmlIntegrations/populateSelectors  
   htmlIntegrations/recordLabels
   htmlIntegrations/subNewPlot


.. toctree::
   :hidden:
   :caption: 🖥️HTML Utils

   htmlUtils/help
   htmlUtils/label
   htmlUtils/executeQuery&Database
   htmlUtils/verifyExperiment


.. toctree::
   :hidden:
   :caption: 📚Hydra Libraries
   
   hydraLibraries/connectToDB
   hydraLibraries/aiReport
   hydraLibraries/dataPreprocessing
   hydraLibraries/inferenceEngine
   hydraLibraries/gradcam


.. toctree::
   :hidden:
   :caption: 📝Hydra Scripts  

   hydraScripts/schemaSync
   hydraScripts/startHydra
   hydraScripts/hydraTrain
   hydraScripts/hydraCleaner
   hydraScripts/hydraFeeder
   hydraScripts/hydraPredict
   hydraScripts/hydraKeeper
   hydraScripts/helpers
   hydraScripts/imgCrawler
   hydraScripts/runGradCAM
   hydraScripts/modelAnalysis
   hydraScripts/assignTrainWeights
   hydraScripts/simulateRunTime

.. toctree::
   :hidden:
   :caption: 🔧Hydra Utils

   hydraUtils/dependencies
   hydraUtils/databaseConfig
   hydraUtils/establishingDBConnection

