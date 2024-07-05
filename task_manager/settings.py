import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['webserver', 'your-render-app-url.onrender.com']

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
