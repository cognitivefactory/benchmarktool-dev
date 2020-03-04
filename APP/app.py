from flask import Flask, render_template, url_for
from flask import make_response, redirect, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    title ="my_app"
    return render_template("index.html",title= title)
    
@app.route('/analyse', methods=['GET','POST'])
def analyse():
    title = 'Result'
    data = request.files['file']
    res=data.read()
    res = res.decode("utf-8") 
    return render_template('/results.html',
                           title=title, res=res)


if __name__ =="__main__":
    app.run(debug=True)
