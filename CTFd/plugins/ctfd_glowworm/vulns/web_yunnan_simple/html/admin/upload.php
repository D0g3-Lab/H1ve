<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
<?php
include_once('../config.php');
if (isset($_SESSION['username'])) {
        include_once('header.php');
        $html_username = htmlspecialchars($_SESSION['username']);
        if(isset($_SESSION['error_info']) && $_SESSION['error_info'] != '') {
                echo $_SESSION['error_info'];
                $_SESSION['error_info'] = '';
        }
	

}
else {
	not_find($_SERVER['PHP_SELF']);
	exit();
}


$error=$_FILES['pic']['error'];
$tmpName=$_FILES['pic']['tmp_name'];
$name=$_FILES['pic']['name'];
$size=$_FILES['pic']['size'];
$type=$_FILES['pic']['type'];
try{
	if($name!=="")
	{
		$name1=substr($name,-4);
		if(is_uploaded_file($tmpName)){
			$time=time();
			$rootpath='./upload/'.$time.$name1;
			$file=fopen($tmpName, "r") or die('No such file!');
                	$content=fread($file, filesize($tmpName));
                	if(strstr($content,'fuck')){
                        	exit("<script language='JavaScript'>alert('You should not do this!');window.location='index.php?page=submit'</script>");
                	}
			if(!move_uploaded_file($tmpName,$rootpath)){
				echo "<script language='JavaScript'>alert('文件移动失败!');window.location='index.php?page=submit'</script>";
				exit;
			}
		}
		echo "上传成功：/upload/".$time.$name1;
	}
}
catch(Exception $e)
{
	echo "ERROR";
}
//
require('footer.php');
 ?>
 </html>
