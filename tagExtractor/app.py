from flask import Flask
import extractorService as service
from flask import jsonify

app = Flask(__name__)


@app.route('/getTags/')
def get_tags():
    return jsonify(service.TagExtractor().extractTag(""))


@app.route('/getTags/<brand>')
def get_tags_for_brand(brand):
    return jsonify(service.TagExtractor().extractTag(brand))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')