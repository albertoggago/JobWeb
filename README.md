# Job Web

## 1 OBJECTIVE

This project has the objetive of review all Jobs recived, looking for all information of pages (scraping) and generate a model predictive for get a score of No flag jobs  

## 2 Division of project

The project contains tree parts 
1 - Server python to review emails and create predicted model
2 - Server express-node.js for generate RESTfull service
3 - Web-Application angular4 for read all Jobs inside project


### 2.1 Servers Python

The system contains with 2 servers.

1 - readEmails

This process execute load information inside MongodDB.
You must create in pytonBatch/pyproj/config/configOk.json

file with this structure: 
{
	"fromEmail" : "myaccout@serveremail.com",
	"sslServer" : "userMail",
	"pwdServer" : "pwdMail",
	"url" :  "mongodb://user:password@urlMongodb:port/nameDB?aditionaParameters",
	"nameDB" : "nameDB"
}

Run script into MongoDB in nameDB.correoUrl for system works
	/mongoDB/initMongoDB.js 


2. Process Model  