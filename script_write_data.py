from app import db, models
from app.models import Organism, ATPase, Operon, Sequence

import Parse_input_data_v2
organism_list, broken_orgs = Parse_input_data_v2.parce_file('data_input/Operons_formatted_231018.txt')
#print organism_list
def get_operon_num(organism):
    a = 0
    for i in organism.fof1:
        a = a + i.operon_num
    return a

def clean_db():
    from app import db, models
    from app.models import Organism, ATPase, Operon, Sequence
    for i in Organism.query.all():
        db.session.delete(i)
    db.session.commit()
    for k in ATPase.query.all():
        db.session.delete(k)
    db.session.commit()
    for j in Operon.query.all():
        db.session.delete(j)
    db.session.commit()
    for n in Sequence.query.all():
        db.session.delete(n)
    db.session.commit()

clean_db()


for i in organism_list:
    print(i.name)
    print(i.taxonomy)
    print(len(i.fof1))
    print(i.operon_num)
    organism = Organism(name = str(i.name), taxonomy = str(i.taxonomy), org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = int(i.operon_num))
    db.session.add(organism)
    db.session.commit()
    for k in i.fof1:
        atpase = ATPase(source = i.name, organism = organism, fof1_type = k.type, subunit_list = ', '.join(k.subunit_names))
        db.session.add(atpase)
        db.session.commit()
        for j in range(int(k.operon_num)):
            operon = 0
            operon = Operon(enzyme = atpase, organism = organism, operon_type = k.operon_type[j])
            db.session.add(operon)
            db.session.commit()
            for h in k.subunits:
                if int(h.operon) == j+1:
                    print(h.field_type, h.seq, h.start, h.end)
                    subunit = Sequence(subunit_name = h.field_type, subunit_id_ncbi = h.id, sequence = h.seq, start = h.start, stop = h.end, direction = h.direction, operon = operon)
                    db.session.add(subunit)
                    db.session.commit()
#db.session.commit()

#e = Organism(name = 'lol', taxonomy = 'top kek', org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = int(op_num))
#db.session.add(organism)
#db.session.commit()