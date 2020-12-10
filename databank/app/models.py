# from the app module imports db instance of SQLAlchemy application
from app import db
import datetime
from flask import url_for

# peptoid-author helper table
peptoid_author = db.Table('peptoid-author',
                          db.Column('peptoid_id', db.Integer, db.ForeignKey(
                              'peptoid.code'), primary_key=True),
                          db.Column('author_id', db.Integer, db.ForeignKey(
                              'author.id'), primary_key=True)
                          )

# peptoid-residue helper table
peptoid_residue = db.Table('peptoid-residue',
                           db.Column('peptoid_id', db.Integer, db.ForeignKey(
                               'peptoid.code'), unique=False),
                           db.Column('residue_id', db.Integer, db.ForeignKey(
                               'residue.id'), unique=False)
                           )

# peptoid table: image file name, title to display on page, data base code, release date,
# experimental technique, doi of publication, relationship with the author and residue


class Peptoid(db.Model):
    code = db.Column(db.String(16), primary_key=True)
    image = db.Column(db.Text, index=True, unique=False)
    title = db.Column(db.Text, index=True, unique=False)
    release = db.Column(db.DateTime, index=True, unique=False)
    experiment = db.Column(db.Text, index=True, unique=False)
    pub_doi = db.Column(db.String(32), index=True, unique=False)
    struct_doi = db.Column(db.String(32), index=True, unique=False)
    topology = db.Column(db.String(1), index=True, unique=False)
    sequence = db.Column(db.String(1024), index=True, unique=False)

    peptoid_author = db.relationship('Author', secondary=peptoid_author, lazy='dynamic',
                                     backref=db.backref('peptoids',order_by='Peptoid.release.desc()'))
    peptoid_residue = db.relationship('Residue', secondary=peptoid_residue, lazy='dynamic',
                                      backref=db.backref('peptoids',order_by='Peptoid.release.desc()'))

    def to_dict(self):
        data = {
            'title': self.title,
            'release': self.release,
            'experiment': self.experiment,
            'pub_doi': self.pub_doi,
            'struct_doi': self.struct_doi,
            'topology': self.topology,
            '_links': {
                'self': url_for('api.get_peptoid', code=self.code),
                'residues': url_for('api.get_residues', code=self.code),
                'authors': url_for('api.get_authors', code=self.code),
                'image': url_for('static', filename=self.code[:5]+'.png')
            }
        }
        return data

    def __repr__(self):
        return '<Peptoid {}>'.format(self.title)


# authors table: first name and last name
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, index=True, unique=False)
    last_name = db.Column(db.Text, index=True, unique=False)

    def to_dict(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            '_links':{}
        }
        for p in self.peptoids:
            data['_links'][p.code]=url_for('api.get_peptoid',code=p.code)
        return data

    def __repr__(self):
        return '<Author {}>'.format(self.last_name)

# residues table: nomenclature


class Residue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_name = db.Column(db.Text, index=True, unique=False)
    short_name = db.Column(db.Text, index=True, unique=False)
    pep_type = db.Column(db.Text, index=True, unique=False)
    CSD = db.Column(db.Text, index=True, unique=False)
    SMILES = db.Column(db.Text, index=True, unique=False)

    def to_dict(self):
        data = {
            'full_nomenclature': self.long_name,
            'short_name': self.short_name,
            'type': self.pep_type,
            'CSD ID':self.CSD,
            'SMILES':self.SMILES,
            '_links':{}
        }
        for p in self.peptoids:
            data['_links'][p.code]=url_for('api.get_peptoid',code=p.code)
        return data

    def __repr__(self):
        return '<Residue {}>'.format(self.long_name)
