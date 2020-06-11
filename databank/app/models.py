from app import db

class Peptoid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True)
    chem_identity = db.Column(db.String(128), index=True, unique=True)
    authors = db.Column(db.String(128), index=True, unique=True)
    experiment = db.Column(db.String(64), index=True, unique=True)
    citation = db.Column(db.String(128), index=True, unique=True)
    def __repr__(self):
        return '<Peptoid {}>'.format(self.code) 
