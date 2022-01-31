import boto3
import logging
from functools import wraps

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_cloudwatch(fn):
  @wraps(fn)
  def wrapper(event, context):
    logger.info(f'{context.function_name} - entry:{event}')
    res = fn(event, context)
    logger.info(f'{context.function_name} - result:{res}')
    return res

  return wrapper


def read_file(bucket, key):
  s3 = boto3.client('s3')

  file = s3.get_object(Bucket=bucket, Key=key)
  file_content = file['Body'].read().decode('utf-8')

  return file_content

def translate_text(text):
  translate = boto3.client('translate')

  res = translate.translate_text(
    Text=text,
    SourceLanguageCode='auto',
    TargetLanguageCode='en'
  )

  return {
    'original_text': text,
    'translated_text': res['TranslatedText'],
    'original_language': res['SourceLanguageCode'],
    'target_language': res['TargetLanguageCode']
  }


@log_cloudwatch
def lambda_handler(event, context):
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = event['Records'][0]['s3']['object']['key']

  # read file
  try:
    text = read_file(bucket, key)
  except Exception as e:
    logger.error(f'failed to read file: {e}')
    raise e

  # translate file
  try:
    translation = translate_text(text)
  except Exception as e:
    logger.error(f'failed to translate text: {e}')
    raise e

  return {
    'statusCode': 200,
    'body': translation
  }
