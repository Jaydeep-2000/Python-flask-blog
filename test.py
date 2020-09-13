from flask import Flask, render_template, request, session, redirect
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from dbconnection import connection
from utility import create_dict
from datetime import datetime
from flask_mail import Mail
import os
import json
import math

with open ("config.json", "r") as f:
    params = json.load(f)["params"]

app = Flask(__name__,template_folder="templates")
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

@app.route("/sample/<string:post_slug>", methods=['GET'])
def posts(post_slug):
    print(post_slug)
    c,conn = connection()
    query = "SELECT * FROM posts where slug = '%s'" %(post_slug,)
    c.execute(query)
    post = c.fetchone()
    print(post)
    # keys = ('sno','title','slug','content','date','img_url','tagline')
    # tup1 = ()
    # tup1 = tup1 + (res,)
    # post = create_dict(keys, tup1)
    return render_template('post.html', post=post, params=params)



# main
if __name__ == "__main__":
    app.run(debug=True)