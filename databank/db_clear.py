from app import app, db
from app.models import Peptoid, Author, Residue

for p in Peptoid.query.all():
    db.session.delete(p)

db.session.commit()

for r in Residue.query.all():
    db.session.delete(r)

db.session.commit()

for a in Author.query.all():
    db.session.delete(a)

db.session.commit()
