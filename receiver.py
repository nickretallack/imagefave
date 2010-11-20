from flask import Flask
app = Flask(__name__)
from urllib import urlopen

@app.route("/<path:data>")
def hello(data):
    output = open("foo.png","wb")
    output.write(urlopen(data).read())
    app.logger.debug("Hit with %s" % data)
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()

