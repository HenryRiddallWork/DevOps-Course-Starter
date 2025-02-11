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

## Dependencies

You will need to clone a new `.env` file from the `.env.j2` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.j2 .env  # (first time only)
```

The `.env` file is used to set various environment variables.

You should populate all of the variables surrounded by handlebars e.g. `{{ example_variable }}` with the appropriate values, many of these can be found either in the GitHub project or the production app service on Azure.

## Docker containers

We use docker containers for both development and testing of this app, this means you shouldn't need to install the relevant Node/Python packages but, while it wont be covered in this document, that should be possible to achieve.

#### Production

The production container uses Gunicorn as the WSGI server providing a production ready experience, in general this should not be needed for local development. You can start this container with:

```bash
docker compose up prod
```

Once the container is built and completes startup the application should be available on port 8080.

#### Development

The development container uses flasks built in WSGI which shouldn't be used in production but combined with the bind-mount on the `./todo_app` directory allows hot reloading to pick up code changes immediately. This container can be started using:

```bash
docker compose up dev
```

Once the container is built and completes startup the application should be available on port 5000 and any changes to the code should be visible on refresh (This does not apply to package changes which require the container to be rebuilt however those should be extremely uncommon).

#### Test

The test container will automatically run all the unit/integration tests

```bash
docker compose up test
```

Once the container is built it will run the tests and display the results in the console.

NOTE: The pull policy on all services are set to build. This acts like adding the --build option to the compose command and as such the image is rebuilt every time. At the moment this isn't very costly as the containers are quite small, but this decision may be worth revisiting in future if more complexity is added!

## CI/CD

The CI/CD of this app is handled using GitHub actions currently, as there is only one developer and no live users, every push will result in a full deployment to the Azure App Service. The flow of this pipeline is as follows:

1. Build a new Docker Image using the updated code
2. Run the unit/integration tests
3. If the tests pass, re-build the Docker image and push it to Docker Hub
4. Run Terraform Apply which will create, update or destroy resources based on the Terraform plan
5. Call the Azure webhook, which triggers the App Service to restart using the latest version of the Docker Image from the registry

The Terraform plan is set up to allow a prefix for the resources and thus it should be possible to create multiple environments in future. For example it may make sense to use the current branch as a prefix so that each branch has a separate deployment.

## Security

### Encryption at rest

We are using Azure Cosmos DB and therefore all data is encrypted using AES-256 encryption as this is the default for that service.

## Kubernetes

It is possible to run the application locally using a Minikube kubernetes cluster. Make sure you have installed the following before beggining: [Docker](https://docs.docker.com/desktop/setup/install/windows-install/), [Kubectl](https://kubernetes.io/docs/tasks/tools/) and [minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download). Once you have installed these complete the following steps:

- Start minikube by running: `minikube start`
- Build the docker image by running: `docker build --target production --tag todo-app:prod .`
- Create the environment secret by running the following command, making sure to replace the secret values (the ones inside double curly braces) with your real secrets:

```bash
kubectl create secret generic environment-secret --from-literal=FLASK_APP='todo_app/app' --from-literal=SECRET_KEY='{{ SECRET_KEY }}' --from-literal=PREFERRED_URL_SCHEME='https' --from-literal=MONGO_CONNECTION_STRING='{{ MONGO_CONNECTION_STRING }}' --from-literal=MONGO_DB_NAME='todo_db' --from-literal=MONGO_DB_COLLECTION='todo_items' --from-literal=OAUTH_CLIENT_ID='{{ OAUTH_CLIENT_ID }}' --from-literal=OAUTH_CLIENT_SECRET='{{ OAUTH_CLIENT_SECRET }}' --from-literal=OAUTHLIB_INSECURE_TRANSPORT='1' --from-literal=LOG_LEVEL='DEBUG' --from-literal=LOGGLY_TOKEN='{{ LOGGLY_TOKEN }}'
```

- Then to deploy the pod run: `kubectl apply -f deployment.yaml` AND `kubectl apply -f service.yaml`
- Finally to link the minikube service up with a port on localhost run: `kubectl port-forward service/module-14 7080:8080`
- You should now be able to access the app at: http://localhost:7080/
