from app import db

#peptoid-author helper table

peptoid_author = db.Table('peptoid-author',
    db.Column('peptoid_id',db.Integer,db.ForeignKey('peptoid.id'),primary_key = True),
    db.Column('author_id',db.Integer,db.ForeignKey('author.id'),primary_key = True)
)

#peptoid-residue helper table
peptoid_residue = db.Table('peptoid-residue',
    db.Column('peptoid_id',db.Integer,db.ForeignKey('peptoid.id'),primary_key = True),
    db.Column('residue_id',db.Integer,db.ForeignKey('residue.id'),primary_key = True)
)
#peptoid table
class Peptoid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, index=True, unique=True)
    release = db.Column(db.DateTime, index=True, unique=True)
    authors = db.Column(db.Text, index=True, unique=True)
    experiment = db.Column(db.Text, index=True, unique=True)
    doi = db.Column(db.Text, index=True, unique=True)
    peptoid_author = db.relationship('Author',secondary = peptoid_author, lazy = 'subquery',
        backref = db.backref('peptoids', lazy = True))
    peptoid_residue = db.relationship('Residue',secondary = peptoid_residue, lazy = 'subquery',
        backref = db.backref('peptoids', lazy = True))
    def __repr__(self):
        return '<Peptoid {}>'.format(self.title) 

#authors table

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, index = True, unique = True)

    def __repr__(self):
        return '<Author {}>'.format(self.name)

#residues table
class Residue(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nomenclature = db.Column(db.Text, index = True, unique = True)