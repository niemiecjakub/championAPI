
from flask import abort, make_response
from models import Champion, ChampionSchema

def champion_read_all():
    champions = Champion.query.all()
    return ChampionSchema(many=True).dump(champions)

def champion_read_by_name(name):
    champion = Champion.query.filter(Champion.name == name).one_or_none()

    if champion is not None:
        return ChampionSchema().dump(champion)
    else:
        abort(404, f"Champion with name {name} not found")  

def champion_read_by_key(key):
    champion = Champion.query.filter(Champion.key == key).one_or_none()

    if champion is not None:
        return ChampionSchema().dump(champion)
    else:
        abort(404, f"Champion with key {key} not found")    

def champion_read_by_id(id):
    champion = Champion.query.filter(Champion.id == id).one_or_none()

    if champion is not None:
        return ChampionSchema().dump(champion)
    else:
        abort(404, f"Champion with id {id} not found")    

def champion_name_list():
    champions = Champion.query.all()
    names = []
    for champion in champions:
        names.append(champion.name)
    return {"champions": names}
