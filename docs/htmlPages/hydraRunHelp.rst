.. _HydraRunHelpHTML: 

HydraRunHelp 
======================

This HTML file runs background scripts for Hydra's web-based Run page. 

Highlight 
-----------------

This function bolds the border of an element if e = 1 and does nothing to other elements. 

.. code-block:: html 

    function Highlight(obj, e) {
        objrootid = (obj.id).split("_")[0];
        element = document.getElementById(objrootid)
        if (element) {
            if (e == 1) {
                element.style.border = "thick solid #FF0000";
            }
            else {
                element.style.border = "none";
            }
        }
    }

Parameters
~~~~~~~~~~~~~~~~

- ``obj``: An HTML element representing what to highlight. 
- ``e``: A value indicating a hierarchy of elements. 

Example Usage
~~~~~~~~~~~~~~~~

.. code-block:: html 

    <p id="frametitle-info">The <b id="frametitle_txt" onmouseover="Highlight(this,1)" onmouseout="Highlight(this,0)">title</b> of <b id="CDCoccupancy_txt" onmouseover="Highlight(this,1)" onmouseout="Highlight(this,0)">image</b> displayed above.</p>


-----------------------------

ConfidenceToggle 
---------------

This function creates a popup to alert the user of their actions. 

.. code-block:: html 

    function ConfidenceToggle() {
        //Make a popup
        alert("performing this action would toggle the display of confidence information on the page.  The confidence is simply the value assigned to the highest value classification after normalization such that the sum of values across classifications are 1.");
    }


----------------------------------

showAll
----------------

This function creates a popup to alert the user of their actions. 

.. code-block:: html 

    function showAll() {
        //Make a popup
        alert("performing this action would reshow any hidden frames on the page.");
    }


---------------------------

HighlightBorder
-----------------

This function bolds the border of an element if e = 1 and creates a regular border around other elements. 

.. code-block:: html 

    function HighlightBorder(obj, e) {
        objrootid = (obj.id).split("_")[0];
        element = document.getElementById(objrootid)
        if (element) {
            if (e == 1) {
                element.style.border = "thick solid #FF0000";
            }
            else {
                element.style.border = "solid #000000";
            }
        }
    }

Parameters
~~~~~~~~~~~~~~~~~~

- ``obj``: An HTML element representing what to highlight. 
- ``e``: A value indicating a hierarchy of elements. 

Example Usage
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    <p id="border-info">Each <b id="frames_txt" onmouseover="Highlight(this,1)" onmouseout="Highlight(this,0)">frame</b> has a <b id="border_txt" onmouseover="HighlightBorder(this,1)" onmouseout="HighlightBorder(this,0)">border</b> which conveys the most important information through its color and stye.  These styles are intricate enough that they deserve specific enumeration and descriptions below.</p><br>


----------------------------

HighlightInfo 
----------------

This function sets the font size to 20pt if e = 1 and 12pt if it does not. 

.. code-block:: html 

    function HighlightInfo(obj, e) {
        
        element = document.getElementById(obj.id + "-info")
        if (element) {
            if (e == 1) {
                element.style.fontSize = "20pt";
            }
            else {
                element.style.fontSize = "12pt";
            }
        }
    }

Parameters
~~~~~~~~~~~~~~~~~~

- ``obj``: An HTML element representing what to highlight. 
- ``e``: A value indicating a hierarchy of elements. 

Example Usage
~~~~~~~~~~~~~~~~

.. code-block:: html 

    <div id="header"><img onmouseover="HighlightInfo(this,1)" onmouseout="HighlightInfo(this,0)" class="navbar-brand" id="Explogo" src="./img/GlueX_logo.png" ondblclick="ConfidenceToggle()">


--------------------------

StyleBorder
-------------

This function configures the border and background of the frame to given settings. 

.. code-block:: html 

    function StyleBorder(style, color, bgcolor) {
        
        document.getElementById("border").style.borderStyle = style;
        document.getElementById("border").style.borderColor = color;
        document.getElementById("frameinternal").style.backgroundColor = bgcolor;
    }

Parameters
~~~~~~~~~~~~~~~~~~

- ``style``: A string representing the style of the border. 
- ``color``: A string representing the color of the border.
- ``bgcolor``: A string representing the background color for the border. 

Example Usage
~~~~~~~~~~~~~~~~~~~

.. code-block:: html 

    <p id="red-info" onmouseover="StyleBorder('solid','red','red')" onmouseout="StyleBorder('solid','black','white')"><b>Red</b> is reserved for "Bad" classifications. This may be an indication of a problem and should be watched closely or action should be taken.  Shift crews are reminded to respond to standard alarm appropriately.</p>


--------------------------------

HideAFrame
----------------

This function creates a popup to alert the user of their actions. 

.. code-block:: html 

    function HideAFrame() {
        //Make a popup
        alert("performing this action would hide a frame on the page.");
    }
