notify-send "*** script started to upload leareners ***"
sleep 1
result = $(python '/home/kolibri/Desktop/Adding_Learners/.add_learners/add_user.py' 2>&1)
zenity --info --text "Successfully added learneres! please check if all the learners are added."


