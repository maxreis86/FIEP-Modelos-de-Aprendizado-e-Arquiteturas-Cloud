FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY handler.py ./
COPY GBM_grid_1_AutoML_1_20220602_224459_model_101.zip ./
COPY h2o-genmodel.jar ./

CMD ["handler.lambda_handler"]