
# coding: utf-8

# In[14]:


from app import db, models
from app.models import Organism, ATPase, Operon, Sequence
    


# In[15]:


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


# In[17]:


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
    organism = Organism(name = i.name, org_id_ncbi = i.id, taxonomy = i.taxonomy, org_type = 'bacterial', fof1_number = len(i.fof1), operon_number = int(op_num), org_comment = 'No comment yet')
    #db.session.add(organism)
    for k in i.fof1:
        atpase = ATPase(source = i.name, fof1_type = k.type, subunit_list = ", ".join(k.subunit_names), organism = organism)
        #db.session.add(atpase)
        for j in range(int(k.operon_num)):
            operon = 0
            operon = Operon(number = j+1, enzyme = atpase, organism = organism)
            #db.session.add(operon)
            for h in k.subunits:
                if int(h.operon) == j+1:
                    print(h.field_type, h.start, h.end)
                    subunit = Sequence(subunit_name = h.field_type, subunit_id_ncbi = h.id, sequence = h.seq, start = h.start, stop = h.end, seq_operon_number = h.operon, seq_comment = 'No comments yet', operon = operon)
                    #db.session.add(subunit)
#db.session.commit()




# In[11]:


Sequence.query.all()

