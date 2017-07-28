#!/usr/bin/python
import_success = True

import os
import Tkinter as tk
import tkFileDialog

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_success = False

# Requires Install
try:
    from teknik import uploads as teknik
except ImportError as e:
    print('Missing package(s) for %s: %s' % ('Teknik Upload', e))
    import_success = False

# Weechat Registration
weechat.register("Teknik", "Uncled1023", "1.0.0", "BSDv3", "Interact with the Teknik Services", "", "")

def teknik_prompt(file):
    # Get current config values
    apiUrl = weechat.config_string(weechat.config_get('plugins.var.python.teknik.api_url'))
    apiUsername = weechat.config_string(weechat.config_get('plugins.var.python.teknik.username'))
    apiToken = weechat.config_string(weechat.config_get('plugins.var.python.teknik.token'))
    
    if file is not None and os.path.exists(file):
      # Try to upload the file
      results = teknik.UploadFile(apiUrl, file, apiUsername, apiToken)
      
      # Either print the result to the input box, or write the error message to the window
      if 'error' in results:
        print('Error: ' + results['error']['message'])
      elif 'result' in results:      
        buffer = weechat.current_buffer()
        weechat.buffer_set(buffer, 'input', results['result']['url'])
      else:
        print('Unknown Error')

def teknik_set_url(url):
  weechat.config_set_plugin('plugins.var.python.teknik.api_url', url)
  
def teknik_set_token(token):
  weechat.config_set_plugin('plugins.var.python.teknik.token', token)

def teknik_set_username(username):
  weechat.config_set_plugin('plugins.var.python.teknik.username', username)
      
def teknik_command(data, buffer, args):
  args = args.strip()
  if args == "":
    print("Error: You must specify a command")
  else:
    argv = args.split(" ")
    command = argv[0].lower()
    
    # Upload a File
    if command == 'upload':
      if len(argv) < 2:
        print("Error: You must specify a file")
      else:
        teknik_prompt(argv[1])
        
    # Set a config option
    elif command == 'set':
      if len(argv) < 2:
        print("Error: You must specify the option to set")
      else:
        option = argv[1].lower()
        if option == 'username':
          if len(argv) < 3:
            print("Error: You must specify a username")
          else:
            teknik_set_username(argv[2])
        elif option == 'token':
          if len(argv) < 3:
            print("Error: You must specify an auth token")
          else:
            teknik_set_token(argv[2])
        elif option == 'url':
          if len(argv) < 3:
            print("Error: You must specify an api url")
          else:
            teknik_set_url(argv[2])
        else:
          print("Error: Unrecognized Option")
    else:
      print("Error: Unrecognized Command")
  
  return weechat.WEECHAT_RC_OK

if __name__ == "__main__" and import_success:
  hook = weechat.hook_command("teknik", "Allows uploading of a file to Teknik and sharing the url directly to the chat.",
        "[upload <file>] | [set username|token|url <username|auth_token|api_url>]",
        '          file: The file you want to upload'
        '      username: The username for your Teknik account'
        '    auth_token: The authentication token for your Teknik Account'
        '       api_url: The URL for the Upload API',
        "",
        "teknik_command", "")
