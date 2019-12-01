<?php
/**
 * @Author: 0aKarmA_骅文
 * @Date:   2019-06-22 23:58:25
 * @Last Modified by:   0aKarmA
 * @Last Modified time: 2019-06-22 23:58:25
 */
if( isset( $_POST[ 'Upload' ] ) && isset( $_POST[ 'verify' ] ) ) {
    $verify = $_POST[ 'verify' ];
    $contenttype = $_FILES['uploaded']['type'];
    $filename = $_FILES[ 'uploaded' ][ 'name' ];
    $target_path  = "/../uploads/";
    $fileext = explode(".", $_FILES['uploaded']['name'])[1];
    $black = array("php","PHP","php5");
    $content = array("image/jpeg", "image/jpg", "text/html");
    // black list check
    if(in_array($fileext, $black)){
        echo "Sorry,we only allow uploading JPEG images";
        exit;
    }
    else
    {
        // .htaccess
        if($contenttype == "application/octet-stream"){
            $target_path .= basename( $filename );
            if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], __DIR__.$target_path ) ) 
            {
                // No !
                echo '<pre>Your image was not uploaded.</pre>';
            }
            else 
            {
                // Yes!
                echo "<pre>{$filename} succesfully uploaded!</pre>";
            }
        }
        // Content type check
        elseif(!in_array($contenttype, $content)){ 
            echo "Sorry,we only allow uploading JPEG images";
            exit;
        }
        
        else
        {
            $target_path .= basename($verify."_".$filename );
            if( !move_uploaded_file( $_FILES[ 'uploaded' ][ 'tmp_name' ], __DIR__.$target_path ) ) 
            {
            // No !
            echo '<pre>Your image was not uploaded.</pre>';
            }
            else 
            {
                // Yes!
                echo "<pre>*****_{$filename} succesfully uploaded!</pre>";
            }
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Content-Type Detection</title>
</head>
<body>


    <div class="vulnerable_code_area">
        <form enctype="multipart/form-data" action="#" method="POST"">
            Choose a jpg to upload:<br /><br />
            <input type="hidden" name="verify" value="<?php echo gmdate('YmdHis',time() + 8*3600); ?>" />
            <input name="uploaded" type="file" /><br />
            <br />
            <input type="submit" name="Upload" value="Upload" />
    </div>
</body>
</html>
