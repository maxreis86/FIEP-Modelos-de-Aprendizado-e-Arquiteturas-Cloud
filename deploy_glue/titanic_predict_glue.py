import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.types import *
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pysparkling.ml import H2OMOJOSettings
from pysparkling.ml import H2OMOJOModel
import pandas as pd

# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])

#Job setup
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED")

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

datasource_titanic = glueContext.create_dynamic_frame.from_catalog(database = "auladeploymodelos", table_name = "titanic_propensity_survive", transformation_ctx = "datasource_titanic_propensity_survive", additional_options={"mergeSchema": "true"}).toDF()\
.fillna(value="Missing")

#Name
ModelName = 'titanic_propensity_survive'
# ATENÇÃO: nome do bucket criado no S3 (altere para o bucket com o seu nome)
bucketName = 'aula-deploy-modelos-william-moreira'

#ATENÇÃO
#Remover ./output_model/models/best/ da variável PathModelMojo e deixar somente o nome do arquivo .zip



############################################ COLAR O CÓDIGO DO DEPLOY SOMENTE ABAIXO DESSA LINHA ###########################

# Após testar esse código, colocar no bloco abaixo, na parte reservada para o seu scritp de deploy

#ModelPath
PathModelMojo='StackedEnsemble_BestOfFamily_4_AutoML_1_20221115_210852.zip'

## Selected Features: variaveis que entraram no modelo
CAT = [
'pclass'
,'embarked'
,'cabine_prefix'
,'ticket_str'
,'nametitle']

#float
NUM = [
'fare'
,'sibsp'
,'parch'
,'age_mean'
,'ticket_int']
selected_features = CAT + NUM

##functions
def ratings(p1):
    if p1 <= 0.2508362656036639:
        return 1
    elif p1 <= 0.6540492277407066:
        return 2
    else:
        return 3
ratings_func = F.udf(ratings, StringType())

def predict_survive(predict):
    if predict == 0:
        return 'Not survive'
    elif predict == 1:
        return 'Survive'
    else:
        return 'predict_ERROR'
predict_func = F.udf(predict_survive, StringType())

## Escorar a base, criar o score e o rating
settings = H2OMOJOSettings(convertUnknownCategoricalLevelsToNa = True, convertInvalidNumbersToNa = True)
model = H2OMOJOModel.createFromMojo(PathModelMojo, settings)
predict_titanic_1 = model.transform(datasource_titanic)

predict_titanic = predict_titanic_1.withColumn('predict_int', F.col('detailed_prediction.label').cast(IntegerType()))\
.withColumn('probability', F.col('detailed_prediction.probabilities.1'))\
.withColumn('rating', ratings_func((F.col('probability'))))\
.withColumn('predict', predict_func(F.col('predict_int')))\
.drop('detailed_prediction', 'prediction', 'predict_int', 'partition_0')

first_cols = ['pclass', 'embarked', 'cabine_prefix', 'ticket_str', 'nametitle']
other_cols = sorted([c for c in predict_titanic.columns if c not in first_cols])
rearanged_cols = first_cols + other_cols
predict_titanic = predict_titanic.select(rearanged_cols)

############################################# FIM DO BLOCO PARA COLOCAR SEU CÓDIGO #############################################



## Salvar no Lakehouse no format parquet
predict_titanic.write.mode("overwrite").format("parquet").partitionBy('embarked', 'pclass').save('s3://%s/databases/%s' % (bucketName, ModelName+'_spark'))

job.commit()

#fim