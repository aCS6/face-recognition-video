<?php

	if (isset( $_FILES["vid"])){
          $dir = 'video/';
          $blob = file_get_contents($_FILES["vid"]['tmp_name']);
          $unique_name = date("h_i_sa");
          file_put_contents($dir.$unique_name, $blob);
          echo $unique_name;
          
    }
?>
