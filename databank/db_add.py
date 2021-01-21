import json
import datetime
from app import app, db
from app.models import Peptoid, Author, Residue
from tqdm import tqdm
from termcolor import colored

database = open('Structure.json','r',encoding='utf-8')
database = json.loads(database.read())
authors =[]
author_objects ={}
peptoid_objects = {}

residue_db = open('Residue.json','r',encoding='utf-8')
residue_db = json.loads(residue_db.read())
residue_objects = {}

print('Retrieving Residues...')
for res in tqdm(residue_db):
    if res['Long name'] == '':
        print(colored(f'Invalid Residue Long Name in:\n\n\t\t{res}','red'))
        exit()
    residue_objects[res['Long name']]=Residue(
        long_name=res['Long name'],
        short_name=res['Short name'],
        monomer_structure=res['monomer structure'],
        pep_type=res["Backbone"],
        SMILES = res["SMILES"]
    )

print('Adding Residues to DB...')
for res in tqdm(residue_objects):
    db.session.add(residue_objects[res])

print('Retrieving Author Lists...')
for pep in tqdm(database):
    a = pep["Authors"].split('\n')
    for auth in a:
        if auth not in authors:
            authors.append(auth)

print('Retrieving Authors...')
for author in tqdm(authors):
    names = author.split(', ')
    # print(names)
    author_objects[author]=Author(
        first_name=names[1],
        last_name=names[0]
    )

print('Adding Authors to DB...')
for author in tqdm(author_objects):
    db.session.add(author_objects[author])

print('Retrieving and Adding Peptoids to DB...')
for i in tqdm(range(len(database))):
    rel = database[i]["Release"]
    dates = rel.split('/')
    authors = database[i]["Authors"].split('\n')
    residues = database[i]["Sequence"].split('\n')
    peptoid_objects[i] = Peptoid(
        title=database[i]['Title'],
        code=database[i]['Code'],
        release=datetime.date(int(dates[2]),int(dates[0]),int(dates[1])),
        experiment=database[i]["Experiment"],
        pub_doi=database[i]["Publication doi"],
        struct_doi=database[i]["Structure doi"],
        topology=database[i]["Topology"],
        sequence=", ".join(residues)
    )
    peptoid_objects[i].peptoid_author.extend([author_objects[a] for a in authors])
    try:
        peptoid_objects[i].peptoid_residue.extend([residue_objects[r] for r in residues])
    except:
        for r in residues:
            if r not in residue_objects:
                print(colored(f'Residue.json Missing Definition of: {r}','red'))
                exit()
    db.session.add(peptoid_objects[i])

print(colored('Committing changes...','green'))
db.session.commit()
