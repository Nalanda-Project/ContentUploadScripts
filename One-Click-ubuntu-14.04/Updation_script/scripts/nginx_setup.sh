echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

if [ $? -eq 0 ]; then

    sudo service nginx stop 2>> /home/kolibri/Desktop/Updation_script/updation.log
    echo -ne '\n' | sudo add-apt-repository ppa:nginx/stable 2>> /home/kolibri/Desktop/Updation_script/updation.log
    rm -rf /etc/nginx/sites-enabled/default 2>> /home/kolibri/Desktop/Updation_script/updation.log
    cp /home/kolibri/Desktop/Updation_script/static_files/default /etc/nginx/sites-enabled/ 2>> /home/kolibri/Desktop/Updation_script/updation.log

    rm -rf /etc/nginx/sites-available/default 2>> /home/kolibri/Desktop/Updation_script/updation.log
    cp /home/kolibri/Desktop/Updation_script/static_files/default /etc/nginx/sites-available/ 2>> /home/kolibri/Desktop/Updation_script/updation.log
    echo 's'| sudo -S apt-get update 2>> /home/kolibri/Desktop/Updation_script/updation.log
    echo 'Y'| sudo -S apt-get install nginx 2>> /home/kolibri/Desktop/Updation_script/updation.log
    echo "nginx setup done" >> /home/kolibri/Desktop/Updation_script/updation.log
    zenity --info --text="nginx setup is done."

else
  zenity --info --text="Please check your internet connection."

fi
