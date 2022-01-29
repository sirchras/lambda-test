import json
import logging
from functools import wraps

def log_cloudwatch(fn):
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)

  @wraps(fn)
  def wrapper(event, context):
    logger.info(f'{context.function_name} - entry:{event}')
    res = fn(event, context)
    logger.info(f'{context.function_name} - result:{res}')
    return res

  return wrapper

@log_cloudwatch
def lambda_handler(event, context):
  # TODO implement
  return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
  }
