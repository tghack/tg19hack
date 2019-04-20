<?php
$target_dir = "uploads/";
$uplFilename = basename($_FILES["fileToUpload"]["name"]);
$imageFileType = strtolower(pathinfo($uplFilename,PATHINFO_EXTENSION));
$filename = uniqid() . ".$imageFileType";
$target_file = $target_dir . $filename;
$uploadOk = 1;
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}

if($uploadOk == 0) {
	echo "Failed upload :( Is it a valid image file?";
} else {
	move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);
	echo "File available at <a href='$target_file'>$target_file</a>";
}

?>
