import random
import json

def lambda_handler(event, context):    
    user_id = event['queryStringParameters']['user_id']
    
    post_id=[
     'b0c9a153-9030-4a9d-80cc-f9677174ccff'
    ,'1dc3ba7f-6b9b-4ef2-92af-44a9afa7b4a0'
    ,'915da040-7918-4f02-870e-d968ca7acf4d'
    ,'d49411e4-b02f-491f-a974-9ebd6d9faae1'
    ,'c96e1d56-b160-4551-8414-77d10fcd077e'
    ,'9672e35d-03b9-4fdf-9813-f235e28e593b'
    ,'fbc48d2b-2218-4748-b183-160726d9983f'
    ,'d37176c6-a94c-496b-9c42-db3c466722f6'
    ,'9d1ce001-9429-4501-8584-581b3210211e'
    ,'a7815b8d-29a5-479c-bb0e-7179e419dc92'
    ]
    
    body = {
        "message": "Prediction executed successfully!"        
    }

    body['user_id'] = user_id
    body['post_id'] = random.choice(post_id)    
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*"
        }
    }
    
    return response

# # DEV
# event={
#     "queryStringParameters":{"user_id":"1234"}
# }
# context='context'
# print(lambda_handler(event, context))