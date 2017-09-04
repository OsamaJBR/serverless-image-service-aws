#!/usr/bin/python
from io import BytesIO
from PIL import Image
import urllib
import sys
import json
import boto3
import os

# config
config = json.loads(open('config.json').read())
resized_bucket_name=config.get('resized_bucket')[os.environ.get('env')]

# MIME
# image types
content_types = {
    'png' : 'image/png',
    'jpg' : 'image/jpeg',
    'jpeg': 'image/jpeg',
    'bmp' : 'image/bmp',
    'gif' : 'image/gif'
}

# Functions
def resize(size,image_content):
    width=int(size.split('x')[0])
    height=int(size.split('x')[1])
    img = Image.open(image_content)
    if width and height:
        img = img.resize((width, height), Image.ANTIALIAS)
    elif not height:
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
    elif not width:
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), Image.ANTIALIAS)
    tmp_img = BytesIO()
    img.save(tmp_img,'png')
    return tmp_img

def mark_media_as_ready(key):
    # Do whatever you want to do after resizing the image
    return True

def lambda_handler(event,context):
    print(event)
    if not os.environ.get('env') :
        print("env variable should be added")
        exit
    for record in event['Records']:
        event_bucket = record['s3']['bucket']['name']
        key = urllib.unquote_plus(record['s3']['object']['key'])
        fname, image_type = os.path.splitext(key)
        print("A new image was added to %s, path=%s" %(event_bucket,key))
        # get image from s3
        s3 = boto3.client('s3')
        # Save image into FileObject
        image_file = BytesIO()
        s3.download_fileobj(Bucket=event_bucket,Key=key,Fileobj=image_file)
        # do the resize 
        sizes = config.get('sizes') 
        for item in sizes:
            size=item['size']
            print("Resizing image=%s to %s" %(key,size))
            resized_image= resize(size=size,image_content=image_file)
            # Upload the new sizes to s3 again
            print("New resized image size = %s " %len(resized_image.getvalue()))
            resized_image.seek(0)
            resized_fname=key.replace(image_type,'.%s%s' %(size,image_type))
            s3.upload_fileobj(
                Fileobj=resized_image,
                Bucket=resized_bucket_name,
                Key=resized_fname,
                ExtraArgs={
                    'ACL':'public-read',
                    'ContentType' : content_types[image_type.lower().replace('.','')]
                }
            )
            print("Size=%r should be uploaded to %s:%s"%(size,resized_bucket_name,key))
            mark_media_as_ready(key)