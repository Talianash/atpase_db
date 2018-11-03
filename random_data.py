from app import db, models
from app.models import Organism, ATPase, Operon, Sequence
import random, string

def get_some_names():
    list_of_names = []
    f = open('app/static/bacteria_list.txt', 'r')

    for line in f:
	    l = line.strip().split()
	    #print(l)
	    if len(l) > 2 and (l[0] != 'Note' or l[0] != 'Reference' or l[0] != '\xc2\xa4'):
	        name = l[1] + " " + l[2]
	    if (name in list_of_names) == False:
	    	list_of_names.append(name)

    f.close()
    return list_of_names

#names = get_some_names()

def add_organism(name, tax, org_type, fof1_num, operon_num):
	org = Organism(name = name, taxonomy = tax, org_type = org_type, fof1_number = fof1_num, operon_number = operon_num)
	db.session.add(org)

	return 0

#for i in range(10):
#	name = random.choice(names)
#	tax = ''.join([random.choice(string.letters) for i in range(20)])
#	org_type = 'bacteria'
#	fof1_num = random.choice([1, 2])
#	operon_num = random.choice([1, 2])
	#add_organism(name, tax, org_type, fof1_num, operon_num)

#db.session.commit()
a = Organism.query.all()
#org = Organism.query.get(1)
#print(org.name, org.taxonomy, org.org_type, org.fof1_number, org.operon_number)

#for i in a:
#	enz = ATPase(source = i.name, subunit_alpha = 'some seq', organism = i)
#	db.session.add(enz)

#db.session.commit()
enzyme = ATPase.query.all()
print(enzyme[0].organism.operon_number) 

#for i in enzyme:
#	if i.organism.operon_number == 1:
#		op = Operon(number = 1, enzyme = i, organism = i.organism)
#		db.session.add(op)
#	elif i.organism.operon_number == 2:
#		op = Operon(number = 1, enzyme = i, organism = i.organism)
#		db.session.add(op)
#		op = Operon(number = 2, enzyme = i, organism = i.organism)
#		db.session.add(op)

#db.session.commit()
operons = Operon.query.all()
print(operons)

subunits = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'b', 'c', 'a', 'I']
for i in operons:
	k = i.sequence
	print(k)
	for a in range(len(subunits)):
		i.subunit_name[a] = subunits[a] 
#		seq_len = random.randint(50, 150)
#		start = random.randint(0, 1500)
#		stop = start + seq_len
#		sequence = ''.join([random.choice(string.ascii_uppercase) for k in range(seq_len)])
#		seq_all = Sequence(subunit_name = sub, sequence = sequence, start = start, stop = stop, operon = i)
#		db.session.add(seq_all)
#db.session.commit()
sequences = Sequence.query.all()
print(sequences) 