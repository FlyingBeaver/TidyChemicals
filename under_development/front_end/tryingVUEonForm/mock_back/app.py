import json
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


app = Flask(__name__)
CORS(app)
delta = {"ops":[{"insert":"tret-Butyldimethylsilyl chloride\n"}]}


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
    return {"id": 29,
            "name_code": "<p>tret-Butyldimethylsilyl chloride</p>",
            "name_delta": delta,
            "structure_pic": url_for("static", filename="TBDMSCl.png"),
            "structure_mol": mol,
            "structure_aq": 0,
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
