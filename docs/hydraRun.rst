.. _HydraRunHTML:

HydraRun
============================

This HTML file create Hydra's web-based Run pages, which display plots as they are generated. 

To learn about using the web-based Run page, see here: :ref:`hydraRunFE`


deltaAlpha
--------------

This function adjusts the overlay alpha value (opacity) by adding the specified delta value. 
It ensures that the resulting overlay alpha value is within the range of 0.0 to 1.0.

.. code-block:: html

        function deltaAlpha(delta)
        {
            overlay_alpha=parseFloat((overlay_alpha+delta).toFixed(2))
            
            if(overlay_alpha<0.0)
            {
                overlay_alpha=0.0
            }
            else if(overlay_alpha>1.0)
            {
                overlay_alpha=1.0
            }
            //console.log("alpha:",overlay_alpha)
            try{
                    localStorage.setItem("HydraRun_overlayAlpha_"+Experiment,overlay_alpha.toString());
                } catch (error){
                    console.log(error)
                    
                }
            redrawIMGs()
        }

Parameter
~~~~~~~~~~~~~~~~~~

- ``delta``: A float representing what value to add to the overlay alpha (opacity).

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    deltaAlpha(-0.05)


----------------------------------------------

toggleExpertMode
--------------

This function toggles the expert mode.  

.. code-block:: html

        function toggleExpertMode(){
            ExpertMode=!ExpertMode;
            try{
                    localStorage.setItem("HydraRun_Expert_"+Experiment,ExpertMode.toString());
                } catch (error){
                    console.log(error)
                    
                }
        }


----------------------------------------------

toggle_gradCAM
--------------

This function toggles the overlay alpha value (opacity) between 0.0 and 0.5. 
If the overlay alpha value is currently greater than 0.0, it is set to 0.0.
Otherwise, it is set to 0.5. 

.. code-block:: html

        function toggle_gradCAM()
        {
            if(overlay_alpha>0.0)
            {   
                overlay_alpha=0.0
               
            }
            else
            {
                overlay_alpha=0.5
            }
            try{
                    localStorage.setItem("HydraRun_overlayAlpha_"+Experiment,overlay_alpha.toString());
                } catch (error){
                    console.log(error)
                    
                }
                redrawIMGs()
            //console.log(show_gradCAM)
        }


----------------------------------------------

redrawIMGs
--------------

This function redraws the images on the page by overlaying the latest images with the current overlay alpha value. 

.. code-block:: html

        function redrawIMGs()
        {
            frames=document.getElementById("frames")
            for(let key in latest_imgs)
            {
                    overlayImages(latest_imgs[key][0], latest_imgs[key][1], overlay_alpha).then(canvas => {
                      //const newWindow = window.open();
                      //newWindow.document.body.appendChild(canvas);
                      img = document.getElementById(key)
                      blobUrl=canvas.toDataURL('image/png')
                      URL.revokeObjectURL(img.src)
                        img.src = blobUrl;
                        img.onclick=function (){zoomIMG(this);}
                    });
                
                
            }
        }


----------------------------------------------

setExp
----------------

This function sets the experiment based on the current URL and updates the corresponding experiment logo. 

.. code-block:: html

            function setExp()
            {
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

------------------------------------------

.. _pollRunTimeHydraRun:

pollRunTime
--------------

This function polls the server the get the latest runtime information for the plots, updating the page accordingly. 

It also calls a php file, which can be found here: :ref:`pollRunTimephp`

.. code-block:: html

    // Extended code on GitHub
    function pollRunTime()


Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

     $(document).ready(function(){ setExp();loadDONTSHOW();pollRunTime_interval=setInterval(pollRunTime, 1000);});


----------------------------------------------

removeChildren
--------------

This function removes all child nodes of a specified parent node. 

.. code-block:: html

            function removeChildren(node) {
                while (node.firstChild) {
                    node.removeChild(node.firstChild);
                }
            }

Parameter
~~~~~~~~~~~~~~~~~~

- ``node``: An HTML element representing the parent node from which child nodes will be removed. 

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    removeChildren(rwindow)


----------------------------------------------

.. _BuildRunHTMLHydraRun:

BuildRunHTML
--------------

This function builds the HTML content for the runtime plots by dynamically creating frame elements based on the available plot types. 

It also calls a php file, which can be found here: :ref:`getPlotTypesphp`

.. code-block:: html

            function BuildRunHTML()
            {
                rwindow=document.getElementById("frames")
                removeChildren(rwindow)
                rwindow.innerHTML=""
                poll_lock=false
                //lastUpdateTime=new Date();
                //lastPollTime=lastUpdateTime;
                //time_since_update=0;

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
                                PlotTypes=JSON.parse(this.responseText);
                                //console.log(PlotTypes)
                                total_frame_count=PlotTypes.length
                                hidden_count=0
                                for(var i=0; i<PlotTypes.length;i++)
                                {
                                    
                                    //check if plot name is in DONT_SHOW
                                    if(DONT_SHOW.includes(PlotTypes[i]["Name"]))
                                    {
                                        hidden_count+=1
                                        continue
                                    }
                                    
                                    CreateFrame(PlotTypes[i]["Name"])
                                }
                                //if pollRunTime not setInterval, then set it

                                //setInterval(pollRunTime, 1000);
                            }
                            showing_count=total_frame_count-hidden_count
                            document.getElementById("frameCount").innerHTML="showing "+showing_count+" / "+total_frame_count+" frames"
                        }
                    };
                    
                    //console.log("populate_selectors.php?Selector="+id)
                    php_call="./php/getPlotTypes.php?Experiment="+Experiment
                    //console.log(php_call);
                    xmlhttp.open("GET",php_call,true);
                    xmlhttp.send();
            }


----------------------------------------------

showAll
--------------

This function shows all the hidden frames by clearing the "Dont_Show" array and updating the local storage. 

.. code-block:: html

            function showAll(){
                DONT_SHOW=[]
                savestr=""
                for (var i=0; i<DONT_SHOW.length;i++)
                {
                    if(i==0)
                    {
                        savestr=DONT_SHOW[i]
                    }
                    else
                    {
                        savestr=savestr+":"+DONT_SHOW[i]
                    }
                    
                }
                try{
                    localStorage.setItem("HydraRun_dontShow_"+Experiment,savestr);
                } catch (error){
                    console.log(error)
                    
                }
                finally{
                    BuildRunHTML()
                }
                
            }


----------------------------------------------

loadDONTSHOW
--------------

This function initializes the the "Dont_Show" array, emptying the array or setting it to true if it does not exist in the local storage. 

.. code-block:: html

            function loadDONTSHOW()
            {
                if(localStorage.getItem("HydraRun_dontShow_"+Experiment) != null)
                {
                    DONT_SHOW=localStorage.getItem("HydraRun_dontShow_"+Experiment).split(":")
                }
                else
                {
                    DONT_SHOW=[]
                }

                if(localStorage.getItem("HydraRun_Expert_"+Experiment) != null)
                {
                    ExpertMode=bool(localStorage.getItem("HydraRun_Expert_"+Experiment))
                }
                else
                {
                    ExpertMode=true
                }
                
                if(localStorage.getItem("HydraRun_overlayAlpha_"+Experiment) != null)
                {
                    overlay_alpha=parseFloat(localStorage.getItem("HydraRun_overlayAlpha_"+Experiment))
                }
                else
                {
                    overlay_alpha=0.0
                }
                BuildRunHTML()
            }

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    $(document).ready(function(){ setExp();loadDONTSHOW();pollRunTime_interval=setInterval(pollRunTime, 1000);});


----------------------------------------------

CreateFrame
--------------

This function creates a frame element for a given plot type name.

.. code-block:: html

    // Extended code found on GitHub
    function CreateFrame(name)

Parameter
~~~~~~~~~~~~~~~~~~

- ``name``: A string representing the name of the plot type. 

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    CreateFrame(PlotTypes[i]["Name"])


----------------------------------------------

overlayImages
--------------

This function overlays two images with a specific alpha value, returning the resulting canvas element. 

.. code-block:: html

            function overlayImages(image1, image2, alpha) {
                return new Promise(resolve => {
                const img1 = new Image();
                img1.onload = () => {
                  const img2 = new Image();
                  img2.onload = () => {
                    //console.log(img1.naturalWidth, img1.naturalHeight);
                    //console.log(img2.naturalWidth, img2.naturalHeight);
                    const canvas = document.createElement('canvas');
                    canvas.width = img1.width;
                    canvas.height = img1.height;
                    const ctx = canvas.getContext('2d');

                    ctx.drawImage(img1, 0, 0, img1.width, img1.height);
                
                    ctx.globalAlpha = alpha;
                    ctx.drawImage(img2, 0, 0, img2.width, img2.height);

                    resolve(canvas);
                  };
                  img2.src = URL.createObjectURL(image2);
                };
                img1.src = URL.createObjectURL(image1);
              });
            }

Parameters
~~~~~~~~~~~~~~~~~~

- ``image1``: A string representing the base image in base64 format. 
- ``image2``: A string representing the overlay image in base64 format. 
- ``alpha``: A float representing the alpha value to control the transparency of the overlay image. 

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    overlayImages(latest_imgs[key][0], latest_imgs[key][1], overlay_alpha).then(canvas => {


----------------------------------------------

RenderIMG
--------------

This function renders an image with the provided data and updates the page accordingly. 
If gradCAM data is available, images are overlayed with the gradCAM data. 

.. code-block:: html

           function RenderIMG(data,holder,gradCAM)
           {
               //console.log("RENDER "+holder)
                //console.log("Rendering")
                const img = document.getElementById(holder)
                // Convert the string to bytes

                const b64toBlob = (b64Data, contentType='', sliceSize=512) => {
                const byteCharacters = atob(b64Data);
                const byteArrays = [];

                for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
                    const slice = byteCharacters.slice(offset, offset + sliceSize);

                    const byteNumbers = new Array(slice.length);
                    for (let i = 0; i < slice.length; i++) {
                      byteNumbers[i] = slice.charCodeAt(i);
                    }

                    const byteArray = new Uint8Array(byteNumbers);
                    byteArrays.push(byteArray);
                }
    
                const blob = new Blob(byteArrays, {type: contentType});
                return blob;
                }

                const contentType = 'image/png';
                const b64Data = data;

                const blob = b64toBlob(b64Data, contentType);
                blob_to_show=blob
                blobUrl = URL.createObjectURL(blob_to_show);
                if(show_gradCAM && gradCAM!=null && gradCAM!="")
                {
                    const contentType= 'image/png';
                    const gc_b64Data=gradCAM;
                    const gc_blob = b64toBlob(gc_b64Data, contentType);
                    
                    latest_imgs[holder]=[blob,gc_blob]

                    overlayImages(blob, gc_blob, overlay_alpha).then(canvas => {
                      //const newWindow = window.open();
                      //newWindow.document.body.appendChild(canvas);
                      blobUrl=canvas.toDataURL('image/png')
                      URL.revokeObjectURL(img.src)
                                    img.src = blobUrl;
                                    img.onclick=function (){zoomIMG(this);}
                    });
                    return
                }

Parameters
~~~~~~~~~~~~~~~~~~

- ``data``: A string representing the image data in base64 format. 
- ``holder``: A string representing the ID of the holder element to update with the rendered image. 
- ``gradCAM``: An optional string representing the gradCAM data in base64 format. Default is an empty string. 

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    RenderIMG(NewPlots[i]["IMG"],root_name,NewPlots[i]["gradCAM"])


----------------------------------------------

zoomIMG
--------------

This function opens the image in a new window when the image is clicked. 

.. code-block:: html

           function zoomIMG(img)
           {
               window.open(img.src,img.id)
           }

Parameter
~~~~~~~~~~~~~~~~~~

- ``img``: An HTML image element representing the image to open. 

Example Usage
~~~~~~~~~~~~~~~~~

.. code-block:: html 

    img.onclick=function (){zoomIMG(this);}


----------------------------------------------

