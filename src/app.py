import config
from flask import render_template, request, session, redirect, url_for
from champions import champion_read_all, champion_read_by_key
from category import category_read_all, category_read_by_key, category_get_list
from flask_cors import cross_origin
from flask_socketio import join_room, leave_room, send, emit
import random
from string import ascii_uppercase


app = config.connex_app.app

@app.route("/")
@cross_origin()
def home():
    category_list = category_get_list()
    return render_template("home.html", category_list=category_list)

#CHAMPION
@app.route("/champion")
@cross_origin()
def champions():
    champions = champion_read_all()
    return render_template("champions.html", champions=champions)

@app.route("/champion/<key>")
@cross_origin()
def champion(key):
    champion = champion_read_by_key(key)
    return render_template("champion.html", champion=champion)

@app.route("/<category>")
@cross_origin()
def cateogies(category):
    data = category_read_all(category)
    return render_template("categories.html", category=category, data=data )

@app.route("/<category>/<name>")
@cross_origin()
def category(category, name):
    category = category_read_by_key(category, name)
    return render_template("category.html", category=category, name=name)


# ROOMS
rooms = {}

def generate_room_code(length) :
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


@app.route("/roomlobby", methods = ["POST", "GET"])
@cross_origin()
def browse_rooms():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("roomlobby.html", error="Please enter name")
        if join != False and not code:
            return render_template("roomlobby.html", error="Please enter room code")
    
        room = code
        if create != False:
            room = generate_room_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("roomlobby.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))


    return render_template("roomlobby.html")


@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("roomlobby"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


@config.socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@config.socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@config.socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":  
    # app.run(host="0.0.0.0", port=8000, debug=True)
    config.socketio.run(app, host="0.0.0.0", port=8000, debug=True)


