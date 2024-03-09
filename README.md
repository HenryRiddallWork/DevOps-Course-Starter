# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

For styling tailwindcss is used via their CLI tool. For this to work you must also have Node installed.

### VSCode

It is reccomended to use VSCode for this project as there is an included launch config and linting has so far been enforced using VSCode extensions. The reccomended linting extensions are:

- Better Jinja
- Black Formatter
- Mypy
- Prettier (You will also need the NPM package, installation details described in the style section)

However none of these styles are enforced yet so go wild I guess.

You may also want to install other extensions to make development easier such as Pylance and Tailwind CSS IntelliSense (this extension is especially helpul if you are new to tailwind).

### Styles

- Install the latest version of Node from: https://nodejs.org/en
- Install the dependancies using `npm install`
- To keep the css build updated run the cli tool with the following command (--watch will watch for file changes in the project regenerate the CSS when neccisary):

```
npx tailwindcss -i ./todo_app/tailwind.css -o ./todo_app/static/css/index.css --watch
```

Note: the website will not have any styles if you do not run the above as the generated CSS file is in the .gitignore.

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

You can check poetry is installed by running `poetry --version` from a terminal.

**Please note that after installing poetry you may need to restart VSCode and any terminals you are running before poetry will be recognised.**

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

You must also populate the TRELLO_XXXXX variables with your own API key, token and board Id.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:

```bash
$ poetry run flask run
```

You should see output similar to the following:

```bash
 * Serving Flask app 'todo_app/app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 113-666-066
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
