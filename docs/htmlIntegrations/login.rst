.. _loginphp:

login
====================

This php file stores chunked plots and their information. 

This This php file is called in:

- :ref:`loginFuncLabeler` function from the **labeler.html** file. 
- :ref:`loginFuncLibrary` function from the **Library.html** file.

.. code-block:: php

    $sql="SELECT Name, IsChunked from Plot_Types where ID in (SELECT Plot_Type_ID from User_Permissions where UserName=\"". $_SERVER['PHP_AUTH_USER'] ."\");";


