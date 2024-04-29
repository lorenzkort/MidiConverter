import os
import boto3
import tflite_runtime.interpreter as tflite
from basic_pitch.inference import predict as basic_pitch_predict
from basic_pitch import ICASSP_2022_MODEL_PATH

try:
    # Load the TFLite model
    tflite.Interpreter(model_path=ICASSP_2022_MODEL_PATH)
    interpreter = tflite.Interpreter(model_path=ICASSP_2022_MODEL_PATH)
    interpreter.allocate_tensors()
except Exception as e:
    print( {"statusCode": "Error", "body": str(e)} )


def clean_up_tmp(event):
    file_name = '/tmp/'+event['file_id']

    # Clean up other filenames if they exist
    if os.path.exists(file_name):
        os.remove(file_name)
    return

def handler(event, context):
    """
    Top-level function which handles events that come in from the front-end
    """
    try:

        # Initialise Amazon Webservices S3 Client
        s3_client = boto3.client('s3', region_name='eu-north-1')
        s3_client.download_file('mikro-bucket2',event['file_id'] ,'/tmp/'+event['file_id'])
        
        # load file
        file_path = '/tmp/'+event['file_id']
        
        # Use the predict function to get model output, MIDI data, and note events
        _, midi_data, note_events = basic_pitch_predict(
            file_path,
            interpreter,
        )
        
        # Save the MIDI file
        midi_file_name = f"{file_path.split('/')[-1].split('.')[0]}.midi"
        midi_data.write(midi_file_name)

        # Return the output data
        return {"statusCode": "Success", "body": {"NoteEvents": "test"}}
    
    except Exception as e:
        if os.path.exists('/tmp/'+event['file_id']):
            os.remove('/tmp/'+event['file_id'])
            print(e)
        return {"statusCode": "Error", "body": str(e)}
    finally:
        clean_up_tmp(event)