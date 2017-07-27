import_success = True

import tkinter as tk
from tkinter.filedialog import askopenfilename

try:
    import weechat
except ImportError:
    print('This script must be run under WeeChat.')
    print('Get WeeChat now at: http://www.weechat.org/')
    import_ok = False

# Requires Install
try:
    from teknik import uploads as teknik
except ImportError as e:
    print('Missing package(s) for %s: %s' % ('Teknik Upload', e))
    import_ok = False

# Weechat Registration
weechat.register("Teknik Upload", "Uncled1023", "1.0", "BSDv3", "Uploads files to the Teknik Services", "", "")

def teknik_prompt():
    # Get current config values
    apiUrl = weechat.config_string(weechat.config_get('plugins.var.python.teknik.api_url'))
    apiUsername = weechat.config_string(weechat.config_get('plugins.var.python.teknik.username'))
    apiToken = weechat.config_string(weechat.config_get('plugins.var.python.teknik.token'))
    
    # Prompt for a file
    root = tk.Tk()
    root.withdraw()
    file_path = askopenfilename()
    
    if file_path != '':
      # Try to upload the file
      results = teknik.UploadFile(apiUrl, file_path, apiUsername, apiToken)
      
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
    teknik_prompt()
  else:
    argv = args.split(" ")
    command = argv[0].lower()
    
    if command == 'username':
      if len(argv) < 2:
        print("Error: You must specify a username")
      else:
        teknik_set_username(argv[1])
    elif command == 'token':
      if len(argv) < 2:
        print("Error: You must specify an auth token")
      else:
        teknik_set_token(argv[1])
    elif command == 'url':
      if len(argv) < 2:
        print("Error: You must specify an api url")
      else:
        teknik_set_url(argv[1])
    else:
      print("Error: Unrecognized Command")
  
  return weechat.WEECHAT_RC_OK

if __name__ == "__main__" and import_success:
  hook = weechat.hook_command("teknik", "Allows uploading of a file to Teknik and sharing the url directly to the chat.",
        "[username|token|url <username|auth_token|api_url>]",
        '      username: The username for your Teknik account'
        '    auth_token: The authentication token for your Teknik Account'
        '       api_url: The URL for the Upload API',
        "",
        "teknik_command", "")
