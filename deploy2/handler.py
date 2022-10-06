def lambda_handler(event, context):
    import h2o
    import pandas as pd
    import numpy as np
    import json
    import boto3
    from boto3.dynamodb.conditions import Key
    import datetime as dt
    import queue
    from threading import Thread
    from decimal import Decimal
    import re
    
    #Best Model ID:
    BestModelId='GBM_grid_1_AutoML_1_20220602_224459_model_101.zip'
    
    #Keep the ratings ranges updated
    def ratings(p1):
        if p1 <= 0.0382443443235362:
            return 1
        if p1 <= 0.0530430015585711:
            return 2
        if p1 <= 0.0673746428820707:
            return 3
        if p1 <= 0.0784943959938068:
            return 4
        if p1 <= 0.0995685833288207:
            return 5
        if p1 <= 0.1190589979996429:
            return 6
        if p1 <= 0.1493789514138822:
            return 7
        elif p1 <= 0.1744927522205538:
            return 8
        elif p1 <= 0.2207991656421561:
            return 9
        else:
            return 10
            
    def company_classification_const(s):
        if s == 'Empresa pequena':
            out='Empresa pequena'
        elif s == 'Empresas pequenas':
            out='Empresa pequena'
        elif s == 'Empresa Tradicional A':
            out='Empresa Tradicional A'
        elif s == 'Empresa Tradicional B':
            out='Empresa Tradicional B'
        elif s == 'Empresa Tradicional C':
            out='Empresa Tradicional C'
        elif s == 'High Tech A':
            out='High Tech A'
        elif s == 'High Tech B':
            out='High Tech B'
        elif s == 'High Tech C':
            out='High Tech C'
        elif s == 'High Tech D':
            out='High Tech D'
        elif s == 'Software House A':
            out='Software House A'
        elif s == 'Software House B':
            out='Software House B'
        elif s == 'Software House C':
            out='Software House C'
        elif s == 'not_mapped':
            out='Missing'
        elif s in ('', 'null', None, 'None'):
            out='Missing'
        else:
            out='UNKNOWN'
        return out
            
    linkedinUsername = event['queryStringParameters']['linkedinUsername']
    jobId = event['queryStringParameters']['jobId']
    
    #Eh necessario criar duas boto3 para trabalhar com multiple threads. Uma para cada thread
    
    #boto3_Session para a tabela jobs
    boto_jobs = boto3.Session(region_name='us-east-1')
    
    #boto3_Session para a tabela prospects
    boto_prospects = boto3.Session(region_name='us-east-1')
    
#     #boto3_Session para a tabela jobs
#     boto_jobs = boto3.Session(region_name='us-east-1',
#         aws_access_key_id='AKIATSOWRPN4647AE5NC',
#         aws_secret_access_key='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')

#     #boto3_Session para a tabela prospects
#     boto_prospects = boto3.Session(region_name='us-east-1',
#         aws_access_key_id='AKIATSOWRPN4647AE5NC',
#         aws_secret_access_key='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')
    
    #Criar funcoes de consulta ao DynamoDB para serem executadas em paralelo diminuindo o tempo
    def dynamodb_jobs_clients_companies(jobId, boto3):        
        jobsTable = boto3.resource('dynamodb').Table('prod-jobsTable').query(
            IndexName='GSI1',
            KeyConditionExpression=Key('backofficeId').eq(int(jobId))
        )['Items']
    
        clientsTable = boto3.resource('dynamodb').Table('prod-clientsTable').query(
            IndexName='idBackofficeIndex',
            KeyConditionExpression = (Key('source').eq('backoffice') & Key('idBackoffice').eq(int(jobsTable[0]['companyId'])))
        )['Items']
        
        if clientsTable[0]['linkedinURL'][-1] == '/':
            linkedin_company_user_name = clientsTable[0]['linkedinURL'].split('/')[-2]
        else:
            linkedin_company_user_name = clientsTable[0]['linkedinURL'].split('/')[-1]
    
        linkedinCompanies = boto3.resource('dynamodb').Table('prod-linkedinCompanies').query(
            IndexName='LinkedinUsernameIndex',
            KeyConditionExpression=Key('linkedinUsername').eq(linkedin_company_user_name)
        )['Items']
        
        return_object = {} 
        return_object['jobsTable'] = jobsTable
        return_object['linkedinCompanies'] = linkedinCompanies
        return return_object
        
    def dynamodb_prospects_companies(linkedinUsername, boto3):        
        prospectsTable = boto3.resource('dynamodb').Table('prod-prospectsTable').get_item(Key={'linkedinUsername': linkedinUsername})['Item']
    
        dict_prospects={}
        total_experience_months=[]
        total_experience_months_clean=[]
        prospect_companies=[]        
        all_company_classifications=[]
    def dynamodb_prospects_companies(linkedinUsername, boto3):        
        prospectsTable = boto3.resource('dynamodb').Table('prod-prospectsTable').get_item(Key={'linkedinUsername': linkedinUsername})['Item']
    
        dict_prospects={}
        total_experience_months=[]
        total_experience_months_clean=[]
        prospect_companies=[]        
        all_company_classifications=[]
        try:
            for i in range(len(prospectsTable['experiences'])):
                prospect_companies.append(prospectsTable['experiences'][i]['linkedinCompanyName'])
    
                try:
                    linkedinCompanies = boto3.resource('dynamodb').Table('prod-linkedinCompanies').query(
                        IndexName='LinkedinUsernameIndex',
                        KeyConditionExpression=Key('linkedinUsername').eq(prospectsTable['experiences'][i]['linkedinCompanyUsername'])
                    )['Items']
                    all_company_classifications.append(company_classification_const(linkedinCompanies[0]['category'].replace(' - ', ' ')))
                except Exception as e:                    
                    print("e.1: "+ str(e))
                    try:
                        linkedinCompanies = boto3.resource('dynamodb').Table('prod-linkedinCompanies').query(
                            IndexName='LinkedinIdIndex',
                            KeyConditionExpression=Key('linkedinId').eq(int(prospectsTable['experiences'][i]['linkedinCompanyId']))
                        )['Items']
                        all_company_classifications.append(company_classification_const(linkedinCompanies[0]['category'].replace(' - ', ' ')))
                    except Exception as e:
                        print("e.2: "+ str(e))
                        all_company_classifications.append('Missing')
    
                if i == 0:
                    if prospectsTable['experiences'][i]['to'] == None:
                        total_experience_months.append((int((dt.datetime.now() - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                    else:
                        total_experience_months.append((int((dt.datetime.strptime(prospectsTable['experiences'][i]['to'][:10], "%Y-%m-%d") - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                    #precisa colocar o copy porque a variavel total_experience sera alterada, mas a last_experience nao pode mais ser alterada
                    last_experience_duration_months = total_experience_months.copy()
                    try:
                        last_experience_descriptions = prospectsTable['experiences'][i]['description']
                    except Exception as e:
                        print("e.3: "+ str(e))
                        last_experience_descriptions = ''
                else:
                    try:
                        if prospectsTable['experiences'][i]['to'] == None:
                            total_experience_months.append((int((dt.datetime.now() - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                            total_experience_months_clean.append((int((dt.datetime.now() - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                        else:
                            total_experience_months.append((int((dt.datetime.strptime(prospectsTable['experiences'][i]['to'][:10], "%Y-%m-%d") - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                            total_experience_months_clean.append((int((dt.datetime.strptime(prospectsTable['experiences'][i]['to'][:10], "%Y-%m-%d") - dt.datetime.strptime(prospectsTable['experiences'][i]['from'][:10], "%Y-%m-%d")).days/30)))
                    except Exception as e:
                        print("e.3b: "+ str(e))
        except Exception as e:
            print("e.4: "+ str(e))
            last_experience_duration_months=[0]
            total_experience_months_clean=[0,0.1]
            total_experience_months=[0]
            last_experience_descriptions = ''
            all_company_classifications = ['Missing']
    
        dict_prospects['prospect_companies_qty'] = len(set(prospect_companies))
        dict_prospects['total_experience_months'] = sum(total_experience_months)
        dict_prospects['experience_duration_months_min'] = min(total_experience_months)
        dict_prospects['experience_duration_months_clean_avg'] = np.nan_to_num(np.mean((total_experience_months_clean)))
        dict_prospects['experience_duration_months_clean_stddev'] =  np.nan_to_num(np.std(total_experience_months_clean, ddof = 1))
        dict_prospects['last_experience_duration_months_to_avg'] = float(last_experience_duration_months[0]) - float(dict_prospects['experience_duration_months_clean_avg'])
        dict_prospects['last_experience_descriptions_word_count'] = float(len(last_experience_descriptions.split()))
        dict_prospects['last_company_classification'] = all_company_classifications[0]
#         dict_prospects['all_company_classifications_word_count'] = float(len('; '.join(map(str, all_company_classifications)).replace("||", ",").split()))
        dict_prospects['all_company_classifications_count'] = (sum(map((lambda x: (0 if x.strip() == 'Missing' else 1)), all_company_classifications)))
        
        return_object = {} 
        return_object['prospectsTable'] = prospectsTable
        return_object['dict_prospects'] = dict_prospects
        return return_object

    #Executar as duas funcoes de forma assincrona
    try:
        #criar q1 e q2 para receber o return de cada funcao
        q1 = queue.Queue()
        q2 = queue.Queue()
        #criar as duas tarefas
        t1 = Thread(target = lambda q, arg1, arg2 : q.put(dynamodb_jobs_clients_companies(arg1, arg2)), args = (q1, jobId, boto_jobs))
        t2 = Thread(target = lambda q, arg1, arg2 : q.put(dynamodb_prospects_companies(arg1, arg2)), args = (q2, linkedinUsername, boto_prospects))
        #iniciar as duas tarefas simutaneamente.
        t1.start()
        t2.start()
        #unir as duas tarefas para garantir que a proxima tarefa seja iniciada somente quando as duas terminarem
        t1.join()
        t2.join()
        
        #recebar o return da funcao
        while not q1.empty():
            return_object_jobs_clients_companies = q1.get()
        while not q2.empty():
            return_object_prospects_companies = q2.get()
    except Exception as e:
        print("e.5: "+ str(e))
        #criar q1 e q2 para receber o return de cada funcao
        q1 = queue.Queue()
        q2 = queue.Queue()
        #criar as duas tarefas
        t1 = Thread(target = lambda q, arg1, arg2 : q.put(dynamodb_jobs_clients_companies(arg1, arg2)), args = (q1, jobId, boto3))
        t2 = Thread(target = lambda q, arg1, arg2 : q.put(dynamodb_prospects_companies(arg1, arg2)), args = (q2, linkedinUsername, boto3))
        #iniciar as duas tarefas simutaneamente.
        t1.start()
        t2.start()
        #unir as duas tarefas para garantir que a proxima tarefa seja iniciada somente quando as duas terminarem
        t1.join()
        t2.join()
        
        #recebar o return da funcao
        while not q1.empty():
            return_object_jobs_clients_companies = q1.get()
        while not q2.empty():
            return_object_prospects_companies = q2.get()
            
    jobsTable = return_object_jobs_clients_companies['jobsTable']
    linkedinCompanies = return_object_jobs_clients_companies['linkedinCompanies']
    prospectsTable = return_object_prospects_companies['prospectsTable']
    dict_prospects = return_object_prospects_companies['dict_prospects']

    #Start empty dictionary
    dict_jobs={}

    ## job_seniority = 'profile.seniority'
    def job_seniority_const(s):
        if s in ("Júnior", "junior", "Junior"):
            out="Junior"
        elif s in ("Pleno", "pleno"):
            out="Mid-level"
        elif s in ("Senior", "Sênior", "senior"):
            out="Senior"
        elif s in ("Especialista", "especialista"):
            out="Specialist"
        elif s == "Tech Lead":
            out="Tech Lead"
        elif s == "Tech Manager":
            out="Tech Manager"
        elif s in ('', 'null', None, 'None'):
            out="Missing"
        else:
            out="UNKNOWN"
        return out
    
    dict_jobs['job_seniority'] = job_seniority_const(jobsTable[0]['profile']['seniority'])

    ## job_area = 'area'
    try:
        dict_jobs['job_area'] = jobsTable[0]['area']
    except Exception as e:
        print("e.6: "+ str(e))
        dict_jobs['job_area'] = 'Missing'

    ## max_salary_offered = 'maxsalary'
    try:
        dict_jobs['max_salary_offered'] = float(jobsTable[0]['maxSalary'])
    except Exception as e:
        print("e.7: "+ str(e))
        dict_jobs['max_salary_offered'] = 0
        
    ## import_policy_word_count = 'importPolicy'
    try:
        dict_jobs['import_policy_word_count'] = float(len(jobsTable[0]['importPolicy'].split()))
    except Exception as e:
        print("e.8: "+ str(e))
        dict_jobs['import_policy_word_count'] = 0

    ## job_technical_requirements_word_count = 'alignments.intendedTechnicalInfo'
    try:
        dict_jobs['job_technical_requirements_word_count'] = float(len(jobsTable[0]['alignments']['intendedTechnicalInfo'].split()))
    except Exception as e:
        print("e.9: "+ str(e))
        dict_jobs['job_technical_requirements_word_count'] = 0

    ## job_validation_questions_word_count = 'validationQuestions'
    try:
        dict_jobs['job_validation_questions_word_count'] = float(len(jobsTable[0]['validationQuestions'].split()))
    except Exception as e:
        print("e.10: "+ str(e))
        dict_jobs['job_validation_questions_word_count'] = 0
        
    ## company_classification
    try:
        dict_jobs['job_company_classification'] = company_classification_const(linkedinCompanies[0]['category'].replace(' - ', ' '))
    except Exception as e:
        print("e.11: "+ str(e))
        dict_jobs['job_company_classification'] = 'Missing'

    
    ## prospectsTable

    ## declared_seniority = 'declaredseniority'
    try:
        dict_prospects['declared_seniority'] = job_seniority_const(prospectsTable['declaredSeniority'])
    except Exception as e:
        print("e.12: "+ str(e))
        dict_prospects['declared_seniority'] = 'Missing'

    # 'declared_seniority_migration'
    dict_prospects['declared_seniority_migration'] = (dict_prospects['declared_seniority']+'-to-'+dict_jobs['job_seniority']).strip()

    #Criacao das variaveis de pais com base na variavel propesct_location do linkedin. Para comparar abordagens de talentos que moram fora do Brasil
    def prospect_country(country):
        if pd.isna(country):
            return "Missing"
        elif country == 'São Paulo':
            return 'Brazil'
        elif country == 'Rio de Janeiro':
            return 'Brazil'
        elif country == 'Campinas':
            return 'Brazil'
        elif country == 'Belo Horizonte':
            return 'Brazil'
        elif country == 'Porto Alegre':
            return 'Brazil'
        elif country == 'Curitiba':
            return 'Brazil'
        elif country == 'Brasília':
            return 'Brazil'
        elif country == 'Florianópolis':
            return 'Brazil'
        elif country == 'Salvador':
            return 'Brazil'
        elif country == 'Fortaleza':
            return 'Brazil'
        elif country == 'Recife':
            return 'Brazil'
        elif country == 'Manaus':
            return 'Brazil'
        elif country == 'Ribeirão Preto':
            return 'Brazil'
        elif country == 'Goiânia':
            return 'Brazil'
        elif country == 'João Pessoa':
            return 'Brazil'
        elif country == 'Londrina':
            return 'Brazil'
        elif country == 'Vitória':
            return 'Brazil'
        elif country == 'Cuiabá':
            return 'Brazil'
        elif country == 'Greater São Paulo Area':
            return 'Brazil'
        elif country == 'Natal':
            return 'Brazil'
        elif country == 'São luis':
            return 'Brazil'
        elif country == 'Brazil':
            return 'Brazil'
        elif country == 'Brasil':
            return 'Brazil'
        else:
            return 'Others'
        
    def prospect_region_international(region, country):
        if country not in ('Brazil', 'Missing'):
            return "International"
        else:
            return region
    try:
        dict_prospects['prospect_location_state'] = prospect_region_international(prospectsTable['location'].split(',')[-2].replace(" e Região", "").strip(), prospect_country(prospectsTable['location'].split(',')[-1].replace(" e Região", "").strip()))
    except Exception as e:
        print("e.13: "+ str(e))
        dict_prospects['prospect_location_state'] = 'Missing'
        
    ## prospect_area_migration
    try:    
        dict_prospects['prospect_area_migration'] = (prospectsTable['area'].split()[0]+'-to-'+dict_jobs['job_area']).strip()
    except Exception as e:
        print("e.14: "+ str(e))
        dict_prospects['prospect_area_migration'] = ('Missing'+'-to-'+dict_jobs['job_area']).strip()

    ## prospect_smart_skills_qty
    try:
        dict_prospects['prospect_smart_skills_qty'] = float(len(prospectsTable['smartTags']))
    except Exception as e:
        print("e.15: "+ str(e))
        dict_prospects['prospect_smart_skills_qty'] = 0.0

    ## prospect_experiences_qty
    try:
        dict_prospects['prospect_experiences_qty'] = float(len(prospectsTable['experiences']))
    except Exception as e:
        print("e.16: "+ str(e))
        dict_prospects['prospect_experiences_qty'] = 0.0
    
    # 'prospect_linkedin_about_word_count'
    try:
        dict_prospects['prospect_linkedin_about_word_count'] = float(len(prospectsTable['linkedinAboutText'].split()))
    except Exception as e:
        print("e.17: "+ str(e))
        dict_prospects['prospect_linkedin_about_word_count'] = 0
        
    # company_classification_migration
    dict_prospects['company_classification_migration']=(dict_prospects['last_company_classification']+'-to-'+dict_jobs['job_company_classification']).strip()
    
    del dict_jobs['job_seniority']
    del dict_jobs['job_company_classification']
    
    df = pd.concat([pd.DataFrame(dict_jobs, index=[0]), pd.DataFrame(dict_prospects, index=[0])], axis=1)
    
    predict=h2o.mojo_predict_pandas(df.set_index('last_company_classification', inplace=False), mojo_zip_path=BestModelId, genmodel_jar_path='h2o-genmodel.jar', verbose=False).loc[:,('predict','p1')]
            
    def suggestion(predict):
        if predict == 0:
            return 'Repensar'
        elif predict == 1:
            return 'Abordar'
        else:
            return 'SUGGESTION_ERROR'
    
    predict['suggestion'] = predict.apply(lambda x: suggestion(x['predict']),axis=1).astype(str)
    
    predict['rating'] = predict.apply(lambda x: ratings(x['p1']),axis=1).astype(str)

    body = {
        "message": "Prediction executed successfully!"        
    }

    body['probability'] = round(predict['p1'][0],4)
    body['rating'] = predict['rating'][0]
    body['suggestion'] = predict['suggestion'][0]
    
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
#     "queryStringParameters":{"jobId":"2329",
#                              "linkedinUsername":"patriciakano"}
# }
# context='context'
# print(lambda_handler(event, context))