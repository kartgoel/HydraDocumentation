.. _labelerHTML:

labeler
===================

This HTML file creates Hydra's web-based labeler, which allows experts to labels plots and assigns a label leader to each plot type.  
It creates the various drop-down bars for selecting which experiments and plots the user will label, as well as the dropwdown bar for selecting a label. 
It also generates the page with images, formatting them as needed.

To learn about using the web-based labeler, see here: :ref:`labelerFE`

RecordLastType
---------------------

This function records the last selected value for a plot and stores it in the browser's local storage.

.. code-block:: html

    function RecordLastType()
    {
        localStorage.setItem("HydraLabeler_hist_"+Experiment,document.getElementById("Plot_Type").value);
    }

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    <select id="Plot_Type" onchange="RecordLastType();CreateLabelPalette();populateImages()">


------------------------------------------------------

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

populateFilters
------------

This function populates the filters section based on the mode and labelPalette array.

.. code-block:: html 

            function populateFilters()
            {
                filterDIV=document.getElementById("filters")
                filterDIV.innerHTML=""

                if(mode=="editor")
                {
                    for(var i=0;i<labelPalette.length;i++)
                    {
                        var checkbox = document.createElement('input');
                        checkbox.type = "checkbox";
                        checkbox.name = labelPalette[i]["Classification"];
                        checkbox.value = labelPalette[i]["Classification"];
                        checkbox.id = labelPalette[i]["Classification"]+"_Filter";
                        checkbox.onclick=function click(){populateImages()}
                        var label = document.createElement('label')
                        label.htmlFor = labelPalette[i]["Classification"]+"_Filter";
                        label.appendChild(document.createTextNode(labelPalette[i]["Classification"]));

                        filterDIV.appendChild(checkbox);
                        filterDIV.appendChild(label);
                        filterDIV.appendChild(document.createElement("br"))
                    }
                }
            }


-----------------------------------------------------

getActivePaletteIndex
-----------

This function searches for the active palette, retrieving its index from its ID. 
It returns the index of the active palette.

.. code-block:: html 

            function getActivePaletteIndex()
            {
                var pal=document.getElementById("Palette-Holder")
                var activePalette=pal.getElementsByClassName("active")[0];
                var activePaletteId=activePalette.id.split("_")[1];
                var index=-1
                for(var i=0;i<pal.childNodes.length;i++)
                {
                    if(pal.childNodes[i].id.split("_")[1]==activePaletteId)
                    {
                        index=i;
                        break
                    }
                }
                
                console.log(index)
                return index;
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    var old_index=getActivePaletteIndex();


-----------------------------------------------------------------

SetMode
-------------

This function sets the mode based on the the state of the "editorToggle" switch. 
It updates the global mode, clears image table body, populates filters, and populates images. 

.. code-block:: html

            function SetMode()
            {
                var toggle_switch=document.getElementById("editorToggle");
                if(toggle_switch.checked)
                {
                    mode="editor";
                    
                }
                else
                {
                    mode="novel";
                }
                console.log(mode)
                $("#imgTableBody").empty();
                populateFilters();
                populateImages();
                
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    <p>Editor mode: <input type="checkbox" id="editorToggle"  data-toggle="toggle" onchange="SetMode();"></p>


------------------------------------------------------

SetColumns
-------------

This function sets the number of columns to display based on a selected value. 
It updates the global number displayed columns and populates images with the new column configuration. 

.. code-block:: html

            function SetColumns()
            {
                var columns_select=document.getElementById("columnsSelect");
                var columns_selected=columns_select.options[columns_select.selectedIndex].value;
                columnstoDisplay=columns_selected;
                populateImages(true);
                
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    <p>Columns <select id="columnsSelect"  data-toggle="toggle" onchange="SetColumns();">


------------------------------------------------------

startFocusOut
-------------

This function is used to hide a context menu or drop-down bar when the user interacts with other parts of the page. 

.. code-block:: html

            function startFocusOut(){
                $(document).on("click",function(){
                $("#context_cntnr").hide();        
                //$(document).off("click");
            });
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    $("#context_cntnr").fadeIn(200,startFocusOut());


------------------------------------------------------

getStyle
-------------

This function retrieves certain CSS style rules, finds the specified class selector, and returns the CSS text. 

.. code-block:: html

            function getStyle(className) {
                var cssText = "";
                var classes = document.styleSheets[4].rules || document.styleSheets[4].cssRules;
                for (var x = 0; x < classes.length; x++) {        
                if (classes[x].selectorText == className) {
                    cssText += classes[x].cssText || classes[x].style.cssText;
                }         
                }
                return cssText;
            }

Parameter
~~~~~~~~~~~~~~~~~~~~~~

- ``className``: A string representing the CSS class for which to retrieve the style rules. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    var color_rgb=getStyle(css_id).split("color:")[1].split(";")[0];


------------------------------------------------------

componentToHex
-------------

This function converts an RGB value to its equivalent hexadecimal representation.
It adds a leading zero if the hex value has only one digit and returns the hex value as a string. 

.. code-block:: html

            function componentToHex(c) {
                var hex = c.toString(16);
                return hex.length == 1 ? "0" + hex : hex;
            }

Parameter
~~~~~~~~~~~~~~~

- ``c``: An integer representing and RGB component value (0-255) to convert.

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
            return componentToHex(r) + componentToHex(g) + componentToHex(b);

------------------------------------------------------

rgbToHex
-------------

This function converts an RGB color value to its equivalent hexadecimal representation. 
It invokes the ``componentToHex`` function to convert each RBG component separately.
It then connets the 3 RGB values and returns the hex value as a string. 

.. code-block:: html

            function rgbToHex(r, g, b) {
                return componentToHex(r) + componentToHex(g) + componentToHex(b);
            }

Parameters 
~~~~~~~~~~~~~~~~~~~~

- ``r``: A string representing the red component value (0-255).
- ``g``: A string representing the green component value (0-255).
- ``b``: A string representing the blue component value (0-255).

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    var color_hex=rgbToHex(parseInt(rgbs[0]),parseInt(rgbs[1]),parseInt(rgbs[2]));


------------------------------------------------------

applyStyle
-------------

This function applies previously saved style rules stored in the browser's local storage depending on the current experiment. 

.. code-block:: html

    // Extended code found on GitHub
    function applyStyle()

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    $(document).ready(function(){setExp();Login();applyStyle();


------------------------------------------------------

ColorPicker 
-------------

This function stores a specified color bthat a user chose from the color picker menu. 
It updates the associated CSS classes with a new color value and stores it in the browser's local storage. 

.. code-block:: html

    // Extended code found on GitHub
    function ColorPicker(element)

Parameter
~~~~~~~~~~~~~~~

- ``element``: An HTML element triggereing the color picker. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    newlabel.oncontextmenu=function click(){ColorPicker(document.elementFromPoint(MouseX,MouseY))}
                                        

------------------------------------------------------

.. _populateSelectorLabeler:

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

SetBrushColor
-------------

This function sets the brush color to a specified value. 

.. code-block:: html

            function SetBrushColor(brush)
            {
                brushColor=brush.id.split("_")[1];
            }

Parameter
~~~~~~~~~~~~~~~

- ``brush``: An HTML element representing the clicked brush. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    SetBrushColor(pal.childNodes[new_index])

------------------------------------------------------

.. _getLeaderLabeler:

getLeader
-------------

This function retrieves the leader for a specific plot from the server, updating the listed leader on a page with their username. 

It also calls a php file, which can be found here: :ref:`getLeaderBoardphp`

.. code-block:: html

            function getLeader(Plot)
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
                                returned_Leader=JSON.parse(this.responseText);
                                console.log(returned_Leader)
                                if(returned_Leader.length==1)
                                {
                                    document.getElementById("leader").innerHTML=returned_Leader[0].User
                                }
                                else
                                {
                                    document.getElementById("leader").innerHTML="No leader.  Get to labeling!"
                                }
                            }
                            
                        }
                    };
                    
                     
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/getLeaderBoard.php?Experiment="+Experiment+"&Plot="+Plot
                    console.log(php_call);
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
            }

Parameter
~~~~~~~~~~~~~~

- ``Plot``: A string representing which plot to retrieve the leader for. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    getLeader(plot_type_selected)


------------------------------------------------------

CreateLabelPalette
-------------

This function creates the label palatte based on the selected plot type. 
It retrieves the selected plot type and corresponding leader, populating the palatte holder with label options. 

.. code-block:: html

            function CreateLabelPalette()
            {
                
                var plot_type_select=document.getElementById("Plot_Type");
                var plot_type_selected=plot_type_select.options[plot_type_select.selectedIndex].value;
                getLeader(plot_type_selected)
                
                if( ! permitted_plots.includes(plot_type_selected))
                {
                    document.getElementById('Palette-Holder').innerHTML = 'You do not have permission to label this plot!';
                }
                else{
                    document.getElementById('Palette-Holder').innerHTML = '';
                    populateSelector("Palette-Holder",plot_type_selected)
                }
                
                labels=[];
                new_labels=0;
                updateApplyNumber();
                
                //console.log(plot_type_selected)
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    <select id="Plot_Type" onchange="RecordLastType();CreateLabelPalette();populateImages()">


------------------------------------------------------

pad
-------------

This function converts a number to a string and pads it with leading zeros to a specified width.

.. code-block:: html

            function pad(n, width, z) {
              z = z || '0';
              n = n + '';
              return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
            }

Parameters 
~~~~~~~~~~~~~~

- ``n``: An integer representing which number to pad. 
- ``width``: An integer representing the desired width of the padded number. 
- ``z``: An optional string representing which character to use for padding. Default is '0'. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    var formatted_RunNumber=pad(returned_img_table['imgs'][i]["RunNumber"],6)


------------------------------------------------------

UpdateLabels
-------------

This function updates the labels data based on existing labels with matching run and chunk numbers. 
If matching numbers are found, the label is updated with a new brush color. 

.. code-block:: html

        // Extended code found on GitHub
        function UpdateLabels(runnum,chunknum,brushcol)
        
Parameters
~~~~~~~~~~~~~~~~~

- ``runnum``: An integer representing the run number of the label.
- ``chunknum``: An integer representing the chunk number of the label. 
- ``brushcol``: A string representing the brush color of the label. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    UpdateLabels(cell_runnum,chunkNum,brushColor);

------------------------------------------------------

updateApplyNumber
-------------

This function updates the apply button with the number of new labels, setting the button texts with the appropriate labels. 

.. code-block:: html

            function updateApplyNumber()
            {
                if(new_labels>0)
                {
                    document.getElementById("applyButton").value="Apply "+new_labels+" labels"
                }
                else
                {
                    document.getElementById("applyButton").value="Apply 0 labels"
                }
            }


------------------------------------------------------

UrlExists
-------------

This function checks if a URL exists by checking its response status (status 200 or 404). 
It returns the existence status of the URL as either 'true' or 'false'.

.. code-block:: html

            function UrlExists(url) {
                var http = new XMLHttpRequest();
                http.open('HEAD', url, false);
                http.send();
                if (http.status != 404)
                   return true;
                else
                    return false
            }

Parameter 
~~~~~~~~~~~~~~~~

- ``url``: A string representing the URL to check for existence. 


------------------------------------------------------

MakeSelectedByValue
-------------

This function sets the selected option. 

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
~~~~~~~~~~~~~~~~~~~~~~~~

- ``select``: An HTML element in which the option is selected. 
- ``val``: A string representing the value of the option to be selected. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    MakeSelectedByValue(document.getElementById("Plot_Type"),localStorage.getItem("HydraLabeler_hist_"+Experiment))


------------------------------------------------------

populateImages
-------------

This function populates a table with images based on the selected plot type. 
It handles AJAX requests to retrieveimage data from the server. 

.. code-block:: html

    // Extended code found on GitHub
    function populateImages(repaint=false,scrollpos=0)

Parameters 
~~~~~~~~~~~~~~~~~~~~~~~

- ``repaint``: An optional boolean that will repaint the tables based on exisiting image data when 'true'. Default is 'false'. 
- ``scrollpos``: An optional integer representing the desired scroll position of the image grid. Defaults to '0'. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    populateImages(true,scroll_pos)


------------------------------------------------------

PaintCell
-------------

This function paints a cell in the grid with a specific color, which is typically called when a user clicks on an image. 
It updates the CSS classes and updates the labels associated with the cell. 

.. code-block:: html

    // Extended code found on GitHub
    function PaintCell(cell)

Parameter 
~~~~~~~~~~~~

- ``cell``: An HTML element represting the cell image to be painted. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    DOM_txt.innerHTML="<center onclick='function click(){ PaintCell(this);}'><font size='5'>"+"Simulated  "+returned_img_table['imgs'][i]["RunPeriod"]


------------------------------------------------------

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


------------------------------------------------------

isEmpty
-------------

This function checks if an object contains any properties. 
The object is returned as 'true' if the object is empty and 'false' if the object is not empty. 

.. code-block:: html

            function isEmpty(obj) {
                for(var key in obj) {
                    if(obj.hasOwnProperty(key))
                    return false;
                }
                return true;
            }

Parameter
~~~~~~~~~~~~~~~~~

- ``obj``: An object to be checked. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    if(! isEmpty(jsonData))
    

------------------------------------------------------

Repaint
-------------

This function repaints the grid based on the existing label data.
It iterates over the labels and updates the corresponding cells with their associated colors.  

.. code-block:: html

            function Repaint()
            {
                console.log("Repaint")
                console.log(jsonData)
                if(! isEmpty(jsonData))
                {
                    console.log(jsonData["labels"])
                    
                    for(var i=0;i<jsonData["labels"].length;i++)
                    {
                        //console.log(jsonData["labels"][i])
                        var formatted_RunNumber=pad(jsonData["labels"][i]["RunNum"],6)
                        //console.log(formatted_RunNumber)
                        img_ID="img_"+formatted_RunNumber+"_"+pad(jsonData["labels"][i]["ChunkNum"],4)
                        header_ID="header_"+formatted_RunNumber+"_"+pad(jsonData["labels"][i]["ChunkNum"],4)
                        //console.log(img_ID)
                        document.getElementById(img_ID).setAttribute("class","gridColor_"+jsonData["labels"][i]["Label"]);
                        document.getElementById(header_ID).parentElement.setAttribute("class","gridColor_"+jsonData["labels"][i]["Label"]) //.style.backgroundColor=color;
                        document.getElementById(header_ID).setAttribute("value",jsonData["labels"][i]["Label"]);
                    }
                }
            }

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    function populateImages(repaint=false,scrollpos=0)


------------------------------------------------------

RecordLabels
-------------

This function record the labels associated with the images in the grid. 
It sends an AJAX request to the server to store the labels for the selected experiment. 

.. code-block:: html

    // Extended code found on GitHub
    function RecordLabels(labels_to_record=jsonData)

Parameter
~~~~~~~~~~~~~~~~~~~~

- ``labels_to_record``: 

record_labels.php
~~~~~~~~~~~~~~~~~~~

This segment 

.. code-block:: html 

    php_call="./php/record_labels.php?Experiment="+Experiment+"&Labels="+JSON.stringify(labels_to_record)

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 
    
    const result = await RecordLabels(block_json)


