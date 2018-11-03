from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
atpases = Table('atpases', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('source', String(length=120)),
    Column('fof1_type', String(length=20)),
    Column('subunit_list', String(length=200)),
    Column('add_prot_list', String(length=200), default=ColumnDefault('')),
    Column('organism_id', Integer),
)

organisms = Table('organisms', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('org_id_ncbi', String(length=50)),
    Column('taxonomy', String(length=120)),
    Column('org_type', String(length=20)),
    Column('fof1_number', Integer, default=ColumnDefault(1)),
    Column('operon_number', Integer, default=ColumnDefault(1)),
    Column('org_comment', String(length=500)),
)

sequence = Table('sequence', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('subunit_name', String(length=20)),
    Column('subunit_id_ncbi', String(length=50)),
    Column('sequence', String(length=500)),
    Column('start', Integer),
    Column('stop', Integer),
    Column('seq_operon_number', Integer),
    Column('seq_comment', String(length=500)),
    Column('operon_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['atpases'].columns['fof1_type'].create()
    post_meta.tables['atpases'].columns['subunit_list'].create()
    post_meta.tables['organisms'].columns['org_comment'].create()
    post_meta.tables['organisms'].columns['org_id_ncbi'].create()
    post_meta.tables['sequence'].columns['seq_comment'].create()
    post_meta.tables['sequence'].columns['seq_operon_number'].create()
    post_meta.tables['sequence'].columns['subunit_id_ncbi'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['atpases'].columns['fof1_type'].drop()
    post_meta.tables['atpases'].columns['subunit_list'].drop()
    post_meta.tables['organisms'].columns['org_comment'].drop()
    post_meta.tables['organisms'].columns['org_id_ncbi'].drop()
    post_meta.tables['sequence'].columns['seq_comment'].drop()
    post_meta.tables['sequence'].columns['seq_operon_number'].drop()
    post_meta.tables['sequence'].columns['subunit_id_ncbi'].drop()
