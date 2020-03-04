from flask import Flask, render_template, url_for
from flask import make_response, redirect, request, jsonify
app = Flask(__name__)
@app.route('/')
def index():
    title ="my_app"
    return render_template("index.html",title= title)
    
@app.route('/resultats/<path>', methods=['GET'])
def results(path):
    title = 'Result'
    return render_template('layouts/resultats.html',
                           title=title)

@app.route('/postmethod', methods = ['POST'])
def post_javascript_data():
    jsdata = request.form['data']
    params = { 'path' : jsdata}
    return jsonify(params)

if __name__ =="__main__":
    app.run(debug=True)
