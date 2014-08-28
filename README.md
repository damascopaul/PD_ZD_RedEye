slee.py
=======

Python script to create ZenDesk tickets from PagerDuty incidents that occurred on a certain time range. Uses ZenDesk and PagerDuty API calls.

###Requirements

####Python Version
Use Python version 2.6 and later.

####Python Libraries
Make sure the following Python Libraries are installed on your system:
* ```requests``` - available in https://github.com/kennethreitz/requests
* ```datetime``` - new in Python version 2.3
* ```json``` - new in Python version 2.6

###Configuration
Be sure to set the global variables before running the script.

Global variable      | Description
-------------------- | -----------
PD_SUBDOMAIN         | PagerDuty Subdomain Name
PD\_API\_ACCESS_KEY  | PD API Token
ZD_SUBDOMAIN			 | ZenDesk Subdomain Name
ZD_USER				 | ZenDesk Username
ZD_PWD			   		 | ZenDesk Password
ZD_REQUESTER			 | The User ID of the Requester when creating a new ticket
ZD_GROUP				 | The Group ID of the assignee of the new ticket
ZD_ASSIGNEE			 | The User ID of the assignee of the new ticket


###Usage
You can run the script on the terminal manually or run it as a cron job.

####Terminal Command
Run the script on the terminal using the command: 
```$ python slee.py```

####Cron Job
The script can be run as a cron job. You can also pipe the message outputs to a logfile if you want.

Example:

```00 08 * * * /path/to/file/slee.py >> /var/log/sleepy.log```