from app import db


class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    resume = db.Column(db.String(256))
    cover_letter = db.Column(db.String(300))




class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(300))
    from_salary = db.Column(db.Integer, default=0)
    to_salary = db.Column(db.Integer, default=0)