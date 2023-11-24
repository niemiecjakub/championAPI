
from flask import abort, make_response
from models import Legacy, LeagcySchema, Position, PositionSchema, Resource, ResoureSchema, Rangetype, RangetypeSchema, Region, RegionSchema
import collections

def category_read_all(category):
    category = category.lower()
    match category:
        case "legacy":
            data = Legacy.query.all()
            return LeagcySchema(many=True).dump(data)
        case "position":
            data = Position.query.all()
            return PositionSchema(many=True).dump(data)
        case "resource":
            data = Resource.query.all()
            return ResoureSchema(many=True).dump(data)
        case "rangetype":
            data = Rangetype.query.all()
            return RangetypeSchema(many=True).dump(data)
        case "region":
            data = Region.query.all()
            return RegionSchema(many=True).dump(data)
    return {"message": {"no data"}}

def category_read_by_key(category, name):
    category = category.lower()
    name = name.capitalize()
    match category:
        case "legacy":
            data = Legacy.query.filter(Legacy.name == name).one_or_none()
            return LeagcySchema().dump(data)
        case "position":
            data = Position.query.filter(Position.name == name).one_or_none()
            return PositionSchema().dump(data)
        case "resource":
            data = Resource.query.filter(Resource.name == name).one_or_none()
            return ResoureSchema().dump(data)
        case "rangetype":
            data = Rangetype.query.filter(Rangetype.name == name).one_or_none()
            return RangetypeSchema().dump(data)
        case "region":
            data = Region.query.filter(Region.name == name).one_or_none()
            return RegionSchema().dump(data)
    return {"message": {"no data"}}

def combine_elements(category, name, other_category, other_name):
    category_data = category_read_by_key(category, name)
    other_category_data = category_read_by_key(other_category, other_name)

    intersected_list = []
    for element in category_data["champions"]:
        if element in other_category_data["champions"]:
                intersected_list.append(element)

    return {"champions" : intersected_list}

def category_get_list():
    legacy_names = [legacy.name for legacy in Legacy.query.all()]
    position_names = [position.name for position in Position.query.all()]
    resource_names = [resource.name for resource in Resource.query.all()]
    rangetype_names = [rangetype.name for rangetype in Rangetype.query.all()]
    region_names = [region.name for region in Region.query.all()]

    category_names = {
        'legacy': legacy_names,
        'position': position_names,
        'resource': resource_names,
        'rangetype': rangetype_names,
        'region': region_names,
    }

    return category_names
