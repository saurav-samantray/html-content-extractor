from flask import Flask
import extractorService as service

app = Flask(__name__)


@app.route('/getTags/')
def getTags():
    return service.TagExtractor().extractTag()


if __name__ == "__main__":
    app.run(debug=True)