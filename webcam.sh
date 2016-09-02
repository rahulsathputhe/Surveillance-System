#!/bin/bash

#DATE=$(date +"%Y-%m-%d_%H%M")
rm -f picture.jpg

#fswebcam -r 640x480 --no-banner /home/pi/Mini\ Project/picture.jpg

#fswebcam -r 640x480 -S 15 --flip h --jpeg 95 --shadow --title "Intruder" --subtitle "Detected" --info "Monitor: Active @ 1 fpm" --save /home/pi/webcam/picture.jpg -q -l 60

#fswebcam -p YUYV -d /dev/video0 -r 640x480 /home/pi/Mini\ Project/picture.jpg

fswebcam -r 640x480 -S 15 --flip h --jpeg 95 --shadow --title "Surveillance System" --save picture.jpg
