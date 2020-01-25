from flask import Flask, request, jsonify
import main as sparkapp
import json
import config

app = Flask(__name__)


@app.route("/spark-submit",methods=['POST'])
def spark_submit():   
    mode = request.args.get('mode')
    retailers = request.args.get('retailers')

    #override with request body if present
    if request.data:
        jsondata =  json.loads(request.data)
        retailers = jsondata['retailers']
        mode = jsondata['mode']
    result = {}
    if config.MASTER_NODE_MAP.get(mode) is None:
    	return {'success':False,'error':f'{mode} is not a valid input for mode'}
    else:
        app.logger.info(f'Initiating spark job in {mode} mode')
        master = config.MASTER_NODE_MAP[mode]
        result = sparkapp.runtask(retailers,master)
    
    return result

    
if __name__ == "__main__":
    app.run(debug=True)