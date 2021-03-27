<?php

include_once("db_conf.php"); // Include nastavení DB

$sql = $conn->prepare("INSERT INTO log_data (type, text) VALUES (?,?)");
$text = $_POST["text"];
$type = $_POST["type"];

$text = htmlspecialchars($_POST["text"]);
$type = intval(htmlspecialchars($_POST["type"]));
$sql->bind_param("is", $type, $text);

$sql->execute();
