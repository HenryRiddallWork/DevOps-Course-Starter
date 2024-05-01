# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

For styling tailwindcss is used via their CLI tool. For this to work you must also have Node installed.

### VSCode

It is recommended to use VSCode for this project as there is an included launch config and linting has so far been enforced using VSCode extensions. The recommended linting extensions are:

- Better Jinja
- Black Formatter
- Mypy
- Prettier (You will also need the NPM package, installation details described in the style section)

However none of these styles are enforced yet so go wild I guess.

You may also want to install other extensions to make development easier such as Pylance and Tailwind CSS IntelliSense (this extension is especially helpul if you are new to tailwind).

### Node installation

Node is required for the development of this app so you will need to install Node and the project dependencies. However, the site is primarily built using Python with Flask, so think very carefully before adding any packages.

- Install the latest version of Node from: https://nodejs.org/en
- Install the dependencies using `npm install`

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
$ npm run dev
```

You should see output similar to the following:

```bash
$> dev
$> concurrently "npm run css" "poetry run flask run"
$[0]
$[0] > css
$[0] > npx tailwindcss -i ./todo_app/tailwind.css -o ./todo_app/static/css/index.css --watch
$[0]
$[1]  * Serving Flask app 'todo_app/app'
$[1]  * Debug mode: on
$[1] WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
$[1]  * Running on http://127.0.0.1:5000
$[1] Press CTRL+C to quit
$[1]  * Restarting with stat
$[0]
$[0] Rebuilding...
$[0]
$[0] Done in 306ms.
$[1]  * Debugger is active!
$[1]  * Debugger PIN: 207-877-058
$[1] 127.0.0.1 - - [05/Apr/2024 16:49:39] "GET / HTTP/1.1" 200 -
$[1] 127.0.0.1 - - [05/Apr/2024 16:49:39] "GET /static/css/custom.css HTTP/1.1" 304 -
$[1] 127.0.0.1 - - [05/Apr/2024 16:49:39] "GET /static/css/index.css HTTP/1.1" 200 -
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing

Unit tests & integration tests are implemented using [pytest](https://docs.pytest.org/). The full suite of tests can be run using:

```bash
$ poetry run pytest
```

or a specific test can be run using:

```bash
$ poetry run pytest path/to/test_file
```

## Docker containers

It is also possible to run the app using Docker containers. There are two containers maintained in the Dockerfile, a production container and a development container. To build the containers you must first have a valid .env file as described in the instructions above. Then you should run the build command:

### Production

```bash
docker build --target production --tag todo-app:prod .
```

### Development

```bash
docker build --target development --tag todo-app:dev .
```

Once that has completed you can run the corresponding run command and the app should become visible on the corresponding port:

### Production

This will not pick up on any code changes and the above build step will need to be run again for them to be noticed.

```bash
docker run -it --env-file ./.env --publish 8000:8000 todo-app:prod
```

### Development

This supports hot reloading and should pick up on code changes you make.

```bash
docker run -it --env-file ./.env --publish 5000:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/code/todo_app" todo-app:dev
```

## Ansible

To provision a VM and start the todo app you must first ensure the necissary files are on the control Node either by pulling the entire git repo or copying them over. The necessary files are:

- playbook.yaml
- inventory.ini
- .env.j2
- todoapp.service

**NOTE: You must update the "Checkout repo" task in the playbook.yaml to match the branch on the control node!**

You can add any managed nodes to the inventory.ini file.
Then, on the control node from the directory these files are in, run the following
command:

```bash
$ ansible-playbook playbook.yaml -i inventory.ini
```

You will then be prompted for some secret details required for the app to run. After you have entered these details you should see an output similar to the following (though likely with all tasks displaying "Changed" rather than "ok"):

```bash
PLAY [Install ToDo App on new web servers] **************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************************************************************************************************************************************************
[WARNING]: Platform linux on host 13.43.77.114 is using the discovered Python interpreter at /usr/bin/python3.9, but future installation of another Python interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-
core/2.15/reference_appendices/interpreter_discovery.html for more information.
ok: [13.43.77.114]

TASK [Install git] **************************************************************************************************************************************************************************************************************************************************************************************
ok: [13.43.77.114]

.....
.....
.....

PLAY RECAP **********************************************************************************************************************************************************************************************************************************************************************************************
13.43.77.114               : ok=13   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

You should now (or at least within a few seconds) be able to access the app from the IPs within the inventory.ini file on port 8000.
