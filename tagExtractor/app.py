from flask import Flask
import extractorService as service

app = Flask(__name__)


@app.route('/getTags/')
def get_tags():
    return service.TagExtractor().extractTag("")


@app.route('/getTags/<brand>')
def get_tags_for_brand(brand):
    return service.TagExtractor().extractTag(brand)


if __name__ == "__main__":
    app.run(debug=True,port='5001')