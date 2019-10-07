<?php
$searchterm = $_GET["searchbox"];
echo $searchterm;
echo exec("python test.py $searchterm");
?>