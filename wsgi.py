import sys
import os

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import app
application = app
