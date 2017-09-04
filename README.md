# Serverless Image Service
Simple server-less implementation for Image-Service that resizes images using AWS Lambda Function and S3 Storage.

### How It Works
Lambda function could be fired by S3::ObjectCreated events, this starts the lambda function that gets the image from s3 and resizes it to defined sizes in *config.json*.

### Notes : 
- New resized images are public by default.
- It only supports : jpg,gif,png,bmp
- If you want to use the same bucket for both input/output,you should filter s3 events (in zappa_settings.json).
```
"key_filters": [
                {
                    "type": "prefix",
                    "value": "originals"
                }]
```
# How To Deploy
```
# Create virtualenv
$ virtualenv env
$ source env/bin/activate

# Install Requirements 
$ pip install -r requirements.txt

# Edit the config.json, set output sizes and s3 bucket.
# Then, change ORIGINAL_BUCKET in zappa_settings.json
# Deploy it now.
$ zappa deploy production
```

# How To Test
- Upload an image on S3
- Wait a second, you should find a new folder in the resized bucket with new resized images.