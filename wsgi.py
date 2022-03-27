'''Import the app variable from the app.py file'''
from app.main import app
'''Python WSGI HTTP Server'''
if __name__ == '__main__':
    app.run(load_dotenv=True)