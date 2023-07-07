Help
===============

This file contains classes that are referenced later on in html files for formatting purposes.

.modal
---------

.. code-block:: css

    /* The Modal (background) */
    .modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    }


- Hidden from user
- Fixed in position
- 100px padding on top
- Positioned in top-left corner
- Max width and height
- Vertical scrolling
- Black background
- 40% opaque

.modal-content
--------------

.. code-block:: css

    /* Modal Content */
    .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    }

- White background
- Horizontally centered
- 20px padding around
- Gray border
- 80% width

.close
----------

.. code-block:: css

    /* The Close Button */
    .close {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    }

    .close:hover,
    .close:focus {
    color: #000;
    text-decoration: none;
    cursor: pointer;
    }

- Gray color
- Float aligned right
- 28px font size
- Bold font

:hover
~~~~~~~~~~~~~

- Black color
- No text decoration
- Cursor becomes a pointer

:focus
~~~~~~~~~~~~~~~~

- Black color
- No text decoration
- Cursor becomes a pointer




