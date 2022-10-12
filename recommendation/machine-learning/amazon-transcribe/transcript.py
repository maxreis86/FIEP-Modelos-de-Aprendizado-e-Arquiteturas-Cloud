#Import libraries
import boto3
import json
from time import gmtime, strftime, sleep
import uuid
import datetime as dt

#Create boto3 sesesion
boto3_session = boto3.Session(region_name='us-east-1')

#Amazon Transcribe
transcribe = boto3_session.client('transcribe')

#Transcribe function
def transcribe_post(post_id):
    job_id = uuid.uuid4()
    
    #Start transcription job
    response = transcribe.start_transcription_job(
        TranscriptionJobName=f'post-ingestion-transcription-{post_id}-{job_id}',
        LanguageCode='en-US',        
        MediaFormat='mp4',
        Media={
            'MediaFileUri': f's3://now-app-media-service/{post_id}.mp4'
        },
        OutputBucketName='now-app-media-service',
        OutputKey= f'transcripts/python/{post_id}.json',
        Settings={        
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 10,
            'ChannelIdentification': False,
            'ShowAlternatives': False            
        },
        Subtitles={
            'Formats': [
                'srt'
            ],
            'OutputStartIndex': 1
        }    
    )
    
    #wait until the job is finished
    while response['TranscriptionJob']['TranscriptionJobStatus'] not in ('COMPLETED', 'FAILED'):
        response = transcribe.get_transcription_job(
            TranscriptionJobName=f'post-ingestion-transcription-{post_id}-{job_id}'
        )
        # print(
        #     response['TranscriptionJob']['TranscriptionJobStatus'] + " - " + strftime("%d-%H-%M-%S", gmtime())
        # )
        sleep(1)
        
    #print the transcription
    s3 = boto3_session.resource('s3')
    content_object = s3.Object('now-app-media-service', f'transcripts/python/{post_id}.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    print(post_id + ': ' + json_content['results']['transcripts'][0]['transcript'])
    print('-----------------------------------------------------------------------')
    
    #Read the subtitles in srt file
    srt_content_object = s3.Object('now-app-media-service', f'transcripts/python/{post_id}.srt')
    srt_file_content = srt_content_object.get()['Body'].read().decode('utf-8')
    
    #Save to DynamoDB
    put_item={}
    put_item['id']=post_id
    put_item['postTranscript']=json_content['results']['transcripts'][0]['transcript']
    put_item['postSubtitles']=srt_file_content
    put_item['postSpeakersNumber']=json_content['results']['speaker_labels']['speakers']
    put_item['postedTimestamp'] = str(dt.datetime.now().isoformat())
    
    prod_post_table = boto3_session.resource('dynamodb').Table('prod-post')
    prod_post_table.put_item(Item=put_item)
    
#Infor the post ID and execute transcription
transcribe_post('N26')