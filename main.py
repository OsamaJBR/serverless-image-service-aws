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

bucket_name=config.get('bucket')
original_dir=config.get('original').get('directory')
sizes=config.get('resizes')  

# resize handler 
resize = resize_handler()

# image types
content_types = {
    'png' : 'image/png',
    'jpg' : 'image/jpeg',
    'jpeg' : 'image/jpeg',
    'bmp'   : 'image/bmp',
    'gif'   : 'image/gif'
}

def lambda_handler(event,context):
    for record in event['Records']:
        event_bucket = record['s3']['bucket']['name']
        key = urllib.unquote_plus(record['s3']['object']['key'])
        image_type = content_types[record['s3']['object']['key'].split('.')[-1].lower()]
        if '/' in key : 
            image_name = key.split('/')[-1]
        else:
            image_name = key

        # get image from s3
        s3 = boto.connect_s3()
        bucket = s3.get_bucket(event_bucket, validate=False)
        k = bucket.new_key(key)

        # Save image into FileObject
        image_file = StringIO.StringIO()
        k.get_file(image_file)

        # do the resize 
        sizes = config.get('sizes') 
        for item in sizes:
          size=item['size']
          s3_directory=item['directory']
          resized_image= resize.resize(size=size,image_content=image_file)
          # Upload the new sizes to s3 again
          s3 = boto.connect_s3()
          bucket = s3.get_bucket(bucket_name)
          new_k = bucket.new_key('{folder}/{fname}'.format(folder=s3_directory,fname=image_name))
          new_k.set_acl("public-read")
          new_k.set_metadata('Content-Type',image_type)
          new_k.set_contents_from_string(resized_image.getvalue())
          
        
        resized_image.close()
        image_file.close()

        