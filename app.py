from flask import Flask, render_template, session, flash, request
import pymongo, requests


app = Flask(__name__)

connection=pymongo.MongoClient("homer.stuy.edu")
db = connection['usStats']
collection = db['usStatsCollection']

collection.drop()

file = open("populationUSA.json","r")
data = file.read()

#print(data)

#parse the data

#first remove the starting and ending [{ and }]
data = data[2:len(data)-2]

#split along }, {
data = data.split("}, {")



for index in data:
    dataDict = {}
    rowSplit = index.split(', ')
    for dataPair in rowSplit:
		colonIndex = dataPair.find(':')
		theKeyNoQuotes = dataPair[1:colonIndex-1]
		theValue = dataPair[colonIndex+2:len(dataPair)]
		theValue = theValue.strip('"')
		try:
			theValue = int(theValue)
		except:
			print 'noIntConvert'
		dataDict[theKeyNoQuotes]=theValue
    print dataDict
    collection.insert_one(dataDict)

@app.route('/')
def root():
	return render_template("base.html")
	
@app.route('/response',methods=["GET","POST"])
def response():
	lowerBound = int(request.form['lowerRange'])
	upperBound = int(request.form['upperRange'])
	cursor = collection.find({"males":{"$gt":lowerBound,"$lt":upperBound}})
	flashList = list()
	print str(lowerBound) + " | " + str(upperBound)
	print cursor
	for entry in cursor:
		print entry
		print entry['age']
		flash(entry['age'])
	return render_template("base.html")

if __name__ == "__main__":
    app.debug = True
    app.run()	
