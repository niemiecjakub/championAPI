from config import db, ma
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, Schema, post_dump

champion_legacy = db.Table('champion_legacy',
                    db.Column('champion_id', db.Integer, db.ForeignKey('champion.id')),
                    db.Column('legacy_id', db.Integer, db.ForeignKey('legacy.id'))
                    )

champion_position = db.Table('champion_position',
                    db.Column('champion_id', db.Integer, db.ForeignKey('champion.id')),
                    db.Column('position_id', db.Integer, db.ForeignKey('position.id'))
                    )

champion_resource = db.Table('champion_resource',
                    db.Column('champion_id', db.Integer, db.ForeignKey('champion.id')),
                    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
                    )

champion_rangetype = db.Table('champion_rangetype',
                    db.Column('champion_id', db.Integer, db.ForeignKey('champion.id')),
                    db.Column('rangetype_id', db.Integer, db.ForeignKey('rangetype.id'))
                    )

champion_region = db.Table('champion_region',
                    db.Column('champion_id', db.Integer, db.ForeignKey('champion.id')),
                    db.Column('region_id', db.Integer, db.ForeignKey('region.id'))
                    )

class Champion(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    key = db.Column(db.String, unique=True)
    name = db.Column(db.String, unique=True)
    title = db.Column(db.String, unique=True)

    legacy = db.relationship('Legacy', secondary=champion_legacy, backref='champions')
    position = db.relationship('Position', secondary=champion_position, backref='champions')
    resource = db.relationship('Resource', secondary=champion_resource, backref='champions')
    rangetype = db.relationship('Rangetype', secondary=champion_rangetype, backref='champions')
    region = db.relationship('Region', secondary=champion_region, backref='champions')

    def __init__(self, id, key, name, title, image):
        self.id = id
        self.key = key
        self.name = name
        self.title = title
        self.image = image

    def __repr__(self):
        return f"<Champion: {self.name}>"

class Legacy(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, id,name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Legacy: {self.name}>"

class Position(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Position {self.name}>"

class Resource(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Resource {self.name}>"

class Rangetype(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Rangetype {self.name}>"

class Region(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Region {self.name}>"
    
class LeagcySchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    champions = fields.Pluck("ChampionSchema", "name", many=True)

class PositionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    champions = fields.Pluck("ChampionSchema", "name", many=True)

class ResoureSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    champions = fields.Pluck("ChampionSchema", "name", many=True)

class RangetypeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    champions = fields.Pluck("ChampionSchema", "name", many=True)

class RegionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    champions = fields.Pluck("ChampionSchema", "name", many=True)

    
class ChampionSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Int()
    name = fields.Str()
    key = fields.Str()
    title = fields.Str()

    legacy= fields.Pluck("LeagcySchema", "name", many=True)
    position = fields.Pluck("PositionSchema", "name", many=True)
    resource = fields.Pluck("ResoureSchema", "name", many=True)
    rangetype = fields.Pluck("RangetypeSchema", "name", many=True)
    region = fields.Pluck("RegionSchema", "name", many=True)
