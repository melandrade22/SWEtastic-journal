# Import the application from your project
# Make sure this import is correct
from server.endpoints import app as application
import sys
import os

# Set the project directory
# Update this to your app's path
project_home = '/home/swetasticfour/SWEtastic-journal'
if project_home not in sys.path:
    sys.path.append(project_home)

# Activate the virtual environment
activate_this = ("/home/swetasticfour/.virtualenvs/" +
                 "myvirtualenv/bin/activate_this.py")
exec(open(activate_this).read(), {'__file__': activate_this})

# Set environment variables
# Replace with your actual MongoDB password
os.environ['YOUR_PASSWORD_VARIABLE'] = 'swe2024to25'
os.environ['CLOUD_MONGO'] = '1'

application
