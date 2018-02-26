from flask import Flask
import pymongo


app = Flask(__name__)

connection=pymongo.MongoClient("homer.stuy.edu")
db = connection['usStats']
collection = db['usStatsCollection']

droppedData = collection.drop()

print droppedData


@app.route('/')
def root():
	return('run')

if __name__ == "__main__":
    echo_app.debug = True
    echo_app.run()	
