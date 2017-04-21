# Serverless Image Service
An AWS Lambda service that listens to S3 events, and if any image was added to a S3 bucket it will resize it to listed sizes in the configuration file.

### Notes : 
- New resized images are public by default.
- It only supports : jpg,gif,png,bmp

# How to deploy

### Clone it
```
$ git clone git@github.com:OsamaJBR/serverless-image-service.git
$ cd serverless-image-service
```
### Create VirtualEnv 
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```


### Initalize and Deploy Zappa project
```
$ zappa init
$ zappa deploy staging
```

# How to test
- Upload an image on S3
- Wait a second, you should find a new folder in the bucket that contains new sizes.

# To Do
- Add watermark
