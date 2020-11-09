import json
import datetime
from app import app, db
from app.models import Peptoid, Author, Residue

from tqdm import tqdm

database = open('Structure.json','r')
database = json.loads(database.read())
authors =[]
author_objects ={}
peptoid_objects = {}

residue_db = open('Residue.json','r')
residue_db = json.loads(residue_db.read())
residue_objects = {}

print('Establishing residues')

for res in residue_db:
    residue_objects[res['Long name']]=Residue(
        long_name=res['Long name'],
        short_name=res['Short name'],
        pep_type=res["Backbone"],
        SMILES = res["SMILES"]
    )


for res in tqdm(residue_objects):
    db.session.add(residue_objects[res])

print('Collecting authors')

for pep in database:
    a = pep["Authors"].split('\n')
    for auth in a:
        if auth not in authors:
            authors.append(auth)

for author in authors:
    names = author.split(', ')
    # print(names)
    author_objects[author]=Author(
        first_name=names[1],
        last_name=names[0]
    )

for author in tqdm(author_objects):
    db.session.add(author_objects[author])

print('Instantiating peptoids')

for i in range(len(database)):
    rel = database[i]["Release"]
    dates = rel.split('/')
    authors = database[i]["Authors"].split('\n')
    residues = database[i]["Sequence"].split('\n')
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
    peptoid_objects[i].peptoid_residue.extend([residue_objects[r] for r in residues])
    db.session.add(peptoid_objects[i])

db.session.commit()