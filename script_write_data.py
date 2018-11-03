from app import db, models
from app.models import Organism, ATPase, Operon, Sequence

import Parse_input_data
organism_list = Parse_input_data.parce_file('data_input/Test_input_ATPase1.txt')
print organism_list
def get_operon_num(organism):
    a = 0
    for i in organism.fof1:
        a = a + i.operon_num
    return a

get_operon_num(organism_list[6])

for i in organism_list:
    op_num = get_operon_num(i)
    print(i.name)
    print(i.taxonomy)
    print(len(i.fof1))
    print(op_num)
    organism = Organism(name = str(i.name), taxonomy = str(i.taxonomy), org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = int(op_num))
    db.session.add(organism)
    db.session.commit()
    for k in i.fof1:
        atpase = ATPase(source = i.name, organism = organism)
        db.session.add(atpase)
        db.session.commit()
        for j in range(int(k.operon_num)):
            operon = 0
            operon = Operon(number = j+1, enzyme = atpase, organism = organism)
            db.session.add(operon)
            db.session.commit()
            for h in k.subunits:
                if int(h.operon) == j+1:
                    print(h.field_type, h.seq, h.start, h.end)
                    subunit = Sequence(subunit_name = h.field_type, sequence = h.seq, start = h.start, stop = h.end, operon = operon)
                    db.session.add(subunit)
                    db.session.commit()
#db.session.commit()

e = Organism(name = 'lol', taxonomy = 'top kek', org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = int(op_num))
db.session.add(organism)
db.session.commit()