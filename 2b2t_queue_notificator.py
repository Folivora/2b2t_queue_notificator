#!/usr/bin/env python3

##    When you are in the 2b2t queue the server sends a message about the current
## position in the queue to the in-game chat every 5 seconds.
## The MultiMC launcher writes all the chat messages to its log file (plain text format).
##    This script reads the last few lines (50 by default) from the log file every 5 seconds
## and parse it to find information about the current position in the queue. 
## Notification in Telegram is sent if the current position is less than or equal
## to the position for which notification sending is selected. If the substring "Connected to the server." 
## is found, a notification about that will be sent, after which the script will be terminated.
##
## Tested with MultiMC launcher 0.7.0-4218, python 3.9.2 (but must work with lower versions too).
## 
##
## Made by CoffeeUtilizer (minecraft nickname) Feb 18 2025.
## Give me a priority pass
##
##                              ░░░░░░░░░░░
##                          ░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▓░░         ░░░░░▒▒▓▓▓▒░░░
##                       ░░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒░░
##                     ░▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##                   ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
##                  ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##                 ░▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░
##                ░▓▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░
##               ░▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##              ░░▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░
##              ░▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░
##           ░░▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒░
##        ░░░▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
##       ░░▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
##      ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░
##     ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░▒▒░░▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##    ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓░░
##   ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▓▓▒▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▓░░░
##  ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░
##  ░░▒▒▒▓▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
## ░░▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓░░
## ░▒▒▒▓▓▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▓▒░
##░░▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░                ░░░░░
##░▓▒▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░             ░░▒▒▒▒▒▒░░▓░░
##░▓▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░           ░▓▒▒▓▓▒▒▒▓▓▒▒▒░
##░▓▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░          ░▓▒▒▒▓▒▒▒▒▓▓▒▒░░
##░▓▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓░  ░▒▒▒▒░  ░░▒▒▒▒▓▒▒▒▒▓▓▒▒▒░
##░▓▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▓▓░ ░▓▒▒▒▓▒  ░▒▒▒▒▓▓▒▒▒▓▓▒▒▒░
##░░▒▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▓▓░  ░▓▒▒▒▓░ ░▒▓▒▒▒▓▒▒▒▓▓▒▒▓░
## ░▒▒▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓░░    ░▓▓▒▒▓░░▓▒▒▒▒▒▒▒▒▒▒▒▓░░
## ░░▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░       ░▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒░░
##  ░▒▒▒▓▓▓▒▓▓▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓░      ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░
##  ░░▒▒▒▒▒▒▓▒▓▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▒▒▒▓▓▒▒▓▓▓▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▒░░    ░▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒░
##   ░░▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▓▒▒▓▒▒▓▓▒▒▓▒▒▓▓▒▒▒▒░░░░░    ▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░
##      ░░▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▓▒▒▒▓▒▒▓▓▒▓▓▓▒▒▓▒▓▓▒▓▓░        ░▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##          ░░▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▓▓▒▓▒▒▒▒▓▒▒▓▓▒▒▓▒▒▒▓▒▒▓▒▒▓░      ░▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##              ░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▓▓▓▒▒▒▒▓▒▒▒▓▒▓▒▒▒▒▓▒▓▓▒▒▒▓░     ░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##                     ░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▒▒▒▒▒░      ░░▓▓▒▒▒▒▒▒▒▒▓▓▓░░
##                                ░░░░░░░░░░░▒▒▒▒▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░       ░░░▒░▒▒▒▒░░░░░
##                                           ░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##                                             ░░▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░
##                                              ░░▓▒▒▒▒▒▒▒▒▓▓▓▓▒░░
##                                                 ░░▒▓▒▒▒▒▒▒░░
##



import requests
import os.path
import time

## The list of position numbers in the queue for which the notification will be sent.
## These are the thresholds. In other words, the notification will be sent (only once for each value in the list)
## if the current queue position number is less than or equal to the value taken from this list.
alarms_position = [1,2,3,4,5,10,20,50,100]


# MultiMC logfile path
Launcher_LogFile="/home/<user>/.local/share/multimc/instances/<instance_name>/.minecraft/logs/latest.log"

# Telegram's endpoint info
TOKEN   = "<bot_token>"
CHAT_ID = "<chat_id>"



def parseLogsToGetQueuePosition():

    if not os.path.exists(Launcher_LogFile):
        print('Log file \"'+Launcher_LogFile+'\" does not exist!')
        exit(1)

    N = 50
    while True:

        # opening file using with() method so that file get closed after completing work
        with open(Launcher_LogFile) as file:

            # loop to read iterate last N lines
            for line in (file.readlines() [-N:]):

                if "Connected to the server." in line :
                    MESSAGE = "We've connected to the server. Shutting down the script."
                    sendTelegramNotification(MESSAGE)
                    exit(0)

                # Parse the line to get queue position
                pattern1="Position in queue: "
                pattern2="\\nYou can purchase priority queue"
                try:
                    q_position = line.split(pattern1,1)[1]         # retain the part after the pattern1
                    q_position = q_position.split(pattern2,1)[0]   # retain the part before the pattern2
                    print(q_position)
                except IndexError:
                    continue

                # Checking whether an alarm needs to be sent for the current position
                sent_alarms_position = []
                for i in range(len(alarms_position)):
                    if int(q_position) <= int(alarms_position[i]):
                        MESSAGE = "Current 2b2t queue position is: <b>"+str(q_position)+"</b>"
                        sendTelegramNotification(MESSAGE)
                        sent_alarms_position.append(alarms_position[i])

                if sent_alarms_position:
                    for i in range(len(sent_alarms_position)):
                        alarms_position.remove(sent_alarms_position[i])

        time.sleep(5)


def sendTelegramNotification(MESSAGE):

    url = "https://api.telegram.org/bot"+TOKEN+"/sendMessage?chat_id="+CHAT_ID+"&parse_mode=HTML&text="+MESSAGE
    response = requests.post(url)
    #print(response.json())


def main():
    parseLogsToGetQueuePosition()

if __name__ == '__main__':
    main()
