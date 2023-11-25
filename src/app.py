
import config
from flask import render_template
from champions import champion_read_all, champion_read_by_key
from category import category_read_all, category_read_by_key, category_get_list
from flask_cors import CORS, cross_origin

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")
CORS(app.app) 
app.app.config['CORS_HEADERS'] = 'Content-Type'


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


if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=8000, debug=True)


