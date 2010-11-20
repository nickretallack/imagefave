from flask import Flask
app = Flask(__name__)
from urllib import urlopen
from hashlib import sha1 as hasher

import mongorm
from pymongo import Connection
from gridfs import GridFS
from gridfs.errors import FileExists

connection = Connection()
db = mongorm.db = connection.imagefave
fs = GridFS(db)

class User(mongorm.Record):
    _collection='user'
    # schema: id=user_id

class Preference(mongorm.Record):
    _collection='preference'
    # schema: user_id, image_id

#class Image(Record):
#    _collection='image'
#    # schema: id=image_id, extension



@app.route("/fave/<user>/<path:upload_path>")
def fave(user, upload_path):
    upload_data = urlopen(upload_path).read()
    image_id = hasher(upload_data).hexdigest()
    image_extension = upload_path.rsplit('.',1)[1]
    preference_data = {'user_id':user,'image_id':image_id}
    if not Preference.find_one(**preference_data):
        Preference(**preference_data).save()
    
    try:
        # Note: this can stream from a file.  We should do that.
        fs.put(upload_data, _id=image_id)
    except FileExists:
        pass

    #if not Image.find_one({'_id':image_id}):
    #    Image(_id=image_id, extension=image_extension).save()

    #output = open("foo.png","wb")
    #output.write(upload_data)
    #app.logger.debug("Hit with %s" % data)
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()

