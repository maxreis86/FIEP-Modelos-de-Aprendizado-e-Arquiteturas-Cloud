FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY handler.py ./
COPY StackedEnsemble_BestOfFamily_4_AutoML_1_20221115_210852.zip ./
COPY h2o-genmodel.jar ./

CMD ["handler.lambda_handler"]