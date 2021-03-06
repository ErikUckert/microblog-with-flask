import os
from os.path import join, dirname, realpath

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='\xd9\xdb0A\x04\xcc\xc6UJ\x1f\xa3st\xa1\x88"\xc3\xf4i\x86v\xd1y\xe1',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        MAX_CONTENT_LENGTH = 128 * 1024 * 1024,
        UPLOAD_EXTENSIONS = ['.jpg', '.png'],
        UPLOAD_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
    