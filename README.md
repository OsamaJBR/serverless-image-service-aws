# serverless-image-service
Server-less  Image Service that listens to S3 events and fire a resize / watermakr process on the image.

# How to deploy
```
$ git clone git@github.com:OsamaJBR/serverless-image-service.git
$ cd serverless-image-service

# Create VirtualEnv 
$ virtualenv env
$ source env/bin/activate
$ pip install zappa
$ pip install -r requirements.txt

# Deploy Zappa Production
$ zappa deploy production
```

