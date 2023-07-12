label 
=================

This file contains classes and IDs that are referenced later on in HTML files for formatting purposes.

.navbar
-----------

.. code-block:: css

    .navbar {
        margin-bottom: 0;
        border-radius: 0;
      }

- Remove the navbar's default margin-bottom and rounded borders

--------------------------

.row.content
--------------

.. code-block:: css
    
    .row.content {height: 450px}

- Set height of the grid so ``.sidenav`` can be 100% (adjust as needed)

--------------------------

.sidenav
----------

.. code-block:: css
    
      .sidenav {
        padding-top: 20px;
        background-color: #f1f1f1;
        height: 75em;
      }

- Set gray background color 
- 100% height

--------------------------

footer
-----------

.. code-block:: css
    
    footer {
        background-color: #555;
        color: white;
        padding: 15px;
    }
    
- Set black background color
- Set white text 
- 15px padding

--------------------------

@media screen
--------------

.. code-block:: css
    
    @media screen and (max-width: 767px) {
        .sidenav {
          height: auto;
          padding: 15px;
        }
        .row.content {height:auto;} 
    }

- On small screens, set height to 'auto' for sidenav and grid

--------------------------

.zoom
--------------

.. code-block:: css
    
    .zoom {

        transition: transform .2s; /* Animation */
        margin: 0 auto;
    }

- Animates a 0.2 second transitions
- 0 margins on top and margin-bottom
- Horizontally center

--------------------------

:hover
~~~~~~~~~~~~~~~~

.. code-block:: css
    
    .zoom:hover {
        transform: scale(2); /* translate(50%,50%) (150% zoom - Note: if the zoom is too large, it will go outside of the viewport) */
        position: absolute;
        
    }

- Scale factor of 2
- Absolute position

--------------------------

.LeaderLabel
------------

.. code-block:: css
    
    .LeaderLabel
    {
    font-size:20px;
    font-style:bold;
    }

- 20px font size
- Bolded font

--------------------------

.Leader
-------------

.. code-block:: css
    
    .Leader
    {
    font-size:32px;
    font-style:bold; 
    }

- 32px font size
- Bolded font

--------------------------

#Plot_Type
-------------

.. code-block:: css
    
    #Plot_Type
    {

        font-size: 16px;
        font-family: sans-serif;
        font-weight: 700;
        color: #444;
        line-height: 1.3;
        padding: .6em 1.4em .5em .8em;
        
        box-sizing: border-box;
        border: 1px solid #aaa;
        box-shadow: 0 1px 0 1px rgba(0,0,0,.04);
        border-radius: .5em;
        -moz-appearance: none;
        -webkit-appearance: none;
        appearance: none;
        background-color: #fff;
        background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23007CB2%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E'),
        linear-gradient(to bottom, #ffffff 0%,#e5e5e5 100%);
        background-repeat: no-repeat, repeat;
        background-position: right .7em top 50%, 0 0;
        background-size: .65em auto, 100%;
    }

- 16px sans-serif font
- 700 font weight
- Dark Gray font
- 1.3 line height
- Padding around element: .6em 1.4em .5em .8em
- Border box with 1px light gray
- Box shadow
- 0.5em border radius
- Removes default Firefox and WebKit characteristics
- White background with image and gradient
- Background repeat, position, and size properties

--------------------------

.select-css
-------------

:: ms-expand
~~~~~~~~~~~~~~~~

.. code-block:: css
    
    .select-css::-ms-expand {
        display: none;
    }

- Hides expand icon

:hover
~~~~~~~~~~~~~~~~

.. code-block:: css
    
    .select-css:hover {
        border-color: #888;
    }

- Gray border color

:focus
~~~~~~~~~~~~~~~~

.. code-block:: css
    
    .select-css:focus {
        border-color: #aaa;
        box-shadow: 0 0 1px 3px rgba(59, 153, 252, .7);
        box-shadow: 0 0 0 3px -moz-mac-focusring;
        color: #222; 
        outline: none;
    }

- Gray border color
- Adds box shadow
- Black font
- No outline

option
~~~~~~~~~~~~~~~~

.. code-block:: css
    
    .select-css option {
        font-weight:normal;
    }

- Normal font weight

--------------------------

.switch-field
--------------

.. code-block:: css
    
    .switch-field {
	
        margin-bottom: 36px;
        overflow: hidden;
    }

- 36px bottom margin
- No overflow

input
~~~~~~~~~~

.. code-block:: css
    
    .switch-field input {
        
        clip: rect(0, 0, 0, 0);
        height: 1px;
        width: 1px;
        border: 0;
        overflow: hidden;
    }

- Clips reactangle to nothing
- Height and Width to 1px
- Removes border and overflow

input:checked + label
~~~~~~~~~~~~~~~~

.. code-block:: css
    .switch-field input:checked + label {
        background-color: #a5dc86;
        box-shadow: none;
    }

    
- Light green background color
- No shadow

--------------------------

label
~~~~~~~~~~~~

.. code-block:: css

  .switch-field label {
        background-color: #e4e4e4;
        color: rgba(0, 0, 0, 0.6);
        font-size: 14px;
        line-height: 1;
        text-align: center;
        padding: 8px 16px;
        margin-right: -1px;
        border: 1px solid rgba(0, 0, 0, 0.2);
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.1s ease-in-out;
    }

- Light gray background color
- 14px 60% opaque font
- 1 line height
- Center align
- Padding around label
- Negative right margin
- 1 px 20% opaque border
- Box shadow
- Animates 0.1 second transition

label:hover
~~~~~~~~~~~~~~

.. code-block:: css

    .switch-field label:hover {
        cursor: pointer;
    }

- Cursor turns to pointer

label:first-of-type
~~~~~~~~~~~~~~~~~

.. code-block:: css

    .switch-field label:first-of-type {
        border-radius: 4px 0 0 4px;
    }

- Left corners have border radii of 4px

label:last-of-type
~~~~~~~~~~~~~

.. code-block:: css
    
    .switch-field label:last-of-type {
        border-radius: 0 4px 4px 0;
    }

- Right corners have border radii of 4px

--------------------------

#logo
-------------

.. code-block:: css
   
    #logo
    {
    margin:-9px;
    text-align: center;
    height:auto;
    width:100px;
    float:left
    }

- -9px margin
- Center align
- Auto height
- 100px width
- Float aligns left

--------------------------

.color
------------

.. list-table::
    :widths: 30 15 30
    :header-rows: 1

    * - Status
      - Color
      - Border
    * - _Good.active
      - Light Green
      - None
    * - _Acceptable.active
      - Dark Green
      - None
    * - _Bad.active
      - Red
      - None
    * - _HotChannel.active
      - Bright Yellow
      - None
    * - _Cosmic.active
      - Golden
      - None
    * - _LED.active
      - Blue
      - None
    * - _TrainingSet.active
      - None
      - 5px Green
    * - _ValidationSet.active
      - None
      - 5px Yellow
    * - _NoData.active
      - Gray
      - None
    * - _Ignore.active
      - Orange
      - None
    * - _Source.active
      - Dark Blue
      - None

--------------------------

.gridColor
--------------

.. list-table::
    :widths: 30 15 30
    :header-rows: 1

    * - Status
      - Color
      - Border
    * - _Good
      - Light Green
      - None
    * - _Acceptable
      - Dark Green
      - None
    * - _Bad
      - Red
      - None
    * - _HotChannel
      - Bright Yellow
      - None
    * - _Cosmic
      - Golden
      - None
    * - _LED
      - Blue
      - None
    * - _TrainingSet
      - None
      - 5px Green
    * - _ValidationSet
      - None
      - 5px Yellow
    * - _NoData
      - Gray
      - None
    * - _Ignore
      - Orange
      - None
    * - _Source
      - Dark Blue
      - None

--------------------------

.active
-----------

.. code-block:: css
    
    .active
    {
        box-shadow: none;
    }

- No shadow

--------------------------

.img-grid
-------------

.. code-block:: css
    
    .img-grid
    {
        height: 90vh;
        width: 83vw;
        padding-bottom: 50px;
        padding-right: 20px;
        overflow-x: scroll;
    overflow-y: scroll; 
    text-align: center;
    }

- Height set to 90% of screen
- Width set to 83% of screen
- 50px bottom padding
- 20px right padding
- Horizontal and vertical scrolling
- Horizontally centered

--------------------------

#context_cntnr
------------

.. code-block:: css
    
    #context_cntnr{
    display:none;
    position:fixed;
    }

- Element hidden
- Fixed position

--------------------------

.colorpicker
-----------

.. code-block:: css
    
    .colorpicker {
    border: solid thin black;
    width: 200px;
    height: 200px;
    }

- Solid black border
- 200px width and height


--------------------------

#colorSelector
------------

.. code-block:: css

    #colorSelector {
    display : inline-block;
    width: 100px;
    height: 25px;
    }

- Inline block
- 100px width
- 25px height

div
~~~~~~~~~~

.. code-block:: css

    #colorSelector div {
    float : left;
    border : 1px solid #C5C5C5;
    padding : 1px;
    margin : 0 3px 0 0;
    width: 25px;
    height: 25px;
    }

- Float aligns left
- 1px gray border
- 1px padding around element
- 3px margin on right
- 25px width and height

input
~~~~~~~~

.. code-block:: css

    #colorSelector input {
        width : 51px;
    }

- 51px width
