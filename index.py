from flask import Flask, redirect , url_for, render_template, abort
import json
app = Flask(__name__)
with open('static/clouds.json', 'r') as f:
    clouds = json.load(f)

@app.route("/private")
def private():
    return redirect(url_for('login'))
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
    return render_template('category.html',name =name, list = names)
@app.route('/login')
def login():
    return "None shall pass"
@app.route('/')
def root():
    return render_template('index.html')
@app.route ('/static/img')
def static_example_img():
    start= '<img src ="'
    url= url_for ('static', filename ='vmask.jpg')
    end= '>'
    return start+url+end, 200
@app.errorhandler(404)
def page_not_found(error):
    return "Couldn't find requested page", 404
if __name__=="__main__":
    app.run(host='localhost', debug=True)
