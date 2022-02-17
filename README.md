# AWS Lambda Backend with Python and API 

## Idea
This project is an extension of our RDS ETL pipeline project. In this project, we are creating a RESTful API endpoint in Python using AWS' serverless infrastructure, Lambda. Lambda will allow us to run python code based on the occurence of an event. Here, our event will be a HTTP GET request sent through AWS' API Gateway. 

## Built With
The event-driven function is built on these frameworks and platforms:
* AWS: RDS (MySQL Database), Lambda, API Gateway, Parameter Store
* Python 3.8
* PyMySQL

## Data
The data we will be returning is the most recent earnings data from the training dataset stored on our RDS database. We will query and execute commands via SQL and calculate the earnings surprise percentage for those most recent earnings events. 

The earnings surprise percentage is calculated by taking the percentage change between the acutal EPS and the estimated EPS: 
```Python
percentSurprise = (eps - eps_estimated) / eps_estimated * 100
```
