
from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User, Product
from werkzeug.utils import secure_filename
import os
from uuid import uuid4


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    # Get the uploaded file
    image = request.files['image']
    banner = request.files['banner']
    new_email = request.form.get('email')
    new_username = request.form.get('username')

    # Check if any field is being updated
    if image or banner or new_email or new_username:
        if image and allowed_file(image.filename):
            # Generate a new filename using UUID
            new_filename = str(uuid4()) + '.' + image.filename.rsplit('.', 1)[1].lower()
            # Remove the old profile picture if it exists
            if current_user.image:
                old_filename = current_user.image
                if old_filename != 'actor.png':
                    # Remove the old file from the uploads folder
                    old_file_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
            # Save the uploaded image with the new filename
            image.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", new_filename))
            # Update the user's image filename in the database
            current_user.image = new_filename

        if banner and allowed_file(banner.filename):
            # Generate a new filename using UUID
            new_banner = str(uuid4()) + '.' + banner.filename.rsplit('.', 1)[1].lower()
            # Remove the old banner if it exists
            if current_user.banner:
                old_filename = current_user.banner
                if old_filename != 'white.png':
                    # Remove the old file from the uploads folder
                    old_file_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
            # Save the uploaded banner with the new filename
            banner.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", new_banner))
            # Update the user's banner filename in the database
            current_user.banner = new_banner

        # Update email if provided
        if new_email:
            current_user.email = new_email

        # Update username if provided
        if new_username:
            current_user.username = new_username

        db.session.commit()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    else:
        flash('No fields were updated.', 'error')
        return redirect(url_for('edit_profile'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',user=current_user)


@app.route('/edit_profile')
@login_required
def edit_profile():
    return render_template('edit_profile.html',user=current_user)

