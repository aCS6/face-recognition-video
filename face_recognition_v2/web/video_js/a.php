<?php 
	// var_dump($_POST['vid']);
	if ( isset( $_FILES["vid"] ) ){
		echo "successvideo";
	  $dir = '/';
	  $blob = file_get_contents($_FILES["file"]['tmp_name']);
	  file_put_contents($dir.$_FILES["file"]["name"], $blob);
	}
?>