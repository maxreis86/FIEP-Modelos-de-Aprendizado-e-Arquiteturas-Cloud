//npm install @aws-sdk/client-transcribe
//npm install uuid

import { TranscribeClient, StartTranscriptionJobCommand } from "@aws-sdk/client-transcribe";
import { v4 as uuidv4 } from 'uuid';

var config = {
    region: 'us-east-1'
};

var input = {
    TranscriptionJobName: 'post-ingestion-transcription-node-N31-' + uuidv4(),
    LanguageCode: 'en-US',    
    MediaFormat: 'mp4',
    Media: {
        'MediaFileUri': 's3://now-app-media-service/N31.mp4'
    },
    OutputBucketName: 'now-app-media-service',
    OutputKey:  'transcripts/node/N31.json',
    Settings: {        
        'ShowSpeakerLabels': true,
        'MaxSpeakerLabels': 10,
        'ChannelIdentification': false,
        'ShowAlternatives': false        
    },
    Subtitles: {
        'Formats': [
            'srt'
        ],
        'OutputStartIndex': 1
    }
};

const client = new TranscribeClient(config);
const command = new StartTranscriptionJobCommand(input);

const response = await client.send(command);