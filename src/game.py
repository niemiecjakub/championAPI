from category import category_get_list, combine_elements
import itertools
import more_itertools
import random
from pprint import pprint
from category import combine_elements

def get_category_name_value_list():
    category_data = category_get_list()
    data = []
    for category_name,category_values in category_data.items():
        for value in category_values:
            x = {
                "category": category_name,
                "name" : value
                }
            data.append(x)    
    return {"data" : data}


def get_fields(field_list, already_picked_list, field_posibility_number):
    fields_data = []
    while len(fields_data) < 3:
            n = random.randint(0, field_posibility_number)
            if n not in already_picked_list:
                field = field_list["data"][n]
                fields_data.append(field)
                already_picked_list.append(n)
    return fields_data


def ensure_game_is_possible(fields):
    n_possible_champions = []
    for field in fields:
        (i,j) = field
        [category, name] = list(i.values())
        [other_category, other_name] = list(j.values())
        print(name, other_name)
        result = combine_elements(category, name, other_category, other_name)
        n_possible_champions.append(len(result["champions"]))
    if 0 not in n_possible_champions:
        return True
    else:
        return False

def get_game_fields():
    field_list = get_category_name_value_list()
    field_posibility_number = len(field_list["data"]) - 1

    game_created = False
    while (not game_created):   
        x, y, already_picked = ([] for i in range(3))
        x = get_fields(field_list, already_picked, field_posibility_number)
        y = get_fields(field_list, already_picked, field_posibility_number)
        fields = list(itertools.product(x,y))
        game_fields = list(more_itertools.batched(fields, 3))
 
        if ensure_game_is_possible(fields):
            game_created = True
            return {"data" : {
                    "horizontal" : x,
                    "vertical" : y
                    },
                    "product": game_fields,
                    "list": fields
                }
        else:
            x, y, already_picked = ([] for i in range(3))
    return {"error" : "error"}


def init_game():
    game_fields = get_game_fields()
    return {"data" : game_fields}

