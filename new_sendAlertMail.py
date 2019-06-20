#!/usr/bin/env python
import requests
import asyncio
import pathlib
import ssl
import websockets
import sys
import smtplib
import json
import yaml
from email.message import EmailMessage
import MySQLdb
import datetime as dt
import traceback

serverstats = {}
eventTypes={}
eventFile = open('metagame.yaml','r')
eventTypes=yaml.load(eventFile.read())
configFile open('config.yaml','r')
config = yaml.load(configFile.read())
worldIDToName={'13':'Cobalt'}
rawHtmlFile = ""

async def hello(): 
	global serverstats,rawHtmlFile
	async with websockets.connect('wss://push.planetside2.com/streaming?environment=ps2&service-id=s:'+config['ServiceId']+'',ssl=True) as ws:
		name='{ "service":"event", "action":"subscribe", "worlds":['+config["WorldId"]'], "eventNames":["MetagameEvent"] }'
		await ws.send(name)
		print (f"> {name}")
		
		while True :
			event = await ws.recv()
			f = open("log.txt",'a')
			event = json.loads(event)
			if 'payload' in event:
				alert = False
				if event['payload']['metagame_event_id'] in eventTypes['Events']:
					if "lock" in str(eventTypes['Events'][event['payload']['metagame_event_id']]):
						alert = True
					event = "<table border='1'><tr><td>"+event['description']+"</td><td>"+event['name']+"</td></tr></table>"
					event = rawHtmlFile.replace('content',event)
					sendEventMail(event,alert)
				else:
					event = "<table border='1'><tr><td>"+event['description']+"</td><td>"+event['name']+"</td></tr></table>"
					event = rawHtmlFile.replace('content',event)
					sendEventMail(event,alert)
				#print (event['meta_event_state_name'])
			#if "detail" not in event and "online" in event:
			#	if serverstats != event['online']:
			#		serverstats=event['online']
			#		sendServerStateChangeMail()
			if "heartbeat" not in json.dumps(event):
				f.write(json.dumps(event))
				print(event)
			f.close()

def connect():
	global rawHtmlFile
	f = open("alert_mail.html",'r')
	rawHtmlFile = f.read()
	f.close()
	try:
		asyncio.get_event_loop().run_until_complete(hello())
	except:
		print(str(traceback.format_exc()))
		asyncio.get_event_loop().run_until_complete(hello())

def sendEventMail(event,alert):
	msg = EmailMessage()
	msg['From'] = config['MailSenderAddress']
	mail_domain = config['MailDomain']
	server = smtplib.SMTP(config['MailServerIP'],25,"mail_domain",10)
	server.set_debuglevel(1)
	msg.set_content(json.dumps(event))
	recipients = []
	time = dt.datetime.now().hour
	endNotification = ""
	db = MySQLdb.connect(host=config['DatabaseIP'],db=config['DatabaseUser'].password=config['DatabasePassword'])
	cnx = db.cursor()
	if 'ended' in event:
		endNotification=' and  ps2SendEndMail=1'
	if alert :
		if config['UseDatabase']
			cnx.execute('Select email from user where ps2NotificationsEnabled=1 and ps2NotificationType=1 and ps2NotificationStartTime <= '+str(time)+' and ps2NotificationEndTime>='+str(time)+endNotification)
			for row in cnx.fetchall():
                        	if row[0] != None:
                                	recipients.append(row[0])	
		else:
			recipients = config['Recipients']
			if 'ended' in event and !config['EndAlertNotification']:
				recipients = []
		if recipients != [] :
                        msg['Subject']="WARNING Alert has started in Planetside 2 on " #+ rawText.split['to lock'][1] 
                        msg['To']="Alert Subscribers"
                        server.sendmail(msg['From'],recipients,msg.as_string())	
	else:
		if config['UseDatabase']
			cnx.execute('Select email from user where ps2NotificationsEnabled=1 and ps2NotificationType=0 and ps2NotificationStartTime <= '+str(time)+' and ps2NotificationEndTime>='+str(time)+endNotification)	
			for row in cnx.fetchall():
				if row[0] != None:
        				recipients.append(row[0])
		elif !config['Alert']:
			recipients = config['Recipients']
			if recipients != [] :
				msg['Subject']="New Event has started"
				msg['To']="EventSubscribers"
				server.sendmail(msg['From'],recipients,msg.as_string())
	server.quit()

#server = sys.argv[1]
connect()
#main(server)
