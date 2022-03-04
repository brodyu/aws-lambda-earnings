import json
import boto3
import pymysql
import pandas as pd
import pickle
import sklearn

# Connect to boto3 and pull parameters
client = boto3.client('ssm')
response = client.get_parameters(Names=[
        "/rds-pipelines/dev/aws-db-name",
        "/rds-pipelines/dev/aws-key",
        "/rds-pipelines/dev/aws-port",
        "/rds-pipelines/dev/aws-user",
        "/rds-pipelines/dev/db-url"
])
    
aws_db = response['Parameters'][0]['Value']
aws_key = response['Parameters'][1]['Value']
aws_port = response['Parameters'][2]['Value']
aws_user = response['Parameters'][3]['Value']
aws_url = response['Parameters'][4]['Value']


def rds_connect():
    db = pymysql.connect(host=aws_url,user=aws_user, password=aws_key, database=aws_db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""
        SELECT symbol, eps, epsEstimated, (eps - epsEstimated) / ABS(epsEstimated) * 100 AS percentSurprise
        FROM train_agg
        ORDER BY STR_TO_DATE(`date`, '%c/%e/%y') DESC
        LIMIT 10
        """)
    data = cursor.fetchall()
    # Close cursor and connection
    cursor.close()
    db.close()
    return data


def s3_connect():
    print("Trying to connect model")
    s3_client = boto3.client("s3")
    
    #Using Pickle + load model from s3
    filename = "earnings_surprise_random_forest.pkl"
    s3_client.download_file('rfmodelpkl', filename, '/tmp/' + filename)  
    loaded_model = pickle.load(open('/tmp/' + filename, 'rb'))
    return loaded_model


def lambda_handler(event, context):
    GET_RAW_PATH = "/getHistoricalEarnings"
    POST_RAW_PATH = "/predictEPS"

    # TODO implement
    if event['rawPath'] == GET_RAW_PATH:
        print("Start Request for getHistoricalEarnings")
        data = rds_connect()
        return {
            "statusCode": 200,
            "headers": {
                "content-type":"application/json"
            },
            "body": json.dumps(data)
        }
    elif event['rawPath'] == POST_RAW_PATH:
        print("Start Request for predictEPS")
        decoded_event = json.loads(event["body"])
        # Manipulate input for model reading
        input_df = pd.Series(decoded_event).to_frame().T
        # Gather loaded model from S3
        loaded_model = s3_connect()
        # Predict with input data using S3 model
        result = loaded_model.predict(input_df)[0]
        return {
            "statusCode": 200,
            "headers": {
                "content-type":"application/json"
            },
            "body": json.dumps(result)
        }