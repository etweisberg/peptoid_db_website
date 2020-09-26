import json
import datetime
from app import app, db
from app.models import Peptoid, Author, Residue

database = open('Structure.json','r')
database = json.loads(database.read())
authors =[]
author_objects ={}
peptoid_objects = {}

# residue_db = open('Residue.json','r')
# residue_db = json.loads(residue_db.read())
# residue_objects = {}

for pep in database:
    a = pep["Authors"].split('\n')
    for auth in a:
        if auth not in authors:
            authors.append(auth)

for author in authors:
    names = author.split(', ')
    author_objects[author]=Author(
        first_name=names[1],
        last_name=names[0]
    )

# for res in residue_db:
#     residue_objects[]

for author in author_objects:
    db.session.add(author_objects[author])

for i in range(len(database)):
    rel = database[i]["Release"]
    dates = rel.split('/')
    authors = database[i]["Authors"].split('\n')
    peptoid_objects[i] = Peptoid(
        image='pep.png',
        title=database[i]['Title'],
        code=database[i]['Code'],
        release=datetime.date(int(dates[2]),int(dates[0]),int(dates[1])),
        experiment=database[i]["Experiment"],
        pub_doi=database[i]["Publication doi"],
        struct_doi=database[i]["Structure doi"],
        topology=database[i]["Topology"]
    )
    peptoid_objects[i].peptoid_author.extend([author_objects[a] for a in authors])

for i in range(len(peptoid_objects)):
    db.session.add(peptoid_objects[i])

db.session.commit()