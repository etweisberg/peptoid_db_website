from app import app, db
from app.models import Peptoid, Author, Residue
from tqdm import tqdm

for p in tqdm(Peptoid.query.all()):
    db.session.delete(p)

db.session.commit()

for r in tqdm(Residue.query.all()):
    db.session.delete(r)

db.session.commit()

for a in tqdm(Author.query.all()):
    db.session.delete(a)

db.session.commit()
