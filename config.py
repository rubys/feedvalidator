# Default URL of the validator itself... feel free to beautify as you like
import os
HOMEURL = 'http://' + os.environ['HTTP_HOST'] + os.environ['SCRIPT_NAME']

# This following value is primarily used for setting up the other values...
HOMEDIR = r'/home/rubys'

# This is where local python libraries are installed.  This may be useful
# for locating a locally installed libxml2 library, for example...
PYDIR  = HOMEDIR + r'/lib/python/'

# This is where the CGI itself is... other supporting scripts (like
# feedfinder) may be placed here.
WEBDIR = HOMEDIR + r'/public_html/feedvalidator'

# This is where the feedvalidator code lives...
SRCDIR = WEBDIR + r'/src'
