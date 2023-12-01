from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, send_file, request, session

from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import File
import boto3
import os
from operator import attrgetter

from botocore.exceptions import NoCredentialsError

views = Blueprint('views',__name__)
Bucket_Name = "bucket name"

def calc_file_size(num_bytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    divisor = 1024.0
    for suffix in suffixes:
        if num_bytes < divisor:
            return f"{round(num_bytes, 2)} {suffix}"
        num_bytes /= divisor

def size_validity(filesize):
    individual_limit = 20971520
    total_limit = 2684354560

    if (filesize >= individual_limit):
        flash('File size is too big', 'error') 
        return False
    
    total_size = 0
    s3 = boto3.client('s3')
    objects = s3.list_objects_v2(Bucket='Bucket_Name')['Contents']
    for obj in objects:
        total_size += obj['Size']

    if total_size+filesize >= total_limit :
        flash('Total storage full', 'error') 
        return False
    return True


def sort_files(files, order_by):
    if order_by == 'alphabetical':
        files.sort(key=attrgetter('file_name'))
    elif order_by == 'date_asc':
        files.sort(key=attrgetter('id'))
    elif order_by == 'date_desc':
        files.sort(key=attrgetter('id'), reverse=True)
    elif order_by == 'size_asc':
        files.sort(key=attrgetter('file_size'))
    elif order_by == 'size_desc':
        files.sort(key=attrgetter('file_size'), reverse=True)
    else:
        flash('Invalid order option', category='error')
        return redirect(url_for('views.home'))
    return files

@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    order_by = request.args.get('order_by', 'date_desc')
    files = File.query.filter_by(user_id=current_user.id).all()
    files = sort_files(files, order_by)
    return render_template("home.html", user=current_user, files=files, order_by=order_by)

@views.route('/upload', methods=['GET','POST'])
@login_required
def upload():


    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file:
            filename = uploaded_file.filename
            existing_file = File.query.filter_by(user_id=current_user.id, file_name=filename).first()

            if existing_file:
               flash('A file with the same name already exists. Please choose a different name.', 'error')
               return render_template("home.html", files=files, user=current_user,  order_by=order_by)
            
            filesize = len(uploaded_file.read())
            uploaded_file.seek(0)

                
            if size_validity(filesize):

                new_file = File(file_name = filename, file_size = filesize, file_size_display = calc_file_size(filesize), user_id=current_user.id)
                db.session.add(new_file)
                db.session.commit()

                uploaded_file_record = File.query.filter_by(user_id=current_user.id, file_name=filename).first()
                if uploaded_file_record:
                    flash(f'File {filename} successfully uploaded to the database!', 'success')
                else:
                    flash('Failed to upload the file to the database. Please try again.', 'error')

                s3 = boto3.client('s3')
                s3_key = f"{current_user.id}/{filename}"
                s3.upload_fileobj(uploaded_file, 'Bucket_Name', s3_key)
           
    order_by = request.args.get('order_by', 'date_desc')
    files = File.query.filter_by(user_id=current_user.id).all()
    files = sort_files(files, order_by)
    return render_template("home.html", files=files, user=current_user,  order_by=order_by)

@views.route('/download/<int:file_id>', methods=['GET','POST'])
@login_required
def download(file_id):
    order_by = request.args.get('order_by', 'date_desc')
    files = File.query.filter_by(user_id=current_user.id).all()
    files = sort_files(files, order_by)

    file = File.query.get(file_id)
    if file:
        s3_key = f"{current_user.id}/{file.file_name}"
        s3 = boto3.client('s3')

        try:
            temp_file_path = '/tmp/temporary_download_file'
            with open(temp_file_path, 'wb') as temp_file:
                s3.download_file('Bucket_Name', s3_key, temp_file_path)
            return send_file(temp_file_path, as_attachment=True, download_name=file.file_name)
        
        except Exception as e:
            flash(f'Error downloading file: {str(e)}', category='error')
            return render_template("home.html", files=files, user=current_user,  order_by=order_by)
        
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
    else:
       flash('File not found', category='error')

    return render_template("home.html", files=files, user=current_user,  order_by=order_by)
    

@views.route('/delete/<int:file_id>', methods=['GET','POST'])
@login_required
def delete(file_id):
    if request.method == 'POST':
        file = File.query.get(file_id)
        try:
            s3 = boto3.client('s3')
            s3_key = f"{current_user.id}/{file.file_name}"
            s3.delete_object(Bucket = "Bucket_Name", Key = s3_key)

            db.session.delete(file)
            db.session.commit()

            flash('File deleted successfully', 'success')
        except Exception as e:
            flash('An error has occured', 'error')
    
    order_by = request.args.get('order_by', 'date_desc')
    files = File.query.filter_by(user_id=current_user.id).all()
    files = sort_files(files, order_by)
    return render_template("home.html", files=files, user=current_user,  order_by=order_by)




@views.route('/rename/<int:file_id>', methods=['GET','POST'])
@login_required
def rename(file_id):
    new_name = request.form.get('newName')

    if not new_name:
        flash('New name cannot be empty', 'danger')
        return render_template("home.html", files=files, user=current_user,  order_by=order_by)
    
    try:
        file = File.query.get_or_404(file_id)
        s3 = boto3.client('s3')
        s3_key = f"{current_user.id}/{file.file_name}"
        
        s3.copy_object(Bucket="Bucket_Name", CopySource=f"Bucket_Name/{s3_key}",Key=f"{current_user.id}/{new_name}")
        s3.delete_object(Bucket="Bucket_Name",Key=s3_key)

        file.file_name = new_name
        db.session.commit()
        flash('File renamed successfully', 'success')
    except Exception as e:
        flash('An error has occured', 'error')

    order_by = request.args.get('order_by', 'date_desc')
    files = File.query.filter_by(user_id=current_user.id).all()
    files = sort_files(files, order_by)
    return render_template("home.html", files=files, user=current_user,  order_by=order_by)
