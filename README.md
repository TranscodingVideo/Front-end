# Front-end
## Setting up environment
* pip3 install virtualenv
* virutalenv -p python3 venv --always-copy
* source venv/bin/activate

## Dependencies to install in virtual environment
* pip install flask
* pip install flask-bootstrap
* pip install boto3 
* pip install awscli
* pip install arrow

## Configuring AWS
* aws configure

## If .env doesnt work
* export FLASK_APP=app.py
* export FLASK_ENV=development
* export S3_BUCKET=<bucket name>
* export S3_BUCKET2=<bucket 2 name>
* export S3_KEY=<access key>
* export S3_SECRET_ACCESS_KEY=<secret>

## To Run the server
* flask run
* flask run --host=0.0.0.0