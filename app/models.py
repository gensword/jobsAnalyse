from app import db


class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(20), nullable=False, index=True)
    salary = db.Column(db.String(15), nullable=False)
    education = db.Column(db.String(15), nullable=False)
    experience = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(10), nullable=False, index=True)
    publish_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<job {}>'.format(self.id)


