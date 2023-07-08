from app import db



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Notification(id={self.id}, user_id={self.user_id}, body={self.body})"
