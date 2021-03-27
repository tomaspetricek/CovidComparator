<?php

$server = "wm101.wedos.net";
$username = "w118404_covid";
$password = "########";

$conn = new mysqli($server, $username, $password);

if($conn->connect_error) {
    echo $conn->connect_error;
    die("Unable to connect" . $conn->connect_error);
}
$conn->select_db("d118404_covid");