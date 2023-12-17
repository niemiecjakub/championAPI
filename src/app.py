
import config
from flask import render_template, redirect
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
    return redirect("/api/ui", code=302)



if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=8000, debug=True)


