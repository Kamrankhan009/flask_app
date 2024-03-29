
from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user, login_required
from ..models import User, Product, Cart, color_management
from werkzeug.utils import secure_filename
import os
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
import requests
from oauthlib.oauth2 import WebApplicationClient

DISCORD_CLIENT_ID = "1143875517909565480"
DISCORD_CLIENT_SECRET = "NzMcQtK_LtU_c295TITCUXnjYMksY09B"
DISCORD_REDIRECT_URI = "http://localhost:5000/callback"
DISCORD_API_BASE_URL = "https://discord.com/api"
DISCORD_OAUTH_AUTHORIZE_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_OAUTH_TOKEN_URL = "https://discord.com/api/oauth2/token"

client = WebApplicationClient(DISCORD_CLIENT_ID)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    # Check if the current user is an admin
    if current_user.is_admin:
        if request.method == 'POST':
            # Toggle the visibility of the jobs page
            current_user.jobs_page_visible = not current_user.jobs_page_visible
            db.session.commit()

        return render_template('dashboard/admin_settings.html', admin=current_user)
    else:
        # Redirect non-admin users to a different page or show an error message
        return redirect(url_for('home'))
    

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
            print("here")
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




@app.route('/admin_update_profile', methods=['POST'])
@login_required
def admin_update_profile():
    # Get the uploaded file
    image = request.files['image']
    banner = request.files['banner']
    new_email = request.form.get('email')
    new_username = request.form.get('username')

    # Check if any field is being updated
    if image or banner or new_email or new_username:
        if image and allowed_file(image.filename):
            print("here")
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
        return redirect(url_for('admin_profile'))
    else:
        flash('No fields were updated.', 'error')
        return redirect(url_for('admin_edit_profile'))

@app.route('/profile')
@login_required
def profile():
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('profile.html',user=current_user, count = count)





@app.route('/edit_profile')
@login_required
def edit_profile():
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('edit_profile.html',user=current_user, count = count)

@app.route('/admin_profile')
@login_required
def admin_profile():
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('dashboard/profile.html',user=current_user, count = count)

@app.route('/admin_edit_profile')
@login_required
def admin_edit_profile():
    count = Cart.query.filter_by(uid=current_user.id).all()
    full_count = 0
    for data in count:
        full_count += data.quantity
    count = full_count
    return render_template('dashboard/edit_profile.html',user=current_user, count = count)


@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    user_id = current_user.id  # Replace with the actual user ID (you need to identify the logged-in user)

    try:
        user = User.query.get(user_id)
        if user:
            user.latitude = data['latitude']
            user.longitude = data['longitude']
            db.session.commit()
            return {'status': 'success', 'message': 'Location updated successfully'}
        else:
            return {'status': 'error', 'message': 'User not found'}
    except SQLAlchemyError as e:
        db.session.rollback()
        return {'status': 'error', 'message': 'Failed to update location'}

@app.route('/get_user_location/<id>', methods=['GET'])
def get_user_location(id):
    print()
    print()
    print()
    print()
    user_id = id # Replace with the actual user ID (you need to identify the logged-in user)
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify({'status': 'success', 'latitude': user.latitude, 'longitude': user.longitude})
        else:
            return jsonify({'status': 'error', 'message': 'User not found'})
    except SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': 'Failed to fetch user location'})


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    from datetime import datetime
    current_time = datetime.now()
    print(current_time)
    color = color_management.query.filter_by(class_name="user_color").first()
    return render_template('dashboard/users.html', users = users, user = current_user, color = color,current_time=current_time)



@app.route("/info_user/<id>")
def info_user(id):
    users = User.query.get(id)
    return render_template("dashboard/info_user.html", user = current_user, users = users)


@app.route("/delete_user/<id>")
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



ALLOWED_EXTENSIONS = {'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/banner_change', methods=['POST', "GET"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'white.png'
            file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", filename))
            return redirect("/banner_change")
        else:
            return 'Invalid file format. Only PNG files are allowed.'
        
        
    print(app.config['UPLOAD_FOLDER'])
    return render_template("dashboard/banner.html", user = current_user, upload_folder = f"{app.config['UPLOAD_FOLDER']}/users/white.png")


@app.route('/profile_change', methods=['POST', "GET"])
def profile_file():
    if request.method == "POST":
        if 'profile_file' not in request.files:
            return redirect(request.url)

        file = request.files['profile_file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = 'actor.png'
            file.save(os.path.join(f"{app.config['UPLOAD_FOLDER']}/users", filename))
            return redirect("/banner_change")
        else:
            return 'Invalid file format. Only PNG files are allowed.'
    print(app.config['UPLOAD_FOLDER'])
    return render_template("banner.html", user = current_user, upload_folder = f"{app.config['UPLOAD_FOLDER']}/users/white.png")

@app.route("/discord_login")
def discord_login():
    redirect_uri = client.prepare_request_uri(DISCORD_OAUTH_AUTHORIZE_URL, redirect_uri=DISCORD_REDIRECT_URI, scope=["identify"])
    return redirect(redirect_uri)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url, headers, body = client.prepare_token_request(DISCORD_OAUTH_TOKEN_URL, code=code, redirect_url=DISCORD_REDIRECT_URI)
    token_response = requests.post(token_url, headers=headers, data=body, auth=(DISCORD_CLIENT_ID, DISCORD_CLIENT_SECRET))

    client.parse_request_body_response(token_response.content.decode("utf-8"))

    userinfo_url = f"{DISCORD_API_BASE_URL}/users/@me"
    userinfo_response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {client.token['access_token']}"})
    user_info = userinfo_response.json()

    avatar_hash = user_info["avatar"]
    user_id = user_info['id']
    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"

    user_name = user_info['username']
    current_user.username = user_name

    print(avatar_url)
    current_user.image = avatar_url
    db.session.commit()
    return redirect("/profile")


@app.route("/Admin_Page")
def admin_page():
    notification = True
    return render_template("dashboard/base.html", user = current_user, notification = notification)

# @app.route("/admin")
# def admin_testing():
#     return render_template("dashboard/base.html")