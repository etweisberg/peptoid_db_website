import datetime
from app import app, db
from app.models import Peptoid, Author, Residue

#instantiating two residue examples
Nspe = Residue(nomenclature='Nspe')
NLeu = Residue(nomenclature='NLeu')

KK = Author(name='Kent Kirshenbaum')
VV = Author(name='Vincent Voelz')
JE = Author(name='James Eastwood')

#adding new objects to database
db.session.add(Nspe)
db.session.add(NLeu)
db.session.add(KK)
db.session.add(VV)
db.session.add(JE)

#testing new objects
for r in Residue.query.all():
    print (r.id,r.nomenclature)
for a in Author.query.all():
    print(a.id,a.name)

#making a peptoid object
p1 = Peptoid(
    title = 'Peptoid 1',
    release = datetime.date(2020,7,4),
    experiment = 'X-ray crystallography',
    doi = '10.107hj1/adk2'
)

p2 = Peptoid(
    title = 'Peptoid 2',
    release = datetime.date(2020,7,5),
    experiment = 'X-ray crystallography',
    doi = '10.107hj1/as123'
)

#adding new objects to database
db.session.add(p1)
db.session.add(p2)

#query for peptoid objects
for p in Peptoid.query.all():
    print(p)

#creating many to many relationships
p1.peptoid_author.append(KK)
p1.peptoid_author.append(JE)

p2.peptoid_author.append(VV)
p2.peptoid_author.append(KK)

p1.peptoid_residue.append(NLeu)
p1.peptoid_residue.append(Nspe)

p2.peptoid_residue.append(NLeu)

#querying all the peptoids with NLeu residue
print('ALL THE PEPTOIDS WITH THE NLeu RESIDUE | SHOULD BE P1 and P2')
for pep in NLeu.peptoids:
    print(pep)

#querying all the peptoids with Dr. K as author
print('ALL THE PEPTOIDS WITH DR K AS AUTHOR | SHOULD BE P1 and P2')
for pep in KK.peptoids:
    print(pep)

#querying all the residues for peptoid 1
print('ALL THE RESIDUES IN PEPTOID 1 | SHOULD BE NLeu and Nspe')
for res in p1.peptoid_residue:
    print(res)

#querying all the authors for peptoid 2
print('ALL THE AUTHORS FOR PEPTOID 2 | SHOULD BE VV AND KK')
for res in p2.peptoid_author:
    print(res)