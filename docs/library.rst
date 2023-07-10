.. _LibraryHTML:

Library
=========================

This HTML file 

To learn about , see here: :ref:`libaryFE`

setExp
----------------

This function sets the experiment based on the current URL and updates the corresponding experiment logo. 

.. code-block:: html

    // Extended code found on GitHub 
    function setExp()

Example Usage
~~~~~~~~~~~~~~

.. code-block:: html 

     $(document).ready(function(){setExp();Login();applyStyle();


----------------------------------------------------

.. _loginFuncLabeler:

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

This function 

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

This function 

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

This function 

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

This function 

.. code-block:: html 

    // Extended code on GitHub
    function MakeModelSelector(returned_info)

Parameter
~~~~~~~~~~~~~

- ``returned_info``: 


--------------------------------

.. _GetModelInfoLibrary:

GetModelInfo
-------------

This function 

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

This function 

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

- ``model_ID``: 
- ``classification``: 
- ``value``: 

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 


--------------------------------


-------------

This function 

.. code-block:: html 


Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 




