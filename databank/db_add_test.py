import datetime
from app import app, db
from app.models import Peptoid, Author, Residue


#instantiating two residue examples
Nspe = Residue(nomenclature='Nspe',pep_type = 'alpha',CSD = 'BABTAA',SMILES='C1=CC=C(C=C1)C[N+](=CC2=CC=CC=C2)[O-]')
NLeu = Residue(nomenclature='NLeu',pep_type = 'beta')
Nme = Residue(nomenclature='Nme',pep_type = 'alpha')
Nspm = Residue(nomenclature='Nspm',pep_type = 'beta')
Nsrd = Residue(nomenclature='Nsrd',pep_type = 'alpha')
Nabc = Residue(nomenclature='Nabc',pep_type = 'alpha')

KK = Author(first_name = 'Kent', last_name = 'Kirshenbaum')
VV = Author(first_name = 'Vince', last_name = 'Voelz')
JE = Author(first_name='James', last_name = 'Eastwood')
AB = Author(first_name='Armand', last_name='Brooks')
CD = Author(first_name='Chris', last_name='Davidson')
EF = Author(first_name='Ed', last_name='Field')

#adding new objects to database
db.session.add(Nspe)
db.session.add(NLeu)
db.session.add(Nme)
db.session.add(Nspm)
db.session.add(Nsrd)
db.session.add(Nabc)
db.session.add(KK)
db.session.add(VV)
db.session.add(JE)
db.session.add(AB)
db.session.add(CD)
db.session.add(EF)

#testing new objects
for r in Residue.query.all():
    print (r.id,r.nomenclature)
for a in Author.query.all():
    print(a.id,a.first_name,a.last_name)

#making a peptoid object
p1 = Peptoid(
    image = 'pep1.png',
    title='Linear Dimer (benzyl side chains)',
    code = '19AB1-2-A',
    release = datetime.date(2019,7,4),
    experiment = 'X-ray crystallography',
    doi = '10.1039/C9CC02335F',
    topology = 'A'
)

p2 = Peptoid(
    image = 'pep2.png',
    title='Cyclic Octamer (propargyl and methoxyethyl side chains)',
    code = '19AA1-8-C',
    release = datetime.date(2019,7,5),
    experiment = 'X-ray crystallography',
    doi = '10.1021/acs.cgd.8b01137',
    topology = 'M'
)

p3 = Peptoid(
    image='pep3.png',
    title='Helical Pentamer (chiral alkyl side chains)',
    code='17AD2-5-A',
    release=datetime.date(2017, 7, 6),
    experiment='X-ray crystallography',
    doi='10.1021/jacs.7b07475',
    topology = 'C'
)

p4 = Peptoid(
    image='pep4.png',
    title='Helical Heptamer (chiral alkyl side chains)',
    code='17AD1-7-A',
    release=datetime.date(2017, 7, 5),
    experiment='X-ray crystallography',
    doi='10.1021/acs.joc.7b00965'
)

p5 = Peptoid(
    image='pep5.png',
    title='Cyclic Hexamer (benzyl and tert-butyl side chains)',
    code='17AC3-6-C',
    release=datetime.date(2017, 6, 5),
    experiment='X-ray crystallography',
    doi='10.1021/jacs.7b02319'
)

p6 = Peptoid(
    image='pep6.png',
    title='Cyclic Hexamer (benzyl and isopropyl side chains)',
    code='17AC2-6-C',
    release=datetime.date(2017, 6, 4),
    experiment='X-ray crystallography',
    doi='10.1038/ncomms8013'
)

p7 = Peptoid(
    image='pep7.png',
    title='Square Helical Octamer',
    code='17AB2-8-A',
    release=datetime.date(2017, 3, 4),
    experiment='NMR',
    doi='10.1039/C3CE42456A'
)

p8 = Peptoid(
    image='pep8.png',
    title='Ribbon Pentamer',
    code='17AB1-5-A',
    release=datetime.date(2017, 1, 5),
    experiment='NMR',
    doi='doi.org/10.1021/ol400820y'
)

#adding new objects to database
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(p4)
db.session.add(p5)
db.session.add(p6)
db.session.add(p7)
db.session.add(p8)


#query for peptoid objects
for p in Peptoid.query.all():
    print(p)

#creating many to many relationships
p1.peptoid_author.extend([KK,JE,CD])
p2.peptoid_author.extend([VV,JE,EF])
p3.peptoid_author.extend([KK,AB,CD,EF])
p4.peptoid_author.extend([AB,EF])
p5.peptoid_author.extend([CD,VV,KK])
p6.peptoid_author.extend([AB, CD, EF])
p7.peptoid_author.extend([AB, CD])
p8.peptoid_author.extend([KK, CD])

p1.peptoid_residue.extend([Nspe,NLeu])
p2.peptoid_residue.extend([Nme,Nspe,Nabc])
p3.peptoid_residue.extend([Nspm,NLeu,Nsrd])
p4.peptoid_residue.extend([Nsrd,Nabc,Nspe])
p5.peptoid_residue.extend([Nspe,Nabc])
p6.peptoid_residue.extend([Nsrd, Nabc])
p7.peptoid_residue.extend([Nspe, Nspm])
p8.peptoid_residue.extend([NLeu, Nsrd])

db.session.commit()
