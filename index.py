from flask import Flask, redirect , url_for, render_template, abort, request
import json
app = Flask(__name__)
with open('static/clouds.json', 'r') as f:
    clouds = json.load(f)
    f.close()
with open('static/community.json', 'r') as co:
    communityList = json.load(co)
    co.close()
@app.route('/category/')
@app.route('/category/<name>')
@app.route('/category/<name>/<type>')
def category(name=None, type=None):
    if (name == None):
        return render_template('category.html',background="clouds3.jpg",title = "Clouds - Categories", alti = "hide", prec = "hide")
    else:
        if(name == 'altitude'):
            if(type == None):
                return render_template('category.html',background="clouds3.jpg",title = "Clouds - Categories", alti = "show", prec = "hide")
            else:
                filteredList = []
                typeLower = type.lower()
                if(typeLower in ("high", "medium", "low")):
                    for obj in clouds:
                        if(typeLower == 'high'):
                            if(obj['altitude-max'] > 8):
                                filteredList.append(obj)
                        else:
                            if (typeLower == 'medium'):
                                if(obj['altitude-max'] == 8):
                                    filteredList.append(obj)
                            else:
                                if (typeLower == 'low'):
                                    if(obj['altitude-min']< 8 ):
                                        filteredList.append(obj)
                    return render_template('clouds.html',background="clouds2.jpg",title = "Clouds", filter = name, type = type , list = filteredList)
                else:
                    abort(404)
        else:
            if(name == 'precipitation'):
                if(type == None):
                    return render_template('category.html',background="clouds3.jpg",title = "Clouds - Categories", alti = "hide", prec = "show")
                else:
                    filteredList = []
                    typeLower = type.lower()
                    if(typeLower in ("none", "rain", "seldom", "snow")):
                        for obj in clouds:
                            if(typeLower == 'none'):
                                if(obj['precipitation'].find('none') != -1):
                                    filteredList.append(obj)
                            else:
                                if (typeLower == 'rain'):
                                    if(obj['precipitation'].find('rain') != -1 or obj['precipitation'].find('seldom') != -1):
                                        filteredList.append(obj)
                                else:
                                    if (typeLower == 'snow'):
                                        if(obj['precipitation'].find('snow') != -1):
                                            filteredList.append(obj)
                        return render_template('clouds.html',background="clouds2.jpg",title = "Clouds", filter = name, type = type , list = filteredList)
                    else:
                        abort(404)
            else:
                abort(404)

@app.route('/cloud/')
@app.route('/cloud/<name>')
def cloud(name=None):
    names = []
    if(name !=None):
        for obj in clouds:
            if(obj['name'].lower() == name.lower()):
                names.append(obj)
        if (len(names) == 0):
            abort(404)
    else:
        names = clouds
    return render_template('clouds.html',background="clouds2.jpg",title = "Clouds",name =name, list = names)
@app.route('/')
def root():
    return render_template('index.html',background="clouds1.jpg",title = "Home")
@app.route('/submission', methods=['GET','POST'])
def submission():
    if (request.method == 'POST'):
        if(request.form.get('upload', None) == "upload"):
            cloud = {
            "name": "Cirrus",
            "form":"hello",
            "description": "something",
            "interpretation": "placeholder",
            "email": "example@web.com",
            "altitude-min": 8,
            "altitude-max": 12,
            "precipitation": "none",
            "image": "https://imgur.com/dXuJ9eT.jpg"}
            cloud['name'] = request.form['cloudInput']
            cloud['email'] = request.form['emailInput']
            cloud['form'] = request.form['formationInput']
            cloud['description'] = request.form['descriptionInput']
            cloud['interpretation'] = request.form['interpretationInput']
            cloud['altitude-min'] = request.form['minInput']
            cloud['altitude-max'] = request.form['maxInput']
            cloud['precipitation'] = request.form['precInput']
            cloud['image'] = request.form['imgInput']
            communityList.append(cloud)
            with open('static/community.json', 'w') as outfile:
                json.dump(communityList, outfile)
                outfile.close()
            return redirect('/')
        else:
            toFind = request.form['searchCloud']
            return redirect('/cloud/%s' %toFind)
    else:
        return render_template('submission.html',background="clouds1.jpg",title = "Cloud Upload")

@app.route('/community')
def community():
    return render_template('clouds.html',background="clouds2.jpg",title = "Community Submissions",name = None, list = communityList)
@app.route('/', methods=['POST'])
@app.route('/cloud/', methods=['POST'])
@app.route('/cloud/<path:wildcard>', methods=['POST'])
@app.route('/category/<path:wildcard>', methods=['POST'])
@app.route('/category/', methods=['POST'])
def search_post(wildcard=None):
    toFind = request.form['searchCloud']
    return redirect('/cloud/%s' %toFind)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404
if __name__=="__main__":
    app.run(host='localhost', debug=True)
