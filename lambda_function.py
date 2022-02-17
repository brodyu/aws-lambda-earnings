import json
import boto3
import pymysql

def lambda_handler(event, context):
    GET_RAW_PATH = "/getHistoricalEarnings"
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
    
    db = pymysql.connect(host=aws_url,user=aws_user, password=aws_key, database=aws_db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    # TODO implement
    if event['rawPath'] == GET_RAW_PATH:
        print("Start Request for getHistoricalEarnings")
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
        return {
            "statusCode": 200,
            "headers": {
                "content-type":"application/json"
            },
            "body": json.dumps(data)
        }
        
