from flask import Flask, render_template, request, session, redirect
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from dbconnection import connection
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



		

# home page
@app.route("/")
def home():
    c,conn = connection()
    query = "SELECT * FROM posts"
    c.execute(query)
    post = c.fetchall()
    print(type(post))
    print(post)

    last = math.ceil(len(post)/int(params['no_of_posts']))
    print(last)
    #[0: params['no_of_posts']]
    #posts = posts[]
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page= int(page)
    post = post[(page-1)*int(params['no_of_posts']): (page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    #Pagination Logic
    #First
    if (page==1):
        prev = "#"
        next = "/?page="+ str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template("index.html", params=params, post=post, prev=prev, next=next)




# admin pannel
@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    c,conn = connection()

    if ('user' in session and session['user']==params['admin_user']):
        query = "SELECT * FROM posts"
        c.execute(query)
        post = c.fetchall()
        print(post)
        print(type(post))

        return render_template('admin_pannel.html', params=params, post=post)

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        if (username==params['admin_user'] and password==params['admin_password']):
            #set session variable
            session['user']= username
            query = "SELECT * FROM posts"
            c.execute(query)
            post = c.fetchall()
            print(post)
            print(type(post))
           
            return render_template('admin_pannel.html', post=post, params=params)

    
    return render_template('login.html', params=params)




# contact
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        c,conn = connection()
        query = "INSERT INTO contacts (name, email, phone_num, msg) VALUES ('%s','%s','%s','%s')" % (name, email, phone, message)
        try:
            c.execute(query)
            conn.commit()

        except:
            conn.rollback()

    return render_template('contact.html', params=params)




# sample post
@app.route("/sample/<string:post_slug>", methods=['GET'])
def posts(post_slug):
    print(post_slug)
    c,conn = connection()
    query = "SELECT * FROM posts where slug = '%s'" %(post_slug,)
    c.execute(query)
    post = c.fetchone()
    print(post)
    print(type(post))

    return render_template('post.html', post=post, params=params)

      

# about
@app.route("/about")
def about():
     return render_template('about.html', params=params)




# editing posts
@app.route("/edit/<string:Sno>", methods=['GET','POST'])
def edit(Sno):
    if ('user' in session and session['user']==params['admin_user']):
        c,conn = connection()
        if request.method == 'POST':
            '''Add entry to the database'''
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_url = request.form.get('img_url')
            tagline = request.form.get('tline')

              
            query = "UPDATE posts SET title = '%s', slug = '%s', content = '%s', img_url = '%s', tagline = '%s' WHERE (sno = '%s');" %(title, slug, content, img_url, tagline, Sno)
            c.execute(query)
            conn.commit()
            return redirect('/dashboard')

        query = "SELECT * FROM posts where sno = '%s'" %(Sno,)
        print(query)
        c.execute(query)
        post = c.fetchone()
    
        return render_template('edit.html', params=params, post=post, Sno=Sno)




@app.route("/add", methods=['GET','POST'])
def add():
    if ('user' in session and session['user']==params['admin_user']):
        c,conn = connection()
        if request.method == 'POST':
            '''Add entry to the database'''
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img_url = request.form.get('img_url')
            tagline = request.form.get('tline')

            query = "INSERT INTO posts (title, slug, content, img_url, tagline) VALUES ('%s','%s','%s','%s', '%s')" %(title, slug, content, img_url, tagline)
            print(query)
            c.execute(query)
            conn.commit()
            return redirect('/dashboard')
           
        return render_template('add.html', params=params)



# file uploader
@app.route("/uploader", methods=['GET','POST'])
def upload_file():
    if ('user' in session and session['user']==params['admin_user']):
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Succefully"




# to logout the user
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


# DELETE A POST
@app.route("/delete/<string:Sno>", methods=['GET','POST'])
def delete(Sno):
    if ('user' in session and session['user']==params['admin_user']):
        c,conn = connection()
        query = "DELETE FROM posts where sno = '%s'" %(Sno,)
        print(query)
        c.execute(query)
        conn.commit()
        return redirect('/dashboard')

# main
if __name__ == "__main__":
    app.run(debug=True)


