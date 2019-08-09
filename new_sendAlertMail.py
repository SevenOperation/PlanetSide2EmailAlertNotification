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
worldIDToName={'13':'Cobalt'}
rawHtmlFile = ""
config = yaml.load(open('config.yaml','r').read())['Config']

async def hello(): 
	global serverstats,rawHtmlFile, config
	async with websockets.connect('wss://push.planetside2.com/streaming?environment=ps2&service-id=s:'+config['ServiceId']+'',ssl=True) as ws:
		name='{ "service":"event", "action":"subscribe", "worlds":["'+config['WorldId']+'"], "eventNames":["MetagameEvent"] }'
		await ws.send(name)
		print (f"> {name}")
		
		while True :
			event = await ws.recv()
			f = open("log.txt",'a')
			eventJ = json.loads(event)
			if 'payload' in eventJ:
				alert = False
				if eventJ['payload']['metagame_event_id'] in eventTypes['Events']:
					if "lock" in str(eventTypes['Events'][eventJ['payload']['metagame_event_id']]):
						alert = True
					event = eventTypes['Events'][eventJ['payload']['metagame_event_id']]
					event['state'] = eventJ['payload']['metagame_event_state_name']
					print(event)
					print(eventTypes['Events'][eventJ['payload']['metagame_event_id']])
					event = "<table border='1'><tr><td>"+event['description']+"</td><td>"+event['name']+"</td><td>"+event['state']+"</td></tr></table>"
					event = rawHtmlFile.replace('content',event)
					continent = "unkown"
					if alert:
						continent = str(eventTypes['Events'][eventJ['payload']['metagame_event_id']]).split('lock ')[1].split('"')[0]
						print(continent)
					sendEventMail(event,alert,continent)
				else:
					event = eventTypes['Events'][eventJ['payload']['metagame_event_id']]
					event['state'] = eventJ['payload']['metagame_event_state_name']
					print(event)
					event = "<table border='1'><tr><td>"+event['description']+"</td><td>"+event['name']+"</td><td>"+event['state']+"</td></tr></table>"
					event = rawHtmlFile.replace('content',event)
					sendEventMail(event,alert,"unkown")
				#print (event['meta_event_state_name'])
			#if "detail" not in event and "online" in event:
			#	if serverstats != event['online']:
			#		serverstats=event['online']
			#		sendServerStateChangeMail()
			if "heartbeat" not in json.dumps(eventJ):
				f.write(json.dumps(eventJ))
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
		sendErrorMail(str(traceback.format_exc()))
		connect()

def sendEventMail(event,alert,continent):
	msg = EmailMessage()
	msg['From'] = config['MailSenderAddress']
	mail_domain = config['MailDomain']
	server = smtplib.SMTP(config['MailServerIP'],25,"mail_domain",10)
	server.set_debuglevel(1)
	msg.add_alternative(event,subtype='html')
	#msg.set_content(json.dumps(event))
	db = MySQLdb.connect(host=config['DatabaseIP'],db=config['DatabaseUser'].password=config['DatabasePassword'])
	cnx = db.cursor()
	time = dt.datetime.now().hour
	endNotification=""
	if 'ended' in event:
		endNotification=' and planetside2Settings.endNotification=1'
	if alert:
		if config['UseDatabase']:
			continent = "planetside2Settings."+continent.lower()+"Notification=1 and"
			print(continent)
			cnx.execute('Select email from user Left Join planetside2Settings on user.id=planetside2Settings.userId where planetside2Settings.notificationEnabled=1 and user.id = planetside2Settings.userId and planetside2Settings.notificationStartHour <= '+str(time)+' and planetside2Settings.notificationEndHour>='+str(time) + endNotification + ' and ' + continent +" planetside2Settings.notificationEnabled=1")	
			recipients=[]
			print(cnx)
			for row in cnx.fetchall():
				if row[0] != None:
        				recipients.append(row[0])
		else:
			recipients = config['Recipients']
			if 'ended' in event and !config['EndAlertNotification']:
				recipients = []
		print(recipients)
		if recipients != [] :
			msg['Subject']="WARNING Alert has started in Planetside 2 on "
			msg['To']="Alert Subscribers"
			server.sendmail(msg['From'],recipients,msg.as_string())
	else:
		if config['UseDatabase']:
			cnx.execute('Select email from user Left Join planetside2Settings on user.id=planetside2Settings.userId where planetside2Settings.notificationEnabled=1 and user.id = planetside2Settings.userId and planetside2Settings.alertNotificationOnly=0 and planetside2Settings.notificationStartHour<='+str(time)+' and planetside2Settings.notificationEndHour>='+str(time)+endNotification)	
			print(cnx)
			recipients=[]
			for row in cnx.fetchall():
				if row[0] != None:
        				recipients.append(row[0])
		elif !config['Alert']:
			recipients = config['Recipients']
                        if 'ended' in event and !config['EndAlertNotification']:
                                recipients = []
		print(recipients)
		if recipients != [] :
			msg['Subject']="New Event has started"
			msg['To']="EventSubscribers"
			server.sendmail(msg['From'],recipients,msg.as_string())
	server.quit()

def sendErrorMail(error):
	msg = EmailMessage()
	msg['From'] = config['ErrorSender']
	maildomain = config['MailDomain']
	server = smtplib.SMTP(config['MailServerIP'],25,maildomain,10)
	server.set_debuglevel(1)
	msg['Subject'] = "An error occured"
	msg['To'] = "Admin"
	msg.set_content(error)
	server.sendmail(msg['From'],config['ErrorRecipient'],msg.as_string())






#server = sys.argv[1]
connect()
#main(server)
