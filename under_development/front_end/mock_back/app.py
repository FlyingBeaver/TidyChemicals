import json
from pprint import pprint
from datetime import datetime, date, time
from flask import Flask, request, url_for, render_template, redirect
from flask_cors import CORS, cross_origin
from instead_of_db import storages, users_dict, recent
from mol import mol
from rdkit.Chem.rdmolfiles import MolFromMolBlock
from rdkit.Chem.Draw import MolToFile
from uuid import uuid4
from storages_dict import children_of, path_children


storages_dict = dict()
for item in storages:
    id_ = item["id"]
    item2 = dict(item)
    del item2["id"]
    storages_dict[id_] = item2

t = time(11, 45)
d_created = date(2023, 1, 22)
d_updated = date(2023, 1, 23)
datetime_created = datetime.combine(d_created, t)
datetime_updated = datetime.combine(d_updated, t)


app = Flask(__name__)
CORS(app)
delta = {"ops":[{"insert":"tret-Butyldimethylsilyl chloride\n"}]}


def make_dict(structure_pic):
    return {
        "id": 29,
        "name_data": {"html": "<p>tret-Butyldimethylsilyl chloride</p>",
                      "delta": delta},
        "structure_pic": structure_pic,
        "structure_mol": mol,
        "structure_aq": 0,
        "location": "root/Лаборатория 1/Холодильник/Нижняя полка",
        "quantity": {"number": 50, "unit": "g"},
        "hazard_pictograms": ["flammable", "corrosive", "environmental_hazard"],
        "molar_mass": "150,72",
        "cas": "18162-48-6",
        "synonyms": [
                      {
                      "html": "<p>tret-Butyl(chloro)dimethylsilane</p>", 
                      "delta": {"ops":[{"insert":"tret-Butyl(chloro)dimethylsilane\n"}]},
                      },
                      {
                      "html": "<p>tret-Butyldimethychlorosilane</p>",
                      "delta": {"ops":[{"insert":"tret-Butyldimethychlorosilane\n"}]}
                      },
                      {
                      "html": "<p>TBDMSCl</p>",
                      "delta": {"ops":[{"insert":"TBDMSCl\n"}]}
                      },
                     ],
        "comment":  {
                      "html": "<p>Use parafilm to seal the bottle</p>",
                      "delta": {"ops":[{"insert":"Use parafilm to seal the bottle\n"}]}
                      },
        "tags": ["#protecting_groups",
                 "&silyl_chlorides",
                 "Favorites"],
        "created_by": "@johndoe",
        "creation_date": datetime_created,
        "last_change_by": "@janedoe",
        "last_change_date": datetime_updated,
    }


none_where_possible_dict = {
    "id": 29,
    "name_data": {"html": "<p>tret-Butyldimethylsilyl chloride</p>",
                  "delta": delta},
    "structure_pic": None,
    "structure_mol": None,
    "structure_aq": None,
    "location": None,
    "quantity": {"number": 50, "unit": "g"},
    "hazard_pictograms": None,
    "molar_mass": None,
    "cas": None,
    "synonyms": None,
    "comment":  None,
    "tags": None,
    "created_by": "@johndoe",
    "creation_date": datetime_created,
    "last_change_by": "@janedoe",
    "last_change_date": datetime_updated,
}


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/templates/fg.sdf')
def fg_redirect():
    return redirect("/static/templates/fg.sdf", code=302)


@app.route('/templates/library.sdf')
def library_redirect():
    return redirect("/static/templates/library.sdf", code=302)


@app.route('/templates/library.svg')
def library_svg_redirect():
    return redirect("/static/templates/library.svg", code=302)


@app.route("/check/")
def check():
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
    branch_no = 2
    if branch_no == 1:
        return none_where_possible_dict
    elif branch_no == 2:
        return make_dict(url_for("static", filename="TBDMSCl.png"))
    else:
        raise ValueError("Wrong value of branch_no")


@app.route("/units/", methods=["GET"])
def units():
    return ["l", "ml", "g", "kg", "mg"]


@app.route("/tags/", methods=("POST", "GET"))
def tags():
    return {"ampersandtags": ["tag_one", "tagTwo", "Tag_three"],
            "hashtags": ["tag_four", "tagFIVE", "tagSix"]}


@app.route("/convert/", methods=["POST"])
def convert():
    mol_block = request.json["molBlock"]
    structure = MolFromMolBlock(mol_block)
    name = f"/static/{uuid4()}.svg"
    MolToFile(structure, "." + name, imageType="svg")
    return {"link_to_file": name}


@app.route("/root/", methods=("POST", "GET"))
def root():
    return {"name": "root", "type": 0, "id": 0}


@app.route("/children/<id>", methods=("POST", "GET"))
def children(id):
    return children_of(int(id))


@app.route("/path_to_chemical/<id>", methods=("POST", "GET"))
def path_to_chemical(id):
    return path_children(int(id))


if __name__ == '__main__':
    app.run(debug=True)
