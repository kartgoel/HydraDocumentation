.. _library_utilsphp:

library_utils
================

This php file runs background processes to set threshold values and retrieve other model and plot data. 

This php file is called in:
 
- :ref:`editThresholdLibrary` function from the **Library.html** file.

.. code-block:: php

    #$sql="SELECT * from RunTime where DateTime > now() - interval 10 SECOND;";

    //DO CLEANUP

    //$cleansql="DELETE FROM RunTime where DateTime < now() - interval 1 hour";
    //$conn->query($cleansql);
    //$conn->commit();
    if($Action=="editThreshold")
    {

    //+------------------------+--------------+------+-----+---------+----------------+
    //| Field                  | Type         | Null | Key | Default | Extra          |
    //+------------------------+--------------+------+-----+---------+----------------+
    //| ID                     | int(11)      | NO   | PRI | NULL    | auto_increment |
    //| Model_ID               | int(11)      | NO   | MUL | NULL    |                |
    //| Plot_Classification_ID | int(11)      | NO   |     | NULL    |                |
    //| Threshold              | double       | NO   |     | NULL    |                |
    //| ThresholdMethod        | varchar(100) | YES  |     | INIT    |                |
    //+------------------------+--------------+------+-----+---------+----------------+
        $class_name=$_GET['class'];
        //get ID of class_name from Plot_Classifications
        $sql="SELECT ID from Plot_Classifications where Classification = '" . $class_name . "';";
        $result = $conn->query($sql);
        $clas_ID=$result->fetch_assoc()['ID'];
        // Escape the user input to prevent SQL injection attacks
        $value = $conn->real_escape_string($_GET['value']);
        $User = $conn->real_escape_string($User); // assuming $User is defined elsewhere
        $mID = $conn->real_escape_string($_GET['mID']);
        $clas_ID = $conn->real_escape_string($clas_ID); // assuming $clas_ID is defined elsewhere

        // Construct the SQL query and execute it
        $update_q = "UPDATE ModelThresholds SET Threshold=$value, ThresholdMethod='$User' WHERE Model_ID=$mID AND Plot_Classification_ID=$clas_ID";
        echo $update_q;
        echo "<br>";
        if ($conn->query($update_q) === TRUE) {
        return "Success";
        } else {
        return "Error: " . $conn->error;
        }
        //execute and commit
        
    }


Parameters
~~~~~~~~~~~~~~~

- ``model_ID``: An integer representing the ID of the model. 
- ``class_name``: A string representing the classification name. 