from flask import Flask, request, jsonify
import main as sparkapp
import json
import config

app = Flask(__name__)


@app.route("/spark-submit",methods=['POST'])
def spark_submit():   
    mode = request.args.get('mode')
    retailer = request.args.get('retailers')
    result = {}
    if config.MASTER_NODE_MAP.get(mode) is None:
    	return {'success':False,'error':f'{mode} is not a valid input for mode'}
    else:
    	print(f"Initiating spark job in {mode} mode")
    	master = config.MASTER_NODE_MAP[mode]
    	result = sparkapp.runtask(retailer,master)
    
    return result

    
if __name__ == "__main__":
    app.run(debug=True)