
![Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Flask_logo.svg/640px-Flask_logo.png)



Eti's Travel Blog - A microblog experiment, powered by flask
====


I wrote my own useful backend - a dream comes true!
----

You can get more information about the microframework [here](https://flask.palletsprojects.com/en/1.1.x/). 
There one can find tutorial, documentation and guides how to install and run flask in general.

This blog style demo has basicaly two purposes. First it should teach me how to code and deploy a blog by myself.
Second, a good friend of mine wanted to share his travel pictures with our gang.

Try it on your own, it's super fun:
----

1. Clone the repository to a local directory

2. Install Python 3!
You can find informations on how to do that [here](https://www.python.org/about/gettingstarted/).

3. Check if you have pip installed
    
    ```
    $ pip3 --version
    ```

    otherwise go install it. Look up how to do that [here](https://pypi.org/project/pip/).

4. Create a virtual environment. Lookup details [here](https://docs.python.org/3/library/venv.html) or in a more simple style [here](https://realpython.com/courses/working-python-virtual-environments/).

    ```
    $ python3 -m venv myflaskrvenv
    ```

5. Activate the virtual environment. 
    ```
    $ source myflaskrvenv/bin/activate
    ```
    Or look up how to do that on your particalar os. Once you are in your virtual environment you can deactivate it like so

    ```
    $ deactivate
    ```

6. Go to the flaskr main directory and install the package.

    ```
    $ pip3 install -e .
    ```

I need a database?
----
When you setup the project from scratch you need to initialize a new database.
Lucky us, this is easily done by
```
$ flask init-db
```

Everything is working fine ... localy ... but how do I get this stuff online?
----
There are lot's of plattforms which give you options to deploy your python based app.
I decided to go for [pythonanywhere](https://www.pythonanywhere.com/) to deploy this blog for my pal to use.

1. First things first - create an account for yourself. (Hint: your free domain starts with your username, so take a nice one!).

2. The trick is to setup the .wsgi File in a correct way. You can copy this code and change the directory to the top level of your project directory.
    ```python
    import sys

    # add your project directory to the sys.path
    project_home = '/home/&user&/&microblog-with-flask&/'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path

    # import flask app but need to call it "application" for WSGI to work
    from flaskr import create_app
    application = create_app()
    ```
    This means you have to go one level above the actual .py files.
    

