from flask import Flask, redirect , url_for, render_template
import json
app = Flask(__name__)
with open('static/wine.json', 'r') as f:
    reviews = json.load(f)

@app.route("/private")
def private():
    return redirect(url_for('login'))
@app.route('/country/')
@app.route('/country/<name>')
def country(name=None):
    countries = ['countries']
    for obj in reviews:
        if(name != None):
            if(obj['country'] == name):
                countries.append(obj)
        else:
            for x in reviews:
                if x['country'] not in countries:
                    countries.append(x)
    return render_template('category.html',name =name, list = countries)
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
