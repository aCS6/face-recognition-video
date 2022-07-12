from flask import Flask

app = Flask(__name__)

@app.route("/home/<file_name>")
def hello_world(file_name):
    
    from recognise import Recognise
    name = Recognise(file_name)
    headers = {'Access-Control-Allow-Origin': '*'}

    return name,headers

if __name__=="__main__":
    app.run(host="localhost", port=7500, debug=True)
