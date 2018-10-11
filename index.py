from flask import Flask, redirect , url_for, render_template, abort
import json
app = Flask(__name__)
with open('static/clouds.json', 'r') as f:
    clouds = json.load(f)


@app.route('/category/')
@app.route('/category/<name>')
@app.route('/category/<name>/<type>')
def category(name=None, type=None):
    if (name == None):
        return render_template('category.html', alti = "hide", prec = "hide")
    else:
        if(name == 'altitude'):
            if(type == None):
                return render_template('category.html', alti = "show", prec = "hide")
            else:
                return render_template('alt_precip.html', type = name, list = clouds)
        else:
            if(name == 'precipitation'):
                if(type == None):
                    return render_template('category.html', alti = "hide", prec = "show")
                else:
                    return render_template('alt_precip.html', type = name, list = clouds)
            else:
                abort(404)

@app.route('/cloud/')
@app.route('/cloud/<name>')
def cloud(name=None):
    names = []
    for obj in clouds:
        if(name != None):
            if(obj['name'] == name):
                names.append(obj)
            if (len(names) == 0):
                abort(404)
        else:
            names = clouds
    return render_template('clouds.html',name =name, list = names)
@app.route('/')
def root():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find requested page", 404
if __name__=="__main__":
    app.run(host='localhost', debug=True)
