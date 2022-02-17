# AWS Lambda Backend with Python and API 

## Idea
This project is an extension of our RDS ETL pipeline project. In this project, we are creating a RESTful API endpoint in Python using AWS' serverless infrastructure, Lambda. Lambda will allow us to run python code based on the occurence of an event. Here, our event will be a HTTP GET request sent through AWS' API Gateway. 

## Built With
The event-driven function is built on these frameworks and platforms:
* AWS: RDS (MySQL Database), Lambda, API Gateway, Parameter Store
* Python 3.8
* PyMySQL

## Data
The data we will be returning is the most recent earnings data from the training dataset stored on our RDS database. We will query and execute commands via SQL and calculate the earnings surprise percentage for those most recent earnings events:
``` sql
SELECT symbol, eps, epsEstimated, (eps - epsEstimated) / ABS(epsEstimated) * 100 AS percentSurprise
FROM train_agg
ORDER BY STR_TO_DATE(`date`, '%c/%e/%y') DESC
LIMIT 10
```

The earnings surprise percentage is calculated by taking the percentage change between the acutal EPS and the estimated EPS: 
```Python
percentSurprise = (eps - eps_estimated) / eps_estimated * 100
```

## Input
HTTP requests are sent through to AWS' API Gateway tool. The gateway is setup to only accept GET requests at the moment.

<img width="714" alt="Screen Shot 2022-02-16 at 10 15 36 PM" src="https://user-images.githubusercontent.com/45079557/154433766-246d1e70-c3d0-45f7-af51-21a099ce3016.png">
