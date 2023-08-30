from app import app,db
from flask import Flask, render_template, request,redirect,url_for,jsonify,flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from ..models import JobApplication,Job, User, Cart
from uuid import uuid4
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..confing import basedir


@app.route('/job_applications')
def job_applications():
    applications = JobApplication.query.all()
    all_apps = []
    for application in applications:
        job = Job.query.filter_by(id=application.job_id).first()
        user = User.query.filter_by(id=application.user_id).first()
        all_apps.append({
            "title":job.title,
            "description":job.description,
            "username":user.username,
            "email":user.email,
            "resume":application.resume
        })
    
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('job_applications.html', applications=all_apps, user=current_user, count = count)


# Apply for a job page
@app.route('/apply_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    email = request.form.get('email')
    # user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        if email != current_user.email:
            flash('If you are not logged in please make sure to login, and use your email, same email you are using now to apply for any job!', category='error')
            return redirect(url_for('apply_job', job_id=job_id))

        resume = request.files['resume']
        
        if resume:
            filename = str(uuid4()) + '.' + secure_filename(resume.filename).rsplit('.', 1)[1].lower()
            
            resume.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/resumes", filename))

            # Create a new job application
            application = JobApplication(
                user_id=current_user.id,
                job_id=job.id,
                resume=filename,
                cover_letter=request.form.get('message')
                # Add other application fields as needed
            )

            db.session.add(application)
            db.session.commit()
            flash('You applied Succesfully For this Job, Thank you!')
            return redirect(url_for('jobs'))
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('apply_job.html', job=job, user=current_user,job_id=job_id, count = count)


@app.route('/jobs')
def jobs():
    jobs = Job.query.all()
    
    
    all_jobs= []
    applied = False
    for job in jobs:
        
        if current_user.is_authenticated:
            check_if_applied_job = JobApplication.query.filter_by(job_id=job.id, user_id=current_user.id).first()
            if check_if_applied_job:
                applied=True

        all_jobs.append({
                "id":job.id,
                "title":job.title,
                "description" :job.description,
                "applied":applied,
                "from_salary":job.from_salary,
                "to_salary":job.to_salary,
                "percent":job.percent
                
            })
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('jobs.html', jobs=all_jobs, user=current_user, applied=applied, count = count)

@app.route('/view_application/<int:application_id>')
def view_application(application_id):
    application = JobApplication.query.get_or_404(application_id)
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('view_application.html', application=application, count = count)


@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.json.get('email')
    declineOrAcept = request.json.get('declineOrAcept')


    # Handle the email sending logic here
    # You can use a library like Flask-Mail to send emails
    # Gmail SMTP configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'selfstudyjo@gmail.com'
    sender_password = 'ahqnmotkzuqpyrqs'
    receiver_email = email
    # Email content
    subject = 'Job Application Response'
    body = render_template('email_decline_message.html')
    template = 'email_decline_message.html'
    if declineOrAcept == 'accept':
        template = 'email_accept_message.html'
    message = f'Subject: {subject}\n\n{body}'
    try:
        # Create SMTP connection
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            
            # Load template file and read its contents
            with open(f'{basedir}/templates/{template}', 'r') as file:
                template_content = file.read()
            
            # Create a multi-part email message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            
            # Attach the template content as HTML
            message.attach(MIMEText(template_content, 'html'))
            
            # Send email
            server.send_message(message)
            
        return jsonify({'message': f'Email sent successfully to : {email}'})
    
    except Exception as e:
        return jsonify({'message': f'Error : {e}'})
    


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        try:
            from_salary = int(request.form.get('from_salary'))
            to_salary = int(request.form.get('to_salary'))
            if from_salary and to_salary:
                job = Job(title=title, description=description, from_salary=from_salary, to_salary=to_salary)
        except:
            percent = request.form.get('percent')
            job = Job(title=title, description=description, percent = percent)

        db.session.add(job)
        db.session.commit()
        
        return redirect(url_for('jobs'))
    
    try:
        count = Cart.query.filter_by(uid=current_user.id).all()
        full_count = 0
        for data in count:
            full_count += data.quantity
        count = full_count
    except:
        count = 0
    return render_template('add_job.html', user=current_user, count = count)