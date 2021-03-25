import os
import random
import imghdr
import time
import fnmatch

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_from_directory, abort
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db, query_db

from PIL import Image

bp = Blueprint('blog', __name__)

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def resize_image(uploaded_file, baseheight):
    img = Image.open(uploaded_file)
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    return img

def store_image(uploaded_file, hashval):
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400) 
        img = resize_image(uploaded_file, 560)        
        img.save(os.path.join(current_app.root_path, current_app.config['UPLOAD_PATH'], str(hashval) + '_' + filename))

def delete_images(id):
    post = query_db('select * from post where id = ?', [id], one=True)
    hashval = post['hashval']

    for image in os.listdir(current_app.config['UPLOAD_PATH']):

        if hashval in image:
            os.remove(os.path.join(current_app.config['UPLOAD_PATH'], image))

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, hashval'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    return render_template('blog/index.html', posts=posts, files=files)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        uploaded_files = request.files.getlist('files[]')
        hashval = hash(time.time())
        if hashval < 1:
            hashval = hashval * -1
        
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, hashval)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], hashval)
            )
            db.commit()

            for uploaded_file in uploaded_files:
                store_image(uploaded_file, hashval)

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, hashval'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()

    delete_images(id)

    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('blog.index'))

@bp.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)