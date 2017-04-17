from ConfigParser import SafeConfigParser
from resize import resize_handler
import cStringIO
import logging
import urllib
import sys
import json
from PIL import Image
import PIL
import boto

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)

# config
config = json.loads(open('config.json').read())

bucket_name=config.get('bucket')
original_dir=config.get('original').get('directory')
sizes=config.get('resizes')  

# resize handler 
resize = resize_handler()

def lambda_handler(event,context):
    for record in event['Records']:
        event_bucket = record['s3']['bucket']['name']
        if event_bucket == bucket_name : continue
        key = urllib.unquote_plus(record['s3']['object']['key'])
        if '/' in key : 
            image_name = key.split('/')[-1]
        else:
            image_name = key
        try:
            # get image from s3
            s3 = boto.connect_s3()
            bucket = s3.get_bucket(event_bucket, validate=False)
            k = bucket.new_key(key)
            image_content = k.get_contents_as_string()

            # do the resize 
            sizes = config.get('resizes') 
            for item in sizes:
                size=item['size']
                s3_directory=item['directory']
                resized_image= resize.resize(size=size,image_content=image_content)
                # Upload the new sizes to s3 again
                s3 = boto.connect_s3()
                bucket = s3.get_bucket(bucket_name)
                k = bucket.new_key('%s/%s'%(s3_directory,image_name))
                k.set_contents_from_string(resized_image.getvalue())
        
        except Exception as e:
            logger.error(e)
            logger.error('Error getting object %s from bucket %s.', key, bucket)
        