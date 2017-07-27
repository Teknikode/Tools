__module_name__ = "Teknik Upload"
__module_version__ = "1.0"
__module_description__ = "Upload files to Teknik"

import hexchat
import base64
import json
import tkinter as tk
from tkinter.filedialog import askopenfilename

# Requires Install
import requests

defaultUrl = 'https://api.teknik.io/v1/Upload'
defaultUsername = ''
defaultToken = ''

def teknik_prompt():
    # Get current config values
    apiUrl = defaultUrl
    apiUsername = defaultUsername
    apiToken = defaultToken
    
    cfgUrl = hexchat.get_pluginpref('teknik_url')
    if cfgUrl is not None:
      apiUrl = cfgUrl
    
    cfgUsername = hexchat.get_pluginpref('teknik_username')
    if cfgUsername is not None:
      apiUsername = cfgUsername
    
    cfgToken = hexchat.get_pluginpref('teknik_auth_token')
    if cfgToken is not None:
      apiToken = cfgToken
    
    # Prompt for a file
    root = tk.Tk()
    root.withdraw()
    file_path = askopenfilename()
    
    if file_path != '':
      # Create the request
      files = {'file': open(file_path, "rb")}
      
      # Create a header if they have added auth info
      headers = {}
      if apiUsername != '' and apiToken != '':
        encAuth = base64.b64encode(apiUsername + ':' + apiToken)
        headers = {'Authorization': 'Basic ' + encAuth}
      
      r = requests.post(apiUrl, files=files, headers=headers)
      jObj = json.loads(r.text)
      
      # Either print the result to the input box, or write the error message to the window
      if 'error' in jObj:
        hexchat.prnt('Error: ' + jObj['error']['message'])
      elif 'result' in jObj:      
        hexchat.command("settext " + jObj['result']['url'])
      else:
        hexchat.prnt('Unknown Error')

def teknik_set_url(url):
  hexchat.set_pluginpref('teknik_url', url)
  
def teknik_set_token(token):
  hexchat.set_pluginpref('teknik_auth_token', token)

def teknik_set_username(username):
  hexchat.set_pluginpref('teknik_username', username)
      
def teknik_command(word, word_eol, userdata):
  if len(word) < 2:
    teknik_prompt()
  else:
    command = word[1].lower()
    
    if command == 'username':
      if len(word) < 3:
        hexchat.prnt("Error: You must specify a username")
      else:
        teknik_set_username(word[2])
    elif command == 'token':
      if len(word) < 3:
        hexchat.prnt("Error: You must specify an auth token")
      else:
        teknik_set_token(word[2])
    elif command == 'url':
      if len(word) < 3:
        hexchat.prnt("Error: You must specify an api url")
      else:
        teknik_set_url(word[2])
    else:
      hexchat.prnt("Error: Unrecognized Command")
  
  return hexchat.EAT_ALL

hexchat.hook_command("TEKNIK", teknik_command, help="""Allows uploading of a file to Teknik and sharing the url directly to the chat.

Usage: TEKNIK
       TEKNIK username <username>
       TEKNIK token <auth_token>
       TEKNIK url <api_url>""")
