def lambda_handler(event, context):
    import h2o
    import pandas as pd
    import boto3    
    import json
    
    #Best Model ID:
    BestModelId='StackedEnsemble_BestOfFamily_4_AutoML_1_20221011_230015.zip'
    
    #Keep the ratings ranges updated
    def ratings(p1):
        if p1 <= 0.2508362656036639:
            return 1
        elif p1 <= 0.6540492277407066:
            return 2
        else:
            return 3

    passenger_id = event['queryStringParameters']['passenger_id']
    embarked = event['queryStringParameters']['embarked']
    
    #Criar conexão com o DynamoDB
    my_boto3_session = boto3.Session(region_name='us-east-1')
    
    titanicTable = my_boto3_session.resource('dynamodb').Table('titanic-propensity-survive').get_item(Key={'passengerid': int(passenger_id)})['Item']
    
    #Fazer o tratamento do campo embarked para deixar com os valores conhecidos pelo modelo
    if embarked == "Cherbourg":
        embarked = "C"
    elif embarked == "Queenstown":
        embarked = "Q"
    elif embarked == "Southampton":
        embarked = "S"
        
    titanicTable['embarked'] = embarked
    
    del titanicTable['referencedate']
    del titanicTable['passengerid']
    del titanicTable['partition_0']
    
    predict_df = h2o.mojo_predict_pandas(pd.DataFrame(titanicTable, index=[0]).set_index('embarked', inplace=False), mojo_zip_path=BestModelId, genmodel_jar_path='h2o-genmodel.jar', verbose=False).loc[:,('predict','p1')]
            
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

# DEV
event={
    "queryStringParameters":{"passenger_id":"2", "embarked": "Cherbourg"}
}
context='context'
print(lambda_handler(event, context))