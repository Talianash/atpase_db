from app import db, models

#test1 = models.Organism(name = 'Escherichia coli O157:H7 EDL933', taxonomy = 'Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacteriales; Enterobacteriaceae; Escherichia', org_type = 'bacteria', fof1_number = 1, operon_number = 1)
#db.session.add(test1)

test2 = models.Organism(name = 'Erythrobacter litoralis HTCC2594', taxonomy = 'Bacteria; Proteobacteria; Alphaproteobacteria; Sphingomonadales; Erythrobacteraceae; Erythrobacter', org_type = 'bacteria', fof1_number = 1, operon_number = 2)
db.session.add(test2)

db.session.commit()