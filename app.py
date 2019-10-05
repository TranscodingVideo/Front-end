from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET,S3_BUCKET2,S3_KEY,S3_SECRET_ACCESS_KEY
from filters import timeformat, file_type

#setup boto 3 resources,
s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)

app = Flask(__name__)
Bootstrap(app)

app.jinja_env.filters['timeformat'] = timeformat
app.jinja_env.filters['file_type'] = file_type

#@app.route('/')
#def index():
#    return render_template("index.html")

@app.route('/')
def files():
    s3_resource = boto3.resource('s3')
    # makes a bucket variable that grabs the bucket 
    # information from the specified bucket
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    # grabs all the summaries (contents) of the s3 bucket
    summaries = my_bucket.objects.all()
    return render_template('files.html', my_bucket=my_bucket, files=summaries)

@app.route('/download')
def download():
    s3_resource = boto3.resource('s3')
    # makes a bucket variable that grabs the bucket 
    # information from the specified bucket
    my_bucket = s3_resource.Bucket(S3_BUCKET2)

    # grabs all the summaries (contents) of the s3 bucket
    summaries = my_bucket.objects.all()
    return render_template('download.html', my_bucket=my_bucket, files=summaries)

if __name__ == '__main__':
    app.run()
