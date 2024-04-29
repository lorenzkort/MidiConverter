import os
import boto3
from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH

def clean_up_tmp(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    return

def handler(event, context):
    """
    Top-level function which handles events that come in from the front-end
    """
    try:

        # Initialise Amazon Webservices S3 Client
        s3_client = boto3.client('s3', region_name='eu-north-1')
        s3_client.download_file('mikro-bucket2', event['file_id'] ,'/tmp/' + event['file_id'])
        
        # load file
        file_path = '/tmp/'+event['file_id']
        
        # After downloading the file, verify it exists
        if not os.path.exists(file_path):
            raise Exception(f"Failed to download file: {file_path}")
        
        # Use the predict function to get model output, MIDI data, and note events
        _, midi_data, note_events = predict(
            file_path
        )
        
        # Remove the file from the tmp directory
        os.remove('/tmp/'+event['file_id'])
        
        # Save the MIDI file
        midi_file_name = f"/tmp/{file_path.split('/')[-1].split('.')[0]}.midi"
        # midi_data.write(midi_file_name)

        # Return the output data
        return {
            "statusCode": "Success",
            "body": {
                "NoteEvents": str(note_events)
                }
        }
    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
        
    except boto3.exceptions.Boto3Error as boto3_error:
        print(f"AWS error: {boto3_error}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        
    except Exception as e:
        clean_up_tmp(file_path)
        return {"statusCode": "Error", "body": str(e)}
    finally:
        clean_up_tmp(file_path)