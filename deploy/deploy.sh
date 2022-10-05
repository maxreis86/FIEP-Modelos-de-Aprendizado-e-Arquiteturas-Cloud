#serverless config credentials --provider aws --key AKIATSOWRPN4647AE5NC --secret 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
serverless create --template aws-python3 --name model-prop-apply-prospects
serverless plugin install -n serverless-python-requirements
python handler.py
#serverless invoke local --function predict-default --path event.json
serverless deploy