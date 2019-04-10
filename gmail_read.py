# Importing required libraries
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
import csv
from operator import itemgetter
import re

def gmailRead():

	## To authorize your account
	SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
	store = file.Storage('storage.json') 
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

	## Enter the date to filter the messages retrieved
	user_date = input("Enter the date from which you want to check the sent feed (yyyy-mm-dd): ")

	## functionaity to get the sent mails after a particular date
	## Recipient	Date		Subject
	subject_list = [ ]
	no_of_terms = input("\nEnter the no. of subjects u want to search: ")
	no_of_terms = int(no_of_terms)
	print("\nenter the key terms in subjects u wanna search for one by one ")

	for i in range(no_of_terms):
		temp_subject = input("subject: ")
		subject_list.append(temp_subject)

	## Selecting the account and the label u want to perform the action on
	user_id = 'me'
	label_id = 'INBOX'
	final_list = [ ]

	## forming the query for different subjects
	q = 'in:inbox after:'+ user_date
	for item in subject_list:
		q = q+' subject:'+'('+item+')'+ ' OR'
	q=q[0:-2]

	## Getting all the mails from the label-id selected
	response = GMAIL.users().messages().list(userId=user_id, labelIds=[label_id], q = q).execute()
	messages = [ ]
	if 'messages' in response:
		messages.extend(response['messages'])
	while 'nextPageToken' in response:
		page_token = response['nextPageToken']
		response = GMAIL.users().messages().list(userId=user_id, labelIds=[label_id], pageToken=page_token, q = q).execute()
		messages.extend(response['messages'])

	##fetch the mails based on label-id u mention
	for mssg in messages:
		temp_dict = { }
		m_id = mssg['id']
		message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
		#print(message)
		payld = message['payload']
		#print(payld)
		headr = payld['headers']
		#print(headr)

		for one in headr:
			if one['name'] == 'Subject':
				msg_subject = one['value'].upper()
				temp_dict['Subject'] = msg_subject
			else:
				pass

		for two in headr:
			if two['name'] == 'Date':
				msg_date = two['value']
				date_parse = (parser.parse(msg_date))
				m_date = (date_parse.date())
				temp_dict['Date'] = str(m_date)
			else:
				pass
				
		for three in headr:
			if three['name'] == 'From':
				msg_from = three['value']
				temp_dict['Sender'] = msg_from
			else:
				pass
		
				
		for three in headr:
			if three['name'] == 'To':
				msg_from = three['value']
				temp_dict['Recipient'] = msg_from
			else:
				pass
		
		temp_dict['Snippet'] = message['snippet']

		try:
			mssg_parts = payld['parts']
			part_one  = mssg_parts[0]
			part_body = part_one['body']
			part_data = part_body['data']
			clean_one = part_data.replace("-","+")
			clean_one = clean_one.replace("_","/")
			clean_two = base64.b64decode (bytes(clean_one, 'UTF-8'))
			soup = BeautifulSoup(clean_two , "lxml" )
			mssg_body = soup.body()
			temp_dict['Message_body'] = mssg_body
		except :
			pass
		## append to the finalList each time
		final_list.append(temp_dict)

	# print(final_list)

	## extract the 'Subject's from the final_list
	subject_list = [i["Subject"] for i in final_list]

	# print(subject_list)

	## splitting the subject into words/key terms
	i=0
	subject_dict = { }
	for item in subject_list:
		split_list = re.split(r'\s',item)
		subject_dict[i]=split_list
		i= i+1

	# print(subject_dict)

	project_dict = [ ]
	for key, value in subject_dict.items():
		for item in value:
			temp = re.compile(r't(.*)e|s(.*)p|gal|a(.*)e',re.I)
			if temp.search(item) is not None:
				project_dict.append(temp.search(item).group(0))

	## remove the duplicate items in the list
	project_dict = set(project_dict)
	##Convert to the list back again
	project_list = list(project_dict)
	# print(project_list)

	## to verify successfull completion of the task
	flag = 0

	## output the required output to the csv file
	with open('final.csv','w', newline='') as csvfile:
		csvfile.write("project\n")
		for entry in project_list:
			csvfile.write(entry)
			csvfile.write("\n")
			flag = 1

	if(flag):
		print("\n\nSuccessfull........\n\nOutput can be found in the \'final.csv\' file in the same directory...")




gmailRead()