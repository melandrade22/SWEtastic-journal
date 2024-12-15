import sys
import os

# Set the project directory
project_home = '/home/swetasticfour/SWEtastic-journal'  # Update this to your app's path
if project_home not in sys.path:
    sys.path.append(project_home)

# Activate the virtual environment
activate_this = '/home/swetasticfour/.virtualenvs/myvirtualenv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Set environment variables
os.environ['YOUR_PASSWORD_VARIABLE'] = 'swe2024to25'  # Replace with your actual MongoDB password
os.environ['CLOUD_MONGO'] = '1'

# Import the application from your project
from server.endpoints import app as application  # Make sure this import is correct

application
