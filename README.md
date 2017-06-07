# Serverless Image Service
An AWS Lambda service that listens to S3 events, and if any image was added to a S3 bucket it will resize it to listed sizes in the configuration file.

### Notes : 
- New resized images are public by default.
- It only supports : jpg,gif,png,bmp

# How to deploy

### Clone it
```
$ git clone git@github.com:OsamaJBR/aws-lamda-image-service.git
$ cd aws-lamda-image-service
```
### Create VirtualEnv 
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```


### Initalize and Deploy Zappa project
```
#Edit the config.json
{
  "resized_bucket": "RESIZED_BUCKET",
  "originals_bucket": "ORIGINAL_BUCKET",
  "sizes": [
    {
      "size": "300x0",
      "directory": "resized/300x0"    
    },
    {
      "size": "600x600",
      "directory": "resized/600x600"
    }
  ]
}
# Then, zappa_settings.json
{
    "staging": {
        "events": [{
            "function": "main.lambda_handler",
            "event_source": {
                  "arn":  "arn:aws:s3:::ORIGINAL_BUCKET",
                  "events": [
                    "s3:ObjectCreated:*" 
                  ]
               }
            }],
    "keep_warm": false,
    "apigateway_enabled" : false,
    "memory_size" : 128,
    "debug": false
    }
}

$ zappa deploy staging
```

# How to test
- Upload an image on S3
- Wait a second, you should find a new folder in the resized bucket with new resized images.

# To Do
- Add watermark
