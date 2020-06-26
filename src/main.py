from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ccbot import *
from messages import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.send']

keywords = ['p45', 'p-45','p125','p-125','ypt-230', 'xd9']
min_price = 120
max_price = 330

def gmailAPIsetup():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def main():
    url = f'https://www.cashconverters.es/es/es/comprar/instrumentos-musicales/pianos-y-organos/teclado-electronico/?srule=new&start=0&sz=12&cgid=1844&pmin={min_price}&pmax={max_price}'
    found,name,price,final_url,matching_keyword = fetchProduct(url,keywords)
    
    if found:
        service = gmailAPIsetup()
        sender = 'andres321duran@gmail.com'
        receiver = 'andres321duran@gmail.com'
        subject = f'CCBot | {matching_keyword} | {price}'
        message_text = f'Nombre: {name}\n\nURL: {final_url}'

        message = CreateMessage(sender, receiver, subject, message_text)
        SendMessage(service, 'me', message)
    else:
        print('Couldn\'t find any product with these keywords')
        
if __name__ == '__main__':
    main()