#!/usr/bin/env python
import requests
import datetime
import json

#PagerDuty Specific Variables
PD_SUBDOMAIN=''
PD_API_ACCESS_KEY=''

#ZenDesk Specific Variables
ZD_SUBDOMAIN=''
ZD_USER=''
ZD_PWD=''
ZD_REQUESTER=''
ZD_GROUP=''
ZD_ASSIGNEE=''

#Gets all the PagerDuty incidents 
#from 8am yesterday to 12mn today (UTC)
def get_incidents():
	TIME=datetime.datetime.now()
	T_SINCE=str(TIME.year)+"-"+str(TIME.month)+"-"+str(TIME.day-1)+"T08:00Z"
	T_UNTIL=str(TIME.year)+"-"+str(TIME.month)+"-"+str(TIME.day)+"T00:00Z"

    	headers = {
        		'Authorization': 'Token token={0}'.format(PD_API_ACCESS_KEY),
        		'Content-type': 'application/json',
    	}
    	parameters = {
	        	'status':'triggered',
	        	'time_zone':'Singapore',
	        	'since':T_SINCE,
	        	'until':T_UNTIL,
	        	'sort_by':'created_on:asc',
	        	'fields':'incident_number,created_on,service,trigger_summary_data,html_url',
    	}
    	response = requests.get(
	            'https://{0}.pagerduty.com/api/v1/incidents'.format(PD_SUBDOMAIN),
	            headers=headers,
	            params=parameters,
    	)
    	data = json.loads(response.text)

    	return data

#Creates a ticket in Zendesk
def create_ticket(subject, body):
	headers = {
        		'Content-type': 'application/json',
    	}
    	ticket = {
    		'ticket':{
    			'requester_id':ZD_REQUESTER,
    			'subject':subject,
    			'type':'incident',
    			'priority':'urgent',
    			'group_id':ZD_GROUP,
    			'assignee_id':ZD_ASSIGNEE,
    			'comment':{
    				'body':body
    			}
    		}
    	}
    	data = json.dumps(ticket)
    	response = requests.post(
	            'https://{0}.zendesk.com/api/v2/tickets.json'.format(ZD_SUBDOMAIN),
	            headers=headers,
	            data=data,
	            auth=(ZD_USER, ZD_PWD),
    	)

#Parses the json formatted response from the get_incidents function
#and creates a new ticket in ZenDesk for each incident.
def beautify_incidents(ugly_incidents):
	for x in range(ugly_incidents['total']):
		subject = "Cascadeo::Internal::"+str(ugly_incidents['incidents'][x]['trigger_summary_data']['subject'])
		body = "Incident: "+str(ugly_incidents['incidents'][x]['service']['name'])+": "+str(ugly_incidents['incidents'][x]['trigger_summary_data']['subject'])+"\nCreated On: "+str(ugly_incidents['incidents'][x]['created_on'])+"\nIncident URL: "+str(ugly_incidents['incidents'][x]['html_url'])+"\n\n\n"
		create_ticket(subject, body)

incidents = get_incidents()
beautify_incidents(incidents)
