from flask import Flask, render_template, request, url_for, redirect, flash, Response, jsonify
from flask_bootstrap import Bootstrap
import boto3
from config import S3_BUCKET,S3_BUCKET2,S3_KEY,S3_SECRET_ACCESS_KEY, AWS_API_KEY, AWS_API_GATEWAY
from filters import timeformat, file_type
import requests

#setup boto 3 resources,
s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)

app = Flask(__name__)
app.secret_key = 'secret'
Bootstrap(app)

app.jinja_env.filters['timeformat'] = timeformat
app.jinja_env.filters['file_type'] = file_type

@app.route('/')
def uploadPage():
    s3_resource = boto3.resource('s3')
    # makes a bucket variable that grabs the bucket 
    # information from the specified bucket
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    # grabs all the summaries (contents) of the s3 bucket
    summaries = my_bucket.objects.all()
    return render_template('upload.html', my_bucket=my_bucket, files=summaries)

@app.route('/download')
def downloadPage():
    s3_resource = boto3.resource('s3')
    # makes a bucket variable that grabs the bucket 
    # information from the specified bucket
    my_bucket = s3_resource.Bucket(S3_BUCKET2)

    # grabs all the summaries (contents) of the s3 bucket
    summaries = my_bucket.objects.all()
    return render_template('download.html', my_bucket=my_bucket, files=summaries)

@app.route('/upload', methods=['POST'])
def upload():
    #Set variable from form
    file = request.files['file']
    email = request.form['email']
    #setting up s3 variables
    s3_resource=boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    #Sets object key to filename and uploads the objects
    my_bucket.Object(file.filename).put(Body=file,ContentDisposition='attachment')
    PARAMS = {
        'email': email,
        'filename': file.filename
    }
    headers = {
        'x-api-key': AWS_API_KEY
    }
    r = requests.post(url=AWS_API_GATEWAY, params=PARAMS, headers=headers)
    data = r.json()
    flash(data)
    return redirect(url_for('uploadPage'))

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    key = request.form['key']
    #setting up s3 variables
    s3_resource=boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    #Deletes the object from the bucket using the key
    my_bucket.Object(key).delete()

    flash('File Deleted')
    return redirect('/')

@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']
    #setting up s3 variables
    s3_resource=boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

@app.route('/delete2', methods=['POST'])
def delete2():
    key = request.form['key']
    #setting up s3 variables
    s3_resource=boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET2)

    #Deletes the object from the bucket using the key
    my_bucket.Object(key).delete()

    flash('File Deleted')
    return redirect(url_for('download'))

@app.route('/download2', methods=['POST'])
def download2():
    key = request.form['key']
    #setting up s3 variables
    s3_resource=boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET2)

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )
@app.route('/callAPI', methods=['POST','GET'])
def callAPI():
    filename = request.form['key']
    email = request.form['email']
    PARAMS = {
        'email': email,
        'filename': filename
    }
    headers = {
        'x-api-key': AWS_API_KEY
    }
    r = requests.post(url=AWS_API_GATEWAY, params=PARAMS, headers=headers)
    data = r.json()
    flash(data)
    return redirect(url_for('uploadPage'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
