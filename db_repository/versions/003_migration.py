from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
at_pase = Table('at_pase', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('source', String),
    Column('subunit_alpha', String),
    Column('organism_id', Integer),
)

organism = Table('organism', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('taxonomy', String),
    Column('org_type', String),
    Column('fof1_number', Integer),
    Column('operon_number', Integer),
)

atpases = Table('atpases', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('source', String(length=120)),
    Column('subunit_alpha', String(length=500)),
    Column('organism_id', Integer),
)

operon = Table('operon', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('number', Integer, default=ColumnDefault(1)),
    Column('atpase_id', Integer),
    Column('organism_id', Integer),
)

organisms = Table('organisms', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('taxonomy', String(length=120)),
    Column('org_type', String(length=20)),
    Column('fof1_number', Integer, default=ColumnDefault(1)),
    Column('operon_number', Integer, default=ColumnDefault(1)),
)

sequence = Table('sequence', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('subunit_name', String(length=20)),
    Column('sequence', String(length=500)),
    Column('start', Integer),
    Column('stop', Integer),
    Column('operon_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['at_pase'].drop()
    pre_meta.tables['organism'].drop()
    post_meta.tables['atpases'].create()
    post_meta.tables['operon'].create()
    post_meta.tables['organisms'].create()
    post_meta.tables['sequence'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['at_pase'].create()
    pre_meta.tables['organism'].create()
    post_meta.tables['atpases'].drop()
    post_meta.tables['operon'].drop()
    post_meta.tables['organisms'].drop()
    post_meta.tables['sequence'].drop()
