from app import app,db
from flask_login import current_user, login_required
from ..models import Notification, LeaderboardList, User
from flask import jsonify, request
from sqlalchemy import text

@app.route('/get_notifications')
@login_required
def get_notifications():
    user_id = current_user.id  # Replace with your own method to get the current user ID
    notifications = Notification.query.filter_by(user_id=user_id).all()

    # Convert notifications to a JSON-serializable format
    notifications_json = [
        {'id': notification.id, 'user_id': notification.user_id, 'body': notification.body, 'type':notification.type, 'sender_id':notification.sender_id,'sender_name':User.query.filter_by(id=notification.sender_id).first().username}
        for notification in notifications
    ]

    notification_count = len(notifications)
    return jsonify(notification_count=notification_count, notifications=notifications_json)


@app.route('/create_notification/<int:user_id>', methods=['POST'])
def create_notification(user_id):
    notification_body = request.form.get('body')  
    notification_type = request.form.get('type')
    sender_id = request.form.get('sender_id')  

    # Code to create the notification for the specified user ID and notification body
    # You can use the SQLAlchemy ORM to create a new Notification object and save it to the database
    # Example:
    notification = Notification(user_id=user_id, body=notification_body,type=notification_type,sender_id=sender_id)
    db.session.add(notification)
    db.session.commit()
    return 'Notification created successfully'

@app.route('/accept_user_notification/<int:notificationId>', methods=['POST'])
def accept_user_notification(notificationId):
    sender_user = request.form.get('sender_user')  

    user = User.query.filter_by(username=sender_user).first()
    check_user = LeaderboardList.query.filter_by(user_id=user.id).first()
    if not check_user:
        ad_user_to_board = LeaderboardList(user_id=user.id,username = user.username, email=user.email, rank=len(LeaderboardList.query.all())+1)
        db.session.add(ad_user_to_board)
        db.session.commit()


        return 'Notification created successfully'
    else:

        return 'User Already Exists!'



@app.route('/delete_notification/<int:notificationId>', methods=['POST'])
def delete_notification(notificationId):

    notification = Notification.query.filter_by(id=notificationId).first()
    if notification:
        # Delete the cart item from the database
        db.session.delete(notification)
        db.session.commit()
    return 'Notification deleted successfully'


# Route to delete all notifications
@app.route('/delete_all_notifications/<int:user_id>', methods=['GET', 'POST'])
def delete_all_notifications(user_id):
    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return 'All notifications deleted successfully'