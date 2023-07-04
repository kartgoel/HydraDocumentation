model_analysis
======================

This file validates and evaluates the AI models by using confusion matrixes and adding their results to the data base.

.. code-block:: python 

    def main(argv):

     global dbhost
     global dbuser
     global dbname
     global dbcnx
     global dbcursor
     

     ap = argparse.ArgumentParser()
     ap.add_argument("-M", "--model", required=True,
     help="model ID to analyze")
     ap.add_argument("-r", "--report", required=False,
     help="report to analyze")
     ap.add_argument("-s", "--scaling", required=False,action="store_true",
     help="confusion matrix scaled")
     ap.add_argument("-I", "--inference", required=False,action="store_true",
     help="run inference on all plots and record")
     ap.add_argument("-c", "--config", required=True,
     help="path to hydra config file")
     ap.add_argument("-u","--update_thresholds",required=False,action="store_true",help="update thresholds for model")
     args = vars(ap.parse_args())
     doScaling=args["scaling"]
     do_threshold_update=args["update_thresholds"]

     configPath = args["config"]
     RunNumber_padding=6
     try:
          with open(configPath) as parms_json:
               parms=json.load(parms_json)

          dbhost=parms["DB_CONNECTION"]["Host"]
          dbuser=parms["DB_CONNECTION"]["User"]
          dbname=parms["DB_CONNECTION"]["DB"]
          RunNumber_padding=len(parms["TRAINING_PARAMS"]["RUN_NUMBER_FORM"])
          
     except Exception as e:
          print(e)
          exit(1)
        
     try:
          print("CONNECTING to "+dbhost+":"+dbname)
          dbcnx=MySQLdb.connect(host=dbhost, user=dbuser, db=dbname)
          dbcursor=dbcnx.cursor(MySQLdb.cursors.DictCursor)
     except:
          print("ERROR: CANNOT CONNECT TO DATABASE")
          exit(1)

     print("CONNECTED to "+dbhost+":"+dbname)

     DBConnector = connector.DBManager(configPath)
     modelInstance = Model(DBConnector, modelID=args["model"]) 
     print("model Instance",modelInstance.model)

     if(modelInstance.model == None):
          print("ERROR: model failed to be loaded")
          errorhtml="<html><body><h1>ERROR: model failed to be loaded during analysis likely due to missing model files and/or versioning issues</h1></body></html>"
          errorsql="update Models Set ConfusionMtx='"+errorhtml+"' where ID="+str(args["model"])+";"
          DBConnector.Update(errorsql)
          exit(1)

     model_line=DBConnector.FetchAll("SELECT * from Models where ID="+str(args["model"]))[0]
     differences_list=[]
     if(args["inference"]):
          DoInference(modelInstance,model_line,DBConnector,RunNumber_padding)

     if(args["report"]):
          
          with open(args["report"]) as report_json:
               json_report=json.load(report_json)
          
          for datum in json_report['DATA']:
               RunPeriod=datum['inDATA'].split("//")[1].split("/")[0]
               RunNumber=int(datum['inDATA'].split("/")[-2].split("Run")[1])
               chunkNum=0
               if(datum['inDATA'].split("/")[-1].split(".")[0].split("_")[-1].isnumeric()):
                    chunkNum=datum['inDATA'].split("/")[-1].split(".")[0].split("_")[-1]

               getPlotID_q="SELECT ID FROM Plots where Plot_Types_ID="+args["model"]+" && RunPeriod=\""+RunPeriod+"\" && RunNumber="+str(RunNumber)+" && Chunk="+str(chunkNum)
               dbcursor.execute(getPlotID_q)
               Plot_ID= dbcursor.fetchall()[0]['ID']
               getUserClass_q="SELECT Classification from Plot_Classifications where ID in (SELECT Plot_Classification_ID from Users_Plots where Plot_ID="+str(Plot_ID)+")"
               dbcursor.execute(getUserClass_q)
               Plot_Classification_return= dbcursor.fetchall()
               if(len(Plot_Classification_return)!=1):
                    continue

               Plot_Classification=Plot_Classification_return[0]['Classification']

               if(Plot_Classification != datum['Verdict']):
                    differences_list.append({"UClass":Plot_Classification,"AIClass":datum['Verdict'],"Confidence": datum["VerdictConfidence"],"RunPeriod":RunPeriod,"RunNumber":str(RunNumber),"Name":datum['inDATA'].split("/")[-1].split(".")[-1],"FileType":datum['inDATA'].split(".")[-1]})

     
     print(differences_list)
     print(model_line)
     
     LookAtDifferences(model_line["ID"],differences_list,RunNumber_padding)
     #ViewAll(model_line["ID"])
     #MakeConfusionMatrix(model_line["ID"],model_line["Labels"],doScaling)#DEPRECATED!
     valid_labels_q="SELECT pc.Classification FROM Models m JOIN Valid_Classifications vc ON m.PlotType_ID = vc.Plot_Types_ID JOIN Plot_Classifications pc ON vc.Plot_Classifications_ID = pc.ID WHERE pc.Classification != 'Ignore' && m.ID ="+str(model_line["ID"])
     valid_labels_r=DBConnector.FetchAll(valid_labels_q)

     valid_labels=[]
     for r in valid_labels_r:
          valid_labels.append(r["Classification"])

     test = MakeConfidenceDistributionMatrix(model_line["ID"],valid_labels)
     print(valid_labels)
     results = DoThresholdOptimization(test[0],valid_labels)

     for l in valid_labels:
          f1_scores = []
          for threshold in results:
               if l in results[threshold]:
                    f1_scores.append((threshold, results[threshold][l]["f1_score"]))
          
          max_f1=-1
          optimal_threshold=-1
          f1_scores=f1_scores[::-1]
          for s in f1_scores:
               if(s[1]>max_f1):
                    max_f1=s[1]
                    optimal_threshold=s[0]

          if optimal_threshold == 1.0:
               optimal_threshold=0.99
          
          modelID=model_line["ID"]
          Plot_Classification_ID=DBConnector.FetchAll("SELECT ID FROM Plot_Classifications where Classification=\""+l+"\"")[0]["ID"]
          
          print("Optimal",l,Plot_Classification_ID,"Threshold:", optimal_threshold)
          if do_threshold_update:
               update_q="UPDATE ModelThresholds SET Threshold="+str(optimal_threshold)+", ThresholdMethod='max_f1' WHERE Model_ID="+str(modelID)+" && Plot_Classification_ID="+str(Plot_Classification_ID)+";"
               DBConnector.Update(update_q)
     
     #MakeDanielConfidenceDistributionMatrix(model_line["ID"],model_line["Labels"])
     return

-------------------

LookAtDifference
~~~~~~~~~~~~~~~~~~~~~


This function compares the plot analysis accuracy of various trained models. 

.. code-block:: python 

    def LookAtDifferences(id,difference_list,zpad):
     
     differences_list=difference_list

     if(len(difference_list)==0):
     
          differences_list_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID=Plot_Types.ID WHERE Users_Plots.Plot_Classification_ID != AIP.Plot_Classification_ID AND Users_Plots.Plot_Classification_ID != 6 AND AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber ASC;"
          dbcursor.execute(differences_list_q)
          differences_list= dbcursor.fetchall()

     list_length=len(differences_list)

     AI_plots_q="SELECT Count(*) from AI_Plots where Model_ID="+str(id)+";"
     dbcursor.execute(AI_plots_q)
     AI_plots=dbcursor.fetchone()
     AI_plots_count=AI_plots["Count(*)"]

     if(AI_plots_count==0):
          print("no inference run for this model")
          print("rerun with -I flag to run inference")
          exit(1)
     print("AI plots count:", AI_plots_count)
     print("difference list length:", list_length)
     
     if list_length==0:
          print("100% accurate!!")
          return

     print("           name                "+"  |  "+"Expert label"+" v "+"AI label"+" @ "+"AI confidence")
     for row in differences_list:
          print(row["RunPeriod"]+str(row["RunNumber"]).zfill(zpad)+"/"+str(row["Name"])+"_"+str(row['Chunk']).zfill(4)+"  |  "+row["UClass"]+" v "+row["AIClass"]+" @ "+str(row["Confidence"]))
     

----------------------

ViewAll
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function retrieves all of the plots for one trained model. 

*Note: This function has been commented out in the main argument.*

.. code-block:: python

    def ViewAll(id):
     differences_list_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID = Plot_Types.ID WHERE AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber desc;"
     print(differences_list_q)
     dbcursor.execute(differences_list_q)
     differences_list= dbcursor.fetchall()

     list_length=len(differences_list)

     i=0

     print(list_length)
     
     for row in differences_list:
          print(row["RunPeriod"]+"/"+str(row["RunNumber"])+"  |  "+row["UClass"]+" v "+row["AIClass"]+" @ "+str(row["Confidence"]))
     

-------------------------------

MakeConfusionMatrix
~~~~~~~~~~~~~~~~~~~~~~~~~

This function returns a 2D array confusion matrix along with a list of the labels given to the plots analyzed by the AI. 
*Note: This function has been commented out in the main argument.*

.. code-block:: python

    def MakeConfusionMatrix(id,labels,doScaling):
     getPlots_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID AND Users_Plots.Plot_Classification_ID != 6 INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID = Plot_Types.ID WHERE AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber ASC;"
     print(getPlots_q)
     dbcursor.execute(getPlots_q)
     Plots_list= dbcursor.fetchall()
     Labels_list=ast.literal_eval(str(labels,"utf-8"))
     Labels_from_indice=[]
     for lab in Labels_list.keys():
          Labels_from_indice.append(Labels_list[lab])
     invLabels_list={y:x for x,y in Labels_list.items()}
     print(len(Plots_list))
     
     data2d=[]
     for i in range(0,len(Labels_list)):
          row=[]
          for j in range(0,len(Labels_list)):
               row.append(0.)
          data2d.append(row)

     data_dataframe=pd.DataFrame(columns=["UClass","AIClass"])
     for entry in Plots_list:
          data2d[invLabels_list[entry["AIClass"]]][invLabels_list[entry["UClass"]]]+=1
          data_dataframe=data_dataframe.append({"UClass":entry["UClass"],"AIClass":entry["AIClass"]}, ignore_index=True)

     print(data_dataframe["UClass"])
     print(data2d)
     rowSums=[]

     for i in range(0,len(data2d)):
          row_sum=0.
          for j in range(0,len(data2d)):
               row_sum+=data2d[j][i]
          rowSums.append(row_sum)

     if(doScaling):
          for i in range(0,len(data2d)):
               for j in range(0,len(data2d)):
                    data2d[j][i]=data2d[j][i]/rowSums[i]

     print(data2d)
     fig = go.Figure(ff.create_annotated_heatmap(x=Labels_from_indice,y=Labels_from_indice,z=data2d,colorscale='Greys'     
          ))
     for i in range(len(fig.layout.annotations)):
          fig.layout.annotations[i].font.size = 24
     if(doScaling):
          fig = go.Figure(go.Heatmap(x=Labels_from_indice,y=Labels_from_indice,z=data2d,zmin=0,zmax=1,colorscale=[
               [0,"rgb(255,255,255)"],[1,"rgb(0,0,0)"]
          ]))
     print(Plots_list[0])
     fig.update_layout(
          title=go.layout.Title(
          text=Plots_list[0]["Name"]+" Confusion Matrix",
          xref="paper",
          x=0
          ),
          xaxis=go.layout.XAxis(
               title=go.layout.xaxis.Title(
               text="Truth",
               font=dict(
               family="Courier New, monospace",
               size=36,
               color="#7f7f7f"
               )
               ),tickfont=dict(
               family="Courier New, monospace",
               size=30,
               color="#7f7f7f"
               )
          ),
          yaxis=go.layout.YAxis(
               title=go.layout.yaxis.Title(
               text="AI",
               font=dict(
               family="Courier New, monospace",
               size=36,
               color="#7f7f7f"
               )
               ),tickfont=dict(
               family="Courier New, monospace",
               size=30,
               color="#7f7f7f"
               )
          )
     )
     fig.show()
     print(data2d)

-------------------------

MakeConfidenceDistributionMatrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function plots and displays the confusion matrix on a histogram based on the figure of a 2D array.

.. code-block:: python

    def MakeConfidenceDistributionMatrix(id,labels):
     getPlots_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID AND Users_Plots.Plot_Classification_ID != 6 INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID = Plot_Types.ID WHERE AIP.Model_ID ="+str(id)+" AND Users_Plots.Plot_Classification_ID != 6 ORDER BY Plots.RunNumber ASC;"
     print(getPlots_q)
     dbcursor.execute(getPlots_q)
     Plots_list= dbcursor.fetchall()
     Labels_list=labels\
     print("HOW MANY PLOTS?",len(Plots_list))

     data2d = {}
     for i in Labels_list:
          for j in Labels_list:
               data2d[(i, j)] = []


     print("empty data2d",data2d)
     for entry in Plots_list:
          key = (entry["AIClass"], entry["UClass"])
          data2d[key].append(entry["Confidence"])


     gridN=len(Labels_list)
     titles=()
     
     for i in Labels_list:
          for j in Labels_list:
               titles = titles + (str(len(data2d[(j, i)])),)

     plotdata=[]
   
     grid_figure = make_subplots(rows=gridN, cols=gridN, subplot_titles=titles)

     for i in grid_figure['layout']['annotations']:
          i['font'] = dict(size=30,color='#000000')

     for i in range(0,len(Labels_list)):
          for j in range(0,len(Labels_list)):
          
               minval=int(100*(1./gridN))/100.
               hist=go.Histogram(x=data2d[(Labels_list[i],Labels_list[j])], nbinsx=100) 
               grid_figure.add_trace(hist,col=i+1,row=j+1)
            
               grid_figure.update_xaxes(range=[0.0, 1.0], row=gridN-i,col=j+1)
               grid_figure.update_yaxes(type="log",row=gridN-i,col=j+1)

               if(gridN-i==gridN):
                    grid_figure.update_xaxes(title_font=dict(
                         family="Courier New, monospace",
                         size=30,
                         color="black",
                         ),title_text="AI "+Labels_list[j],range=[minval, 1.0],row=gridN-i,col=j+1)
            
               if(j+1==1):
                    grid_figure.update_yaxes(title_font=dict(
                         family="Courier New, monospace",
                         size=30,
                         color="black"
                         ),title_text=""+Labels_list[i],type="log",row=i+1,col=j+1)
     
     grid_figure.update_layout(
          title=go.layout.Title(
          text="Model "+str(id)+" - "+Plots_list[0]["Name"]+": AI Confidence Distributions"
          )
     )

     plotly.offline.plot(grid_figure,filename='Grid.html',image = 'png', image_filename='ConfusionMatrix')
     print("Confusion Matrix Made")
     Grid_string=plotly.io.to_html(grid_figure, full_html=True, include_plotlyjs='cdn')

     Grid_string=Grid_string.replace("'",'"') #replace single quotes with double quotes for mysql
     conf_mtx_q="update Models Set ConfusionMtx='"+Grid_string+"' where ID="+str(id)+";"

     dbcursor.execute(conf_mtx_q)
     dbcnx.commit()
     return data2d, Labels_list
     

--------------------------

DoThresholdOptimization
~~~~~~~~~~~~~~~~~~~~~~~~~

This function uses confidence levels to evaluate the model's precision, recall, and accuracy within a threshold. 

.. code-block:: python

    def DoThresholdOptimization(data2d, Labels_list):
     positive_label = "positive"
     negative_label = "negative"
     
     thresholds = [i/100 for i in range(101)]
     results = {}
     
     tp,fp, tn, fn =0,0,0,0 
     
     for threshold in thresholds:
          for i in range(len(Labels_list)):
               label = Labels_list[i]
               fp =0
               fp_count_less =0
               for j in range(len(Labels_list)):
                    confidences = data2d[(Labels_list[i],Labels_list[j])]
                    
                    #check thresholds true positive
                    if i == j:
                         relabeled_counts_tp = [positive_label if confidence >= threshold else negative_label for confidence in confidences]
                         tp_count_less = len([confidence for confidence in relabeled_counts_tp if confidence == negative_label])
                         tp = len([confidence for confidence in relabeled_counts_tp if confidence == positive_label])
                    # check other entries in column
                    else:
                         relabeled_counts_fp = [positive_label if confidence >= threshold else negative_label for confidence in confidences]
                         fp_count_less += len([confidence for confidence in relabeled_counts_fp if confidence == negative_label])
                         fp += len([confidence for confidence in relabeled_counts_fp if confidence == positive_label ])

               tn = sum([len(data2d[(Labels_list[j],Labels_list[k])]) for j in range(len(Labels_list)) for k in range(len(Labels_list)) if j != i and k != i]) + fp_count_less
               fn = sum([len(data2d[(Labels_list[j],Labels_list[i])]) for j in range(len(Labels_list)) if j != i]) + tp_count_less

               
               #calculate precision, accuracy, and recall
               precision = tp / (tp + fp) if (tp + fp) > 0 else 0
               accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
               recall = tp / (tp + fn) if (tp + fn) > 0 else 0
               f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
               
               # Store the results in the dictionary
               if threshold not in results:
                    results[threshold] = {}
               results[threshold][label] = {
               "TP": tp,
               "FP": fp,
               "TN": tn,
               "FN": fn,
               "precision": precision,
               "accuracy": accuracy,
               "recall": recall,
               "f1_score": f1_score
               }
               
               
     #plot things using plotly
     # what we want to plot
     evaluation_metrics = ["precision", "recall", "accuracy", "f1_score"]
     # Create a subplot for each evaluation metric
     fig = make_subplots(rows=len(evaluation_metrics), cols=1, subplot_titles=evaluation_metrics)

     # Loop through each evaluation metric and add a trace for each label
     for i, metric in enumerate(evaluation_metrics):
          for label in results[threshold]:
               metric_data = []
               threshold_data = []
               for threshold in results:
                    metric_data.append(results[threshold][label][metric])
                    threshold_data.append(threshold)
        
               # Add a scatter trace to the subplot for the current label
               fig.add_trace(go.Scatter(x=threshold_data, y=metric_data, name=label), row=i+1, col=1)
    
     # Set the subplot title and axis labels
     fig.update_yaxes(title_text=metric, row=i+1, col=1)
     fig.update_xaxes(title_text="Threshold", row=i+1, col=1)

     # Update the layout and show the plot
     fig.update_layout(title="Evaluation Metrics vs. Threshold",
                  height=800, width=800)

     # Save the plot as a PNG image in the current directory
     pio.write_image(fig, "./evaluation_metrics.png")
     
     return results
     

------------------

MakeDanielConfigurationDistributionMatrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function is a tool for developers to see what plots are being excluded from the confusion matrix.

*Note: This function has been commented out in the main argument.*

.. code-block:: python

    def MakeDanielConfidenceDistributionMatrix(id,labels):
     getPlots_q="SELECT Plot_Classifications.Classification AS UClass, AIClasses.Classification AS AIClass, AIP.Confidence, Plots.RunPeriod, Plots.RunNumber, Plot_Types.Name, Plot_Types.FileType FROM AI_Plots_Top_Classification_View AIP LEFT JOIN Users_Plots ON Users_Plots.Plot_ID = AIP.Plot_ID INNER JOIN Plot_Classifications ON Users_Plots.Plot_Classification_ID = Plot_Classifications.ID INNER JOIN Plot_Classifications AIClasses ON AIP.Plot_Classification_ID = AIClasses.ID INNER JOIN Plots ON Plots.ID = AIP.Plot_ID INNER JOIN Plot_Types ON Plots.Plot_Types_ID = Plot_Types.ID WHERE AIP.Model_ID ="+str(id)+" ORDER BY Plots.RunNumber ASC;"
     print(getPlots_q)
     dbcursor.execute(getPlots_q)
     Plots_list= dbcursor.fetchall()
     print(labels)
     Labels_list=ast.literal_eval(str(labels,"utf-8"))
     print(Labels_list)
     Labels_from_indice=[]
     for lab in Labels_list.keys():
          Labels_from_indice.append(Labels_list[lab])
     invLabels_list={y:x for x,y in Labels_list.items()}
     print(len(Plots_list))
    
     data2d=[]
     for i in range(0,len(Labels_list)):
          row=[]
          for j in range(0,len(Labels_list)):
               row.append([])
          data2d.append(row)

     for entry in Plots_list:
          data2d[invLabels_list[entry["AIClass"]]][invLabels_list[entry["UClass"]]].append(entry["Confidence"])

     gridN=len(Labels_list)
     titles=()
     for i in range(0,len(Labels_list)):
          for j in range(0,len(Labels_list)):
               titles = titles + (str(len(data2d[gridN-i-1][j])),)
    

     plotdata=[]
   
     grid_figure = make_subplots(rows=gridN, cols=gridN, subplot_titles=titles)

     for i in grid_figure['layout']['annotations']:
          i['font'] = dict(size=30,color='#000000')

     for i in range(0,len(Labels_list)):
          for j in range(0,len(Labels_list)):
               print("================================")
               print("AI: "+str(Labels_list[i])+"_Truth: "+str(Labels_list[j]))
               nbins=10
               binned_count=[]
               for k in range(0,nbins):
                    binned_count.append(0.)
               
               for point in data2d[i][j]:
                    bin_index=math.floor(point*nbins)-1
                    binned_count[bin_index]=binned_count[bin_index]+1.0
               
               for l in range(0,nbins):
                    if len(data2d[i][j]) != 0.:
                         binned_count[l]=binned_count[l]/float(len(data2d[i][j]))
               print(binned_count)
               print(len(data2d[i][j]))

-------------------------------

DoInference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This function reaches a conclusion about the model's performance using the validation generator and inserts results into the database.

.. code-block:: python

    def DoInference(modelInstance,model_line,DBConnector,RunNumber_padding):
     All_data_q="SELECT Plot_Types.Name, Plot_Types.IsChunked, Plot_Types.FileType, Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plots.TrainingWeight, Plot_Classifications.Classification FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id inner join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.ID = "+str(model_line["PlotType_ID"])+" && Plot_Classifications.Classification != \'Ignore\' and (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id) ORDER BY Plots.RunNumber asc"
     print(All_data_q)
     All_img=DBConnector.FetchAll(All_data_q)
     print("how many images of ID",str(model_line["PlotType_ID"]),"?",len(All_img))
     if(model_line["MergedTrain"]):
          other_ID_q="SELECT ID from Plot_Types where Name in (Select Name from Plot_Types where ID="+str(model_line["PlotType_ID"])+");"
          other_ID=DBConnector.FetchAll(other_ID_q)
          for other in other_ID:
               if(other["ID"] != model_line["PlotType_ID"]):
                    All_odata_q="SELECT Plot_Types.Name, Plot_Types.IsChunked, Plot_Types.FileType, Plots.RunPeriod, Plots.RunNumber, Plots.Chunk, Plots.TrainingWeight, Plot_Classifications.Classification FROM Plots inner join Plot_Types on Plot_Types.id = Plots.Plot_types_id inner join Users_Plots on Users_Plots.plot_id = Plots.id left join Plot_Classifications on Plot_Classifications.id = Users_Plots.Plot_classification_id where Plot_Types.ID = "+str(other["ID"])+" && Plot_Classifications.Classification != \'Ignore\' and (Users_Plots.id) = (select max(Users_Plots2.id) from Users_Plots Users_Plots2 where Users_Plots2.plot_id = Plots.id) ORDER BY Plots.RunNumber asc"
                    print(All_odata_q)
                    All_other_img=DBConnector.FetchAll(All_odata_q)
                    print("how many images of ID",str(model_line["PlotType_ID"]),"?",len(All_other_img))
                    All_img=All_img+All_other_img

     print("how many images in total?",len(All_img))
     plot_is_chunked=False
     
     DATA_dataframe=pd.DataFrame(columns=["img","label"])
     for datum in All_img:
          if datum["RunNumber"] != 0:
               location=datum["RunPeriod"]+str(datum["RunNumber"]).zfill(RunNumber_padding)+"/"+datum["Name"]
               if(datum["IsChunked"] == 1):
                    plot_is_chunked=True
               
               
                    location=location+"_"+str(datum["Chunk"]).zfill(4)
               location=location+"."+datum["FileType"]
          else:
            location=datum["RunPeriod"]+"."+datum["FileType"]

          
          DATA_dataframe=DATA_dataframe.append({"img":location,"label":datum["Classification"]}, ignore_index=True)
     

     for i in range(0,10):
          print(DATA_dataframe.iloc[i]["img"])

     imgheight=ast.literal_eval(model_line["InputShape"])[0]
     imgwidth=ast.literal_eval(model_line["InputShape"])[1]
     valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
     validation_generator=valid_datagen.flow_from_dataframe( 
               dataframe=DATA_dataframe, 
               directory=None, 
               x_col="img", y_col="label", 
               class_mode="categorical", 
               target_size=(imgheight,imgwidth),
               color_mode="rgb",
               batch_size=1,
               shuffle=False,
               seed=42)

     labels=ast.literal_eval(str(model_line["Labels"],"utf-8"))
     
     preds=modelInstance.model.predict_generator(validation_generator,verbose=1,steps=validation_generator.n)
     print("recording",len(preds),"predictions")
     for pred in range(0,len(preds)):
          print("recording prediction",pred,"of",len(preds),"predictions")
          datum=DATA_dataframe.iloc[pred]['img']
          chunknum=0
          if(datum.split("_")[-1].split(".")[0].isnumeric()):
               chunknum=datum.split("_")[-1].split(".")[0]
          else:
               chunknum=0
               plot_is_chunked=False

          chunk_str="NULL"
          if(plot_is_chunked):
               chunk_str="NOT NULL"

          ptype=datum.split(".")[1]
          ppath=datum.split("/")
          pname=ppath[-1].split(".")[0]
          ploc="/".join(ppath[:-2])
          prunnum=int(ppath[-2].replace("Run",""))

          if(plot_is_chunked):
               pname="_".join(pname.split("_")[:-1])

          Plot_ID_q="SELECT ID FROM Plot_Types WHERE FileType = \'"+ptype+"\'"+" && Name = \'"+pname+"\'"+" && IsChunked is "+chunk_str
          print("plot_ID_q:",Plot_ID_q)

          Plot_IDr=DBConnector.FetchAll(Plot_ID_q)
          print("Plot_ID_qr:",Plot_IDr)

          if(len(Plot_IDr) != 1):
               print("ambiguous plot type ID")
               return

          Plot_Type_ID=Plot_IDr[0]["ID"]

          plots_ID_q="SELECT ID FROM Plots WHERE RunNumber = "+str(prunnum)+" && Plot_types_id = "+str(Plot_Type_ID)+" && Chunk = "+str(chunknum)
          plots_ID_r=DBConnector.FetchAll(plots_ID_q)

          
          if(len(plots_ID_r) != 1):
               print("ambiguous plot ID")
               return

          Plot_ID=plots_ID_r[0]["ID"]

          for p in range(0,len(preds[pred])):
               Classification_line_q="SELECT * from Plot_Classifications where Classification = \'"+labels[p]+"\'"
               Classification_line_r=DBConnector.FetchAll(Classification_line_q)
               if(len(Classification_line_r) != 1):
                    print("ambiguous classification")
                    return
               Classification_line=Classification_line_r[0]
               Classification_type_ID=Classification_line["Classification_Type_ID"]
               Classification_ID=Classification_line["ID"]

               AIplots_q="SELECT ID from AI_Plots WHERE Model_ID = "+str(model_line["ID"])+" && Plot_ID = "+str(Plot_ID)+" && Plot_Classification_ID = "+str(Classification_ID)+" && Classification_Type_ID = "+str(Classification_type_ID)
               AIplots_r=DBConnector.FetchAll(AIplots_q)
               if(len(AIplots_r) == 0):
                    AI_plot_insert_q="INSERT INTO AI_Plots (Model_ID,Plot_ID,Plot_Classification_ID,Classification_Type_ID,Confidence) VALUES ("+str(model_line["ID"])+","+str(Plot_ID)+","+str(Classification_ID)+","+str(Classification_type_ID)+","+str(preds[pred][p])+")"

                    DBConnector.Update(AI_plot_insert_q)



