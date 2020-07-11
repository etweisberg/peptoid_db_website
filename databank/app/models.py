#from the app module imports db instance of SQLAlchemy application
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

#peptoid table: image file name, title to display on page, data base code, release date,
# experimental technique, doi of publication, relationship with the author and residue
class Peptoid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, index=True, unique=True)
    title = db.Column(db.Text, index=True, unique=True)
    code = db.Column(db.String(16), index=True, unique=True)
    release = db.Column(db.DateTime, index=True, unique=True)
    experiment = db.Column(db.Text, index=True, unique=False)
    doi = db.Column(db.String(32), index=True, unique=True)
    
    peptoid_author = db.relationship('Author',secondary = peptoid_author, lazy = 'dynamic',
        backref = db.backref('peptoids'))
    peptoid_residue = db.relationship('Residue',secondary = peptoid_residue, lazy = 'dynamic',
        backref = db.backref('peptoids'))
    
    def __repr__(self):
        return '<Peptoid {}>'.format(self.title) 


#authors table: first name and last name
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, index = True, unique = True)
    last_name = db.Column(db.Text, index = True, unique = True)

    def __repr__(self):
        return '<Author {}>'.format(self.last_name)

#residues table: nomenclature
class Residue(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nomenclature = db.Column(db.Text, index = True, unique = True)

    def __repr__(self):
        return '<Residue {}>'.format(self.nomenclature)