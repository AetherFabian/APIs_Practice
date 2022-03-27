'''Import libraries of flask on pymongo databases and the os module'''
from flask_pymongo import pymongo
import os

'''Connect to the database with the user, password and the database name on .env file'''
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

'''Connecting the client of the database and saved as a db variable
   to use in the application as students database'''
client = pymongo.MongoClient(f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@api.sc4h7.mongodb.net/{DB_NAME}?retryWrites=true&w=majority')
db = client.students