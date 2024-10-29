# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## Deployment

There is a live deployment of this site being hosted on Microsoft Azure which can be found [here](https://todo-web-app-henry-riddall.azurewebsites.net/). This uses a docker image hosted on docker hub [here](https://hub.docker.com/r/henryriddall1/azure_production_build/tags).

### Manual Deployment Process

Before you begin you will need to have installed the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

- Push the latest version of the docker image to docker hub by running:

```bash
docker login
docker build --target production --tag {{YOUR_USERNAME}}/azure_production_build:prod .
docker push {{YOUR_USERNAME}}/azure_production_build:prod
```

- If an app service does not yet exist you will need to create one by running:

```bash
az appservice plan create --resource-group {{YOUR_RESCOURCE_GROUP}} -n {{APPROPRIATE_SERVICE_NAME}} --sku B1 --is-linux
```

- Then you can create the webapp itself by running:

```bash
az webapp create --resource-group {{YOUR_RESCOURCE_GROUP}} --plan {{APPROPRIATE_SERVICE_NAME}} --name {{APPROPRIATE_APP_NAME}} --deployment-container-image-name docker.io/{{YOUR_USERNAME}}/azure_production_build:prod
```

### Updating a deployment

If you have alrady deployed the webapp you can update the deployment by pushing an updated docker build (see step 1 from above), then running:

```bash
curl -v -X POST '{{WEBHOOK}}'
```

in a bash terminal where {{WEBHOOK}} is found in the Deployment Center tab on your app service's page in Azure Portal.

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

You'll also need to clone a new `.env` file from the `.env.j2` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.j2 .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

You must also populate the MONGO_XXXXX variables with your Mongo account connection string, database and collection names.

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

It is also possible to run the app using Docker containers. There are two containers maintained in the Dockerfile, a production container and a development container. Both of which have corresponding services in the docker-compose.yml file making starting these containers easier for developers.

#### Production

The production container uses Gunicorn as the WSGI server providing a production ready experience. You can start this container with:

```bash
docker compose up prod
```

Once the container is built and completes startup the application should be available on port 8080.

#### Development

The development container uses flasks built in WSGI which shouldn't be used in production but combined with the bind-mount on the `./todo_app` directory allows hot reloading to pick up code changes immediately. This container can be started using:

```bash
docker compose up dev
```

Once the container is built and completes startup the application should be available on port 5000 and any changes to the code should be visible on refresh (This does not apply to package changes which require the container to be rebuilt).

#### Test

The test container will automatically run all the unit/integration tests

```bash
docker compose up test
```

Once the container is built it will run the tests and display the results in the console.

NOTE: The pull policy on all services are set to build. This acts like adding the --build option to the compose command and as such the image is rebuilt every time. At the moment this isn't very costly as the containers are quite small, but this decision may be worth revisiting in future if more complexity is added!

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

You should now (or at least within a few seconds) be able to access the app from the IPs within the inventory.ini file on port 8080.

## Security

### Encryption at rest

We are using Azure Cosmos DB and therefore all data is encrypted using AES-256 encryption as this is the default for that service.
