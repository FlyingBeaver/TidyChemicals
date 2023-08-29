import json
from flask import Flask, request
from flask_cors import CORS
from instead_of_db import storages, users_dict, recent
from mol import mol


storages_dict = dict()
for item in storages:
    id_ = item["id"]
    item2 = dict(item)
    del item2["id"]
    storages_dict[id_] = item2


app = Flask(__name__)
CORS(app)
delta = {"ops":[{"insert":"tret-Butyldimethylsilyl chloride\n"}]}


@app.route("/check/")
def index():
    return """<form action="http://127.0.0.1:5000/" method="POST">
        <p>Children of:</p>
        <input type="text" name="give_children_of">
        <input type="submit">
    </form>
    <br>
    <form action="http://127.0.0.1:5000/" method="POST">
        <p>Give root:</p>
        <input type="hidden" name="give_root" value="">
        <input type="submit">
    </form>
    """


@app.route("/", methods=["POST"])
def new_search():
    if request.method == "POST":
        if "give_root" in request.form:
            print("root is")
            print(storages[0])
            root = storages[0]
            return {root["id"]: [root["name"], root["terminal"]]}
        elif "give_children_of" in request.form:
            parent_id = int(request.form["give_children_of"])
            if parent_id in storages_dict:
                parent = storages_dict[parent_id]
            else:
                return {}
            if parent["terminal"]:
                return {}
            else:
                children = dict()
                for key in storages_dict:
                    if parent_id == storages_dict[key]["parent"]:
                        children[key] = [storages_dict[key]["name"],
                                         storages_dict[key]["terminal"]]
                return children


@app.route("/show_request/", methods=("POST", "GET"))
def show_request():
    return json.dumps(request.form, sort_keys=True, indent=4)


@app.route("/users/", methods=("POST", "GET"))
def users():
    return {"users": users_dict, "recent": recent}
    # Будет возвращать словарь формата {id_юзера: имя_юзера}


@app.route("/chemical/", methods=("POST", "GET"))
def chemical_data():
    return {"name_code": "<p>tret-Butyldimethylsilyl chloride</p>",
            "name_delta": delta,
            "structure_pic": "TBDMSCl.png",
            "structure_mol": mol,
            "location": "root/Лаборатория 1/Холодильник/Нижняя полка",
            "quantity": "50 g",
            "hazard_pictograms": ["flammable", "corrosive", "environmental_hazard"],
            "molar_mass": "150,72",
            "cas": "18162-48-6",
            "synonyms": ("tret-Butyl(chloro)dimethylsilane, "
                         "tret-Butyldimethychlorosilane, TBDMSCl"),
            "comments": "Use parafilm to seal the bottle",
            "tags": ["#protecting_groups",
                     "&silyl_chlorides",
                     "Favorites"],
            "created_by": "@johndoe",
            "creation_date": "22.01.2023",
            "last_change_by": "@janedoe",
            "last_change_date": "23.01.2023"
            }


if __name__ == '__main__':
    app.run(debug=True)
