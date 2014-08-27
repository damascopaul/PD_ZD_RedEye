#!/usr/bin/env python
import requests
import datetime
import json
import requests.exceptions

TIME=datetime.datetime.utcnow()

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
	data = None
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
    	try:
    		response = requests.get(
		           'https://{0}.pagerdutsy.com/api/v1/incidents'.format(PD_SUBDOMAIN),
		           headers=headers,
		           params=parameters,
    		) 
    		response.raise_for_status()
    		data = json.loads(response.text)
    	except requests.exceptions.ConnectionError as e:
    		print '{1} : PD : There is a problem with your network. {0}'.format(e, TIME)
    	except requests.exceptions.HTTPError as e:
    		print '{1} : PD : An error occured. {0}'.format(e, TIME)
    	except requests.packages.urllib3.exceptions.ProtocolError as e:
    		print '{2} : PD : An Error Occured: {0} {1}'.format(e[0], e[1][1], TIME)
    	except Exception as e:
    		print '{1} : PD : Unexpected error: {0}'.format(e, TIME)

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
    	try:
	    	response = requests.post(
		            'https://{0}.zendesk.com/api/v2/ticksssets.json'.format(ZD_SUBDOMAIN),
		            headers=headers,
		            data=data,
		            auth=(ZD_USER, ZD_PWD),
	    	)
	    	response.raise_for_status()
	except requests.exceptions.ConnectionError as e:
    		print '{1} : ZD : There is a problem with your network. {0}'.format(e, TIME)
	except requests.exceptions.InvalidURL as e:
		print "{1} : ZD : {0}".format(e, TIME)
	except requests.exceptions.HTTPError as e:
    		print '{1} : ZD : An error occured. {0}'.format(e, TIME)
    	except Exception as e:
    		print '{1} : ZD : Unexpected error: {0}'.format(e, TIME)

#Parses and formats the json  response from the get_incidents function
#and creates a new ticket in ZenDesk for each incident.
def beautify_incidents(ugly_incidents):
	for x in range(ugly_incidents['total']):
		subject = "Cascadeo::Internal::"+str(ugly_incidents['incidents'][x]['trigger_summary_data']['subject'])
		body = "Incident: "+str(ugly_incidents['incidents'][x]['service']['name'])+": "+str(ugly_incidents['incidents'][x]['trigger_summary_data']['subject'])+"\nCreated On: "+str(ugly_incidents['incidents'][x]['created_on'])+"\nIncident URL: "+str(ugly_incidents['incidents'][x]['html_url'])+"\n\n\n"
		create_ticket(subject, body)

incidents = get_incidents()
beautify_incidents(incidents)
