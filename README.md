# AWS Lambda Backend with Python and API 

## Idea
This project is an extension of our RDS ETL pipeline project. In this project, we are creating a RESTful API endpoint in Python using AWS' serverless infrastructure, Lambda. Lambda will allow us to run python code based on the occurence of an event. Here, our event will be a HTTP GET request sent through AWS' API Gateway. 

![lambda (1)](https://user-images.githubusercontent.com/45079557/154608639-53fd97bb-c3c9-4242-bde8-cc0c556abcf9.png)

## Built With
The event-driven function is built on these frameworks and platforms:
* AWS: RDS (MySQL Database), Lambda, API Gateway, S3
* Python 3.8
* PyMySQL

# GET /getHistoricalEarnings Endpoint
The data we will be returning is the most recent earnings data from the training dataset stored on our RDS database. We will query and execute commands via SQL and calculate the earnings surprise percentage for those most recent earnings events:
```sql
SELECT symbol, eps, epsEstimated, (eps - epsEstimated) / ABS(epsEstimated) * 100 AS percentSurprise
FROM train_agg
ORDER BY STR_TO_DATE(`date`, '%c/%e/%y') DESC
LIMIT 10
```

The earnings surprise percentage is calculated by taking the percentage change between the acutal EPS and the estimated EPS: 
```python
percentSurprise = (eps - eps_estimated) / eps_estimated * 100
```

## Input
HTTP requests are sent through to AWS' API Gateway tool.

Try it out:
* URL: https://mbtnvb29hk.execute-api.us-west-2.amazonaws.com
* Send a GET request to the /getHistoricalEarnings endpoint

You should recieve the following: the last 10 earnings events in our training dataset
```json
[
    {
        "symbol": "CRON",
        "eps": -0.04,
        "epsEstimated": -0.09,
        "percentSurprise": 55.55555555555556
    },
    {
        "symbol": "FCEL",
        "eps": -0.07,
        "epsEstimated": -0.02,
        "percentSurprise": -250.0
    } ...
```
# POST /predictEPS Endpoint
In our predicting-earnings-surprises repository, we trained and tested a random forest regressor that takes in 35 inputs (inputs comprised of earnings & pricing data) and saved the model as a pkl file to our AWS S3 bucket. Within our lambda function, we can now gather this model from S3 and use it to predict the EPS of an upcoming earnings annoucement. 

## Input
The POST request is sent via AWS' API Gateway and requires a request body with the 35 inputs. An example you can run:

```json
{
    "epsEstimated": -1.2,
    "time": 0,
    "open": 360.549988,
    "high": 364.089996,
    "low": 359,
    "close": 361.01001,
    "adjClose": 347.367126,
    "volume": 37900,
    "unadjustedVolume": 37900,
    "change": 0.46002,
    "changePercent": 0.128,
    "vwap": 361.36667,
    "changeOverTime": 0.00128,
    "sma_5": 345.833,
    "sma_10": 338.104,
    "sma_20": 330.254,
    "ema_5": 344.673,
    "ema_10": 339.89,
    "ema_20": 333.162,
    "volatility_5": 5.785,
    "volatility_10": 100.234,
    "rsi_14": 69.866,
    "wma_5": 346.724,
    "wma_10": 342.109,
    "wma_20": 335.98,
    "lastSurp": -2.0161290322580574,
    "last2Surp": 20.14134275618374,
    "lastEps": 3.45,
    "last2Eps": -5.6,
    "lastEst": 2.88,
    "last2Est": -2.83,
    "dow": 9,
    "month": 12,
    "day": 6,
    "year": 2022
}
```
Try it out:
* URL: https://mbtnvb29hk.execute-api.us-west-2.amazonaws.com
* Send a POST request to the /predictEPS endpoint

Running the request above yields our estimated earnings per share of:
```json
-1.326
```
