from ConfigParser import SafeConfigParser
from resize import resize_handler
import StringIO
import logging
import urllib
import sys
import json
import boto

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)

# config
config = json.loads(open('config.json').read())
originals_bucket_name=config.get('originals_bucket')
resized_bucket_name=config.get('resized_bucket')

# resize handler 
resize = resize_handler()

# image types
content_types = {
    'png' : 'image/png',
    'jpg' : 'image/jpeg',
    'jpeg': 'image/jpeg',
    'bmp' : 'image/bmp',
    'gif' : 'image/gif'
}

def lambda_handler(event,context):
    for record in event['Records']:
        event_bucket = record['s3']['bucket']['name']
        key = urllib.unquote_plus(record['s3']['object']['key'])
        image_type = content_types[record['s3']['object']['key'].split('.')[-1].lower()]
        logger.info("Key = %r",key)
        image_name = key
        # get image from s3
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(event_bucket, validate=False)
        tmp_key = bucket.new_key(key)
        # Save image into FileObject
        image_file = StringIO.StringIO()
        tmp_key.get_file(image_file)

        # do the resize 
        sizes = config.get('sizes') 
        for item in sizes:
          size=item['size']
          logger.info("Resizing to %r", size)
          s3_directory=item['directory']
          resized_image= resize.resize(size=size,image_content=image_file)
          # Upload the new sizes to s3 again
          bucket = s3.get_bucket(resized_bucket_name)
          logger.info("Connected to resized bucket %r", resized_bucket_name)
          new_k = bucket.new_key('{folder}/{fname}'.format(folder=s3_directory,fname=image_name))
          logger.info("New Key should be in %r",'{folder}/{fname}'.format(folder=s3_directory,fname=image_name))
          new_k.set_contents_from_string(resized_image.getvalue())
          new_k.make_public()
          new_k.set_remote_metadata({'Content-Type': image_type},{},True)
          logger.info("Size=%r should be uploaded",size)
          resized_image.close()
        
        # clost the fileObject
        image_file.close()

        