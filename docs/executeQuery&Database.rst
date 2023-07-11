Executing Query in Database
=======================

Connecting to Database
-----------------

This code segment establishes a connection to the MySQL database. 

.. code-block:: php 

    //echo $_GET['qs'] . " ---> " . $_GET['qe'];
    // Create connection
    $conn = mysqli_connect($servername, $username, $password, $dbname);
    // Check connection
    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }

Executing Query
---------------

This code segment is the basic format for executing a query and storing the results. 

.. code-block:: php 

    $result = $conn->query($sql);
    $data = array();
    if ($result->num_rows > 0) {
    // output data of each row
        while($row = $result->fetch_assoc()) {
            $data[]=$row;
        //echo "id: " . $row["id"]. " - Run: " . $row["run"]. "<br>";
        }
    }
    $conn->close();

    echo json_encode($data);
    return json_encode($data);