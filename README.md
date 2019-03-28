# AutomateGmail-using-gmail-api
Problem statement:-
  Get the emails in INBOX filtered based on the 'Date' and the 'Subject'  entered.
  
Traditional approach:-
  We search the mails in the search bar of the gmail, but we can  search only one at a time.
  imap and pop3 are also the ways to achieve this goal.
  
Solution:-
  In imap and pop3 we have to expose our credentials which breaches security.
  The developed solution uses gmail-api which gets authorized by using the client-id and client-secretkey provided for the particular
  account which enhances secure authorization.
  
Technology stack:-
  Python3.x
 
How to run:-
1. get the Google api credentials:-
	** https://developers.google.com/gmail/api/quickstart/python
		-> enable the gmail api and download the credentials.json file.
		-> store it in the working directory of the project.
2. install 'pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib'
3. run quickstart.py to get authentication to gmail account given in the above link
	-> generates a .pickle file so that subsequent executions doesnt ask for authorization again
4. install the below modules
      i)pip3 install --upgrade oauth2client
      ii)pip3 install BeautifulSoup4
      iii)pip3 install python-dateutil
5. run the gmail_read.py file and authorize again.
6. enter the Date and the subjects you want to search and get the result.
