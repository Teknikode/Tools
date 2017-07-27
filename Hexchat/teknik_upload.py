__module_name__ = "Teknik Upload"
__module_version__ = "1.0.1"
__module_description__ = "Upload files to Teknik"

import_success = True

import tkinter as tk
from tkinter.filedialog import askopenfilename

try:
    import hexchat
except ImportError:
    print('This script must be run under Hexchat.')
    print('Get Hexchat now at: https://hexchat.github.io/')
    import_ok = False

# Requires Install
try:
    from teknik import uploads as teknik
except ImportError as e:
    print('Missing package(s) for %s: %s' % ('Teknik Upload', e))
    import_ok = False

def teknik_prompt():
    # Get current config values    
    apiUrl = hexchat.get_pluginpref('teknik_url')
    apiUsername = hexchat.get_pluginpref('teknik_username')
    apiToken = hexchat.get_pluginpref('teknik_auth_token')
    
    # Prompt for a file
    root = tk.Tk()
    root.withdraw()
    file_path = askopenfilename()
    
    if file_path != '':
      # Try to upload the file
      results = teknik.UploadFile(apiUrl, file_path, apiUsername, apiToken)
      
      # Either print the result to the input box, or write the error message to the window
      if 'error' in results:
        hexchat.prnt('Error: ' + results['error']['message'])
      elif 'result' in results:      
        hexchat.command("settext " + results['result']['url'])
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

if __name__ == "__main__" and import_success:
  hexchat.hook_command("TEKNIK", teknik_command, help="""Allows uploading of a file to Teknik and sharing the url directly to the chat.

Usage: TEKNIK
       TEKNIK username <username>
       TEKNIK token <auth_token>
       TEKNIK url <api_url>""")
