from flask import Flask, request, jsonify
import mainlocal as sparkapp
import json

app = Flask(__name__)


@app.route("/spark-submit",methods=['POST'])
def spark_submit():
    print("Initiating spark job submission")
    result = sparkapp.runtask(request.args.get('retailers'))
    return result

    
if __name__ == "__main__":
    app.run(debug=True)