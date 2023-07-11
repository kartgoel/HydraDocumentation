.. _LibraryHTML:

Library
=========================

This HTML file creates Hydra's web-based library pages for the different JLab experiments. 

To learn about using the web-based library, see here: :ref:`libraryFE`

setExp
----------------

This function sets the experiment based on the current URL and updates the corresponding experiment logo. 

.. code-block:: html

            function setExp()
            {
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                document.getElementById("PT").value=urlParams.get('PT');
                cur_url=window.location.href
                //check if cur_url contains halldweb
                if(cur_url.includes("halldweb.jlab.org"))
                {
                    Experiment="GlueX"
                    document.getElementById("Explogo").src="./img/GlueX_logo.png"
                    document.getElementById("Explogo").style.width="100px"
                    document.getElementById("Explogo").style.height="auto"
                    document.getElementById("Explogo").style.marginTop="-16px"
                    document.getElementById("Explogo").style.marginLeft="11px"
                    document.getElementById("Explogo").style.marginRight="-16px"
                }
                else if(cur_url.includes("hallaweb.jlab.org"))
                {
                    Experiment="SBS"
                    document.getElementById("Explogo").src="./img/SBSlogo.png"
                    document.getElementById("Explogo").style.width="75px"
                    document.getElementById("Explogo").style.height="auto"
                    document.getElementById("Explogo").style.marginTop="-27px"
                    document.getElementById("Explogo").style.marginLeft="11px"
                    document.getElementById("Explogo").style.marginRight="-16px"
                }
                else if(cur_url.includes("clas"))
                {
                    Experiment="CLAS"
                    document.getElementById("Explogo").src="./img/CLASlogo.png"
                    document.getElementById("Explogo").style.width="75px"
                    document.getElementById("Explogo").style.height="auto"
                    document.getElementById("Explogo").style.marginTop="-20px"
                    document.getElementById("Explogo").style.marginLeft="11px"
                    document.getElementById("Explogo").style.marginRight="-16px"
                }
            }

Example Usage
~~~~~~~~~~~~~~

.. code-block:: html 

     $(document).ready(function(){setExp();Login();applyStyle();


----------------------------------------------------

.. _loginFuncLibrary:

Login
-------------

This function performs a login action for the user, sending an AJAX request to the server to verify the user and retrieve the permitted plots for the selected experiment. 

It also calls a php file, which can be found here: :ref:`loginphp`

.. code-block:: html

            function Login()
            {
            
                if (window.XMLHttpRequest) {
                        // code for IE7+, Firefox, Chrome, Opera, Safari
                        xmlhttp = new XMLHttpRequest();
                    } else {
                        // code for IE6, IE5
                        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                    }
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            //console.log(this.responseText)
                            if(this.responseText != "")
                            {
                                permitted_plots=JSON.parse(this.responseText)
                                populateSelector("Plot_Type");
                            }
                        }
                    };
                    
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/login.php?Experiment="+Experiment
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    $(document).ready(function(){setExp();Login();applyStyle();

-----------------------------------------

Initialize
-----------------

This function initializes the page by setting the selected plot type based on URL parameters. 

.. code-block:: html

            function Initialize()
            {
                if(Object.keys(urlvals).includes("PT"))
                {
                    PTsel=document.getElementById("Plot_Type");
                    name_to_select=urlvals["PT"];
                    if(urlvals["PT"].includes("Chunks"))
                    {
                        name_to_select=urlvals["PT"].replace(/Chunks/g,"")+" Chunks";
                    }
                    
                    //loop through select options and select the one that matches the name
                    for(var i=0;i<PTsel.options.length;i++)
                    {
                        if(PTsel.options[i].text==name_to_select)
                        {
                            PTsel.options[i].selected=true;
                            break
                        }
                    }
                }
                else
                {
                    document.getElementById("Plot_Type")[0].selected=true;
                }
                GetModels();
            }


-------------------------------------

getUrlVars
-------------

This function updates the corresponding unput elements on the page with parameter values. 

.. code-block:: html 

            function getUrlVars() {
                var vars = {};
                var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
                    vars[key] = value;
                });
                urlvals=vars;

                console.log(urlvals);
                for (var key in urlvals)
                {
                    var obj=document.getElementById(key);

                    if(obj)
                    {
                        obj.value=urlvals[key]
                    }
                    console.log(key);
                    console.log(urlvals[key])
                }
            }

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    $(document).ready(function(){getUrlVars();setExp();Login();


--------------------------------

.. _populateSelectorLibrary:

populateSelector
-------------

This function populates the selector element with options retrieved from a server-side script. 
It fetches the options data and create the corresponding HTML elements. 

It also calls a php file, which can be found here: :ref:`populateSelectors`


.. code-block:: html

    // Extended code found on GitHub
    function populateSelector(id,plotType="")

Parameters
~~~~~~~~~~~~~~~

- ``id``: A string representing the selector element to populate.
- ``plotType``: An optional string representing the selected plot type to pass to the server-side script. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    populateSelector("Palette-Holder",plot_type_selected)


------------------------------------------------------

.. _GetModelsLibrary:

GetModels
-------------

This function retrieves the models for the selected plot type. 

It also calls a php file, which can be found here: :ref:`GetModelsphp`


.. code-block:: html 

            function GetModels()
           {
            //get Plot_Type selected option
            var plotType=document.getElementById("Plot_Type").options[document.getElementById("Plot_Type").selectedIndex].text
            plotType=plotType.replace(" Chunks","_Chunks")



            if (window.XMLHttpRequest) {
                        // code for IE7+, Firefox, Chrome, Opera, Safari
                        xmlhttp = new XMLHttpRequest();
                    } else {
                        // code for IE6, IE5
                        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                    }
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            //console.log(this.responseText)
                            returned_info=[];
                            if(this.responseText != "")
                            {
                                returned_info=JSON.parse(this.responseText);
                                
                            }
                            MakeModelSelector(returned_info)
                            
                        }
                    };
                    
                     
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/getModels.php?Experiment="+Experiment+"&PT="+plotType
                    
                    console.log("==================")
                    console.log(php_call)
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
           }


--------------------------------

MakeModelSelector
-------------

This function creates the model selector dropdown on the page. 

.. code-block:: html 

    // Extended code on GitHub
    function MakeModelSelector(returned_info)

Parameter
~~~~~~~~~~~~~

- ``returned_info``: An object representign information about the available models. 


--------------------------------

.. _GetModelInfoLibrary:

GetModelInfo
-------------

This function retrieves information about the the selected model. 

It also calls a php file, which can be found here: :ref:`getModelInfophp`

.. code-block:: html 

           function GetModelInfo()
           {
            //get ModelSelector selected value
            if(document.getElementById("ModelSelector"))
            {
                var model_ID=document.getElementById("ModelSelector").options[document.getElementById("ModelSelector").selectedIndex].value;
                //get ModelSelector selected text
                var model_Name=document.getElementById("ModelSelector").options[document.getElementById("ModelSelector").selectedIndex].text;
            }
            else
            {
                CreateFactSheet([],"")
            }
                

            if (window.XMLHttpRequest) {
                        // code for IE7+, Firefox, Chrome, Opera, Safari
                        xmlhttp = new XMLHttpRequest();
                    } else {
                        // code for IE6, IE5
                        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                    }
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            //console.log(this.responseText)
                            returned_info=[];
                            if(this.responseText != "")
                            {
                                returned_info=JSON.parse(this.responseText);
                                
                            }
                            CreateFactSheet(returned_info,model_Name);
                            
                        }
                    };
                    
                     
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/getModelInfo.php?Experiment="+Experiment+"&mID="+model_ID
                    
                    console.log("==================")
                    console.log(php_call)
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
           }

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    mod_sel.onchange=function(){GetModelInfo()}


--------------------------------

.. _editThresholdLibrary:

editThreshold
-------------

This function edits the threshold values for a specific model and classification. 

It also calls a php file, which can be found here: :ref:`library_utilsphp`

.. code-block:: html 

           function editThreshold(model_ID, classification,value)
           {
            class_name=classification.replace("_edit","")
            console.log("editThreshold",model_ID, class_name,value)
            if (window.XMLHttpRequest) {
                        // code for IE7+, Firefox, Chrome, Opera, Safari
                        xmlhttp = new XMLHttpRequest();
                    } else {
                        // code for IE6, IE5
                        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                    }
                    xmlhttp.onreadystatechange = function() {
                        if (this.readyState == 4 && this.status == 200) {
                            //console.log(this.responseText)
                            if(this.responseText != "")
                            {
                                if(this.responseText.includes("Error"))
                                {
                                    alert(this.responseText)
                                }
                                else
                                {
                                    console.log("SUCCESS")
                                    //clear the inputs and reconstruct the thresholds...
                                    GetModelInfo()
                                }
                                
                            }
                            
                            
                        }
                    };
                    
                     
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/library_utils.php?Experiment="+Experiment+"&action=editThreshold&mID="+model_ID+"&class="+class_name+"&value="+value
                    
                    console.log("==================")
                    console.log(php_call)
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
           }

Parameters
~~~~~~~~~~~~~~~

- ``model_ID``: An integer representing the ID of the model. 
- ``classification``: A string representing the classificatio name. 
- ``value``: An integer representing the new threshold value. 


--------------------------------

CreateFactSheet
-------------

This function creates the fact sheet for a selected model. 

.. code-block:: html 

    // Extended code found on GitHub
    function CreateFactSheet(returned_info,model_Name)

Parameters 
~~~~~~~~~~~~~~

- ``returned_info``: An object representing information about the selected model. 
- ``model_Name``: A string representing the name of the selected model. 


--------------------------------

createIframeFromHTML
-------------

This function creates an iframe element and populates it with the provided HTML content. 
It returns an iframe element. 

.. code-block:: html 

           function createIframeFromHTML(html) {
                let iframe = document.createElement("iframe");
                iframe.style.width = "100%";
                iframe.style.height= "100%";
                iframe.onload = function() {
                    iframe.contentWindow.document.open();
                    iframe.contentWindow.document.write(html);
                    iframe.contentWindow.document.close();
                };
                return iframe;
            }

Parameter 
~~~~~~~~~~~~~~

- ``html``: A string representing the HTML content to be displayed in the iframe. 

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    iframe = createIframeFromHTML(returned_info[0]["ConfusionMtx"]);


--------------------------------

MakeSelectedByValue
-------------

This function selects the option in a select element that matches the provided value. 

.. code-block:: html 

            function MakeSelectedByValue(select,val)
            {
                //see if val is in select options
                var options=select.options;
                found =false
                for(var i=0;i<options.length;i++)
                {
                    if(options[i].value==val)
                    {
                        found=true;
                        select.selectedIndex=i;
                        break;
                    }
                }

                if(found)
                {
                    for (var i = 0; i < select.length; i++){
                      var option = select.options[i];
                      // now have option.text, option.value
                      if (option.value==val)
                      {
                          option.selected=true;
                      }
                      else
                      {
                          option.selected=false;
                      }
                    }
                }
            }

Parameters 
~~~~~~~~~~~~~~~~~~

- ``select``: An HTML element representing the select element. 
- ``val``: A string representing the value o match in the select options. 


