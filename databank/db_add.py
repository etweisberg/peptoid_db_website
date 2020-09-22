import json
import datetime
from app import app, db
from app.models import Peptoid, Author, Residue

database = open('Structure.json','r')
database = json.loads(database.read())

peptoid_objects = {}
for i in range(len(database)):
    rel = database[i]["Release"]
    dates = rel.split('/')
    peptoid_objects[i] = Peptoid(
        image='pep.png',
        title=database[i]['Title'],
        code=database[i]['Code'],
        release=datetime.date(int(dates[2]),int(dates[0]),int(dates[1])),
        experiment=database[i]["Experiment"],
        doi=database[i]["Publication doi"]
    )

for i in range(len(peptoid_objects)):
    db.session.add(peptoid_objects[i])

db.session.commit()