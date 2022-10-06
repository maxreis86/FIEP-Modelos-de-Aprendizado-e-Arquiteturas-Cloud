def lambda_handler(event, context):
    import h2o
    import pandas as pd
    import boto3
    import awswrangler as wr
    import json
    
    #Best Model ID:
    BestModelId='StackedEnsemble_BestOfFamily_4_AutoML_1_20221006_02202.zip'
    
    #Keep the ratings ranges updated
    def ratings(p1):
        if p1 <= 0.2508362656036639:
            return 1
        elif p1 <= 0.6540492277407066:
            return 2
        else:
            return 3
        
    #Criar conexão com o Athena
    my_boto3_session = boto3.Session(region_name='us-east-1')
    
    passenger_id = event['queryStringParameters']['passenger_id']
    
    query = "SELECT * FROM auladeploymodelos.titanic_propensity_survive where passengerid = %s;" % passenger_id
    dataprep_df = wr.athena.read_sql_query(query, database="auladeploymodelos", boto3_session=my_boto3_session)
    
    predict_df = h2o.mojo_predict_pandas(dataprep_df.set_index('passengerid', inplace=False), mojo_zip_path=BestModelId, genmodel_jar_path='h2o-genmodel.jar', verbose=False).loc[:,('predict','p1')]
            
    def predict_func(predict):
        if predict == 0:
            return 'Not survive'
        elif predict == 1:
            return 'Survive'
        else:
            return 'predict_ERROR'
    
    predict_df['predict'] = predict_df.apply(lambda x: predict_func(x['predict']),axis=1).astype(str)
    
    predict_df['rating'] = predict_df.apply(lambda x: ratings(x['p1']),axis=1).astype(str)

    body = {
        "message": "Prediction executed successfully!"        
    }

    body['probability'] = round(predict_df['p1'][0],4)
    body['rating'] = predict_df['rating'][0]
    body['predict'] = predict_df['predict'][0]
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }
    
    return response