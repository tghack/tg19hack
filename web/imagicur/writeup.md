# Writeup for Imagicur
**Points: 150**

**Author: aleksil**

**Difficulty: challenging**

**Category: web**

---

When opening the web-page we are greeted with a file upload form that is meant for uploading images.

Trying to upload a non-image file will result in an error, however, the webserver doesn't use the file-name extension to decide if a file is an image or not, it uses the php `getimagesize`-function. The critical error in this program is that it also keeps the file extension that the user provided with the uploaded files.

This means that we can do the following:
    1. Create a valid image file with embedded PHP code
    2. Name this image file something.php
    3. Upload it and navigate to the uploaded "image" to run our code!

Creating the image file with the embedded PHP code is easy, we can use a tool called `exiftool` to insert comments into files.

Say we have a jpeg file `test.jpg` we can do the following:
```
$ exiftool -comment="<?php readfile('../flag.txt'); die(); ?>" test.jpg
    1 image files updated
$ mv test.jpg test.php
```

Then we can upload this `test.php`-file to the server, and once we open the URL the upload returns we will be greeted with the flag: `TG19{phony_php_images_can_b_scary}`

