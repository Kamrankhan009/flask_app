
from app import app, db
from flask import render_template,jsonify, request, flash, redirect, url_for
from flask_login import current_user
from ..models import User,LeaderboardList,Cart

@app.route('/leaderboard')
def leaderboard():
    # Retrieve the most active users from the database
    active_users = User.query.order_by(User.duration.desc()).limit(10).all()
    count = Cart.query.filter_by(uid=current_user.id).count()
    return render_template('leaderboard.html', active_users=active_users,user=current_user, count = count)


@app.route('/leaderboard_rank')
def leaderboard_rank():
    # Retrieve the most active users from the database
    ranked_users = LeaderboardList.query.order_by(LeaderboardList.rank).all()
    if current_user.is_authenticated:
        active_users = []
        admin_list =[]
        if not current_user.is_admin:
            admin_list = User.query.filter_by(is_admin=True).all()
        for user in ranked_users:
            filter_user = User.query.filter_by(id=user.user_id).first()
            active_users.append(
                {   
                    "id":filter_user.id,
                    "image":filter_user.image,
                    "rank":user.rank,
                    "username":user.username,
                    "email":user.email,
                    "banner":filter_user.banner
                }
            )
        is_in_board = False
        user_in_rboeard = LeaderboardList.query.filter_by(user_id=current_user.id).first()
        if user_in_rboeard:
            is_in_board = True
        count = Cart.query.filter_by(uid=current_user.id).count()
        return render_template('testing.html', active_users=active_users,user=current_user, admin_list=admin_list,is_in_board=is_in_board, count = count)
    else:
        active_users = []
        for user in ranked_users:
            filter_user = User.query.filter_by(id=user.user_id).first()
            active_users.append(
                {   
                    "id":filter_user.id,
                    "image":filter_user.image,
                    "rank":user.rank,
                    "username":user.username,
                    "email":user.email,
                    "banner":filter_user.banner
                }
            )
        is_in_board = False
        count = Cart.query.filter_by(uid=current_user.id).count()
        return render_template('testing.html', active_users=active_users,user=current_user, admin_list=[],is_in_board=is_in_board, count = count)