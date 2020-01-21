from flask import Flask, request, jsonify
import mainlocal as sparkapp
import json

app = Flask(__name__)


@app.route("/spark-submit",methods=['POST'])
def spark_submit():
    print("Submitting spark job")
    retailers = None
    sourcepath = None
    if request.data:
    	jsondata =  json.loads(request.data)
    	retailers = jsondata['retailers']
    	sourcepath = jsondata['sourcepath']
    else:
    	print("Empty request body, using default values configured")
    result = sparkapp.runtask(retailers,sourcepath)
    return result

    
if __name__ == "__main__":
    app.run(debug=True)