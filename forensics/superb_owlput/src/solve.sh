python3 solve.py
exiftool outfile | grep Artist | cut -d ':' -f 2 | xargs | base64 -d 2>/dev/null 
