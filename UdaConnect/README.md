# UdaConnect

## Overview
### Introduction
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

### The Task
We work for a company that is building an app that uses location data from mobile devices. Our company has built a Proof of concept (POC) application to ingest location data named UdaConnect. This POC was built with the core functionality of ingesting location and identifying individuals who have shared close geographic proximity.

Management loved the POC, so now that there is buy-in, we want to enhance this application. We have been tasked to enhance the POC application into a Minimum Viable Product (MVP) to handle the large volume of location data that will be ingested.

To do so, we will refactor this application into a microservice architecture using message passing techniques that you have learned in this course.

# Technologies
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API webserver
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [PostgreSQL](https://www.postgresql.org/) - Relational database
- [PostGIS](https://postgis.net/) - Spatial plug-in for PostgreSQL enabling geographic queries]
- [Vagrant](https://www.vagrantup.com/) - Tool for managing virtual deployed environments
- [VirtualBox](https://www.virtualbox.org/) - Hypervisor allowing you to run multiple operating systems
- [K3s](https://k3s.io/) - Lightweight distribution of K8s to easily develop against a local cluster

# Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

# Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)
4. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) with at least version 6.0
5. [Install Vagrant](https://www.vagrantup.com/docs/installation) with at least version 2.0

# Starter Code
We can get started by forking, cloning, or downloading the [starter code](https://github.com/udacity/nd064-c2-message-passing-projects-starter)

# Environment and Tools
### 1.Setup The Environment
Install the tools mentioned in Prerequisities section to get our environment set up properly.

### 2.Initialize K3s
To run the application, we will need a K8s cluster running locally and to interface with it via `kubectl`. We will be using Vagrant with VirtualBox to run K3s.

In this project's root, run `vagrant up`. 
```bash
$ vagrant up
```
The command will take a while and will leverage VirtualBox to load an [openSUSE](https://www.opensuse.org/) OS and automatically install [K3s](https://k3s.io/). When we are taking a break from development, we can run `vagrant suspend` to conserve some ouf our system's resources and `vagrant resume` when we want to bring our resources back up. Some useful vagrant commands can be found in [this cheatsheet](https://gist.github.com/wpscholar/a49594e2e2b918f4d0c4).

### 3.Retrieve the Kubernetes config File
After `vagrant up` is done, we will SSH into the Vagrant environment and retrieve the Kubernetes config file used by `kubectl`. We want to copy the contents of this file into our local environment so that `kubectl` knows how to communicate with the K3s cluster.
```bash
$ vagrant ssh
```
We will now be connected inside of the virtual OS. Run `sudo cat /etc/rancher/k3s/k3s.yaml` to print out the contents of the file. We should see output similar to the one that shown below. Note that the output below is just for our reference: every configuration is unique and you should _NOT_ copy the output we have below.

Copy the contents from the output issued from our own command into our clipboard -- we will be pasting it somewhere soon!
```bash
$ sudo cat /etc/rancher/k3s/k3s.yaml

apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUJWekNCL3FBREFnRUNBZ0VBTUFvR0NDcUdTTTQ5QkFNQ01DTXhJVEFmQmdOVkJBTU1HR3N6Y3kxelpYSjIKWlhJdFkyRkFNVFU1T1RrNE9EYzFNekFlRncweU1EQTVNVE13T1RFNU1UTmFGdzB6TURBNU1URXdPVEU1TVROYQpNQ014SVRBZkJnTlZCQU1NR0dzemN5MXpaWEoyWlhJdFkyRkFNVFU1T1RrNE9EYzFNekJaTUJNR0J5cUdTTTQ5CkFnRUdDQ3FHU000OUF3RUhBMElBQk9rc2IvV1FEVVVXczJacUlJWlF4alN2MHFseE9rZXdvRWdBMGtSN2gzZHEKUzFhRjN3L3pnZ0FNNEZNOU1jbFBSMW1sNXZINUVsZUFOV0VTQWRZUnhJeWpJekFoTUE0R0ExVWREd0VCL3dRRQpBd0lDcERBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUFvR0NDcUdTTTQ5QkFNQ0EwZ0FNRVVDSVFERjczbWZ4YXBwCmZNS2RnMTF1dCswd3BXcWQvMk5pWE9HL0RvZUo0SnpOYlFJZ1JPcnlvRXMrMnFKUkZ5WC8xQmIydnoyZXpwOHkKZ1dKMkxNYUxrMGJzNXcwPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    password: 485084ed2cc05d84494d5893160836c9
    username: admin
```
Type `exit` to exit the virtual OS and we will find ourself back in our computer's session. Create the file (or replace if it already exists) `~/.kube/config` and paste the contents of the `k3s.yaml` output [here](https://community.suse.com/posts/scheduled/cluster-this-is-your-admin-do-you-read).

Afterwards, we can test that `kubectl` works by running a command like `kubectl describe services`. It should not return any errors.

### 4.Configure kubectl
Create the file `~/.kube/config` (or replace it if it already exists).

Paste the contents of the k3s.yaml output into the config file.

Test that kubectl works by running the command
```
kubectl describe services
```
It should not return any errors.

### 5.Deploy kubectl
1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
4. `kubectl apply -f deployment/udaconnect-api.yaml` - Set up the service and deployment for the API
5. `kubectl apply -f deployment/udaconnect-app.yaml` - Set up the service and deployment for the web app
6. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)

Manually applying each of the individual `yaml` files is cumbersome but going through each step provides some context on the content of the starter project. In practice, we would have reduced the number of steps by running the command against a directory to apply of the contents: `kubectl apply -f deployment/`.

### 6. Seed the Database 
The first time we run this project, we need to seed the database with dummy data. Use the command `sh scripts/run_db_command.sh <POD_NAME>` against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`). Subsequent runs of `kubectl apply` for making changes to deployments or services shouldn't require you to seed the database again!

### 7. Verify Your Deployment
Once the project is up and running, we should be able to see 3 deployments and 3 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return `udaconnect-app`, `udaconnect-api`, and `postgres`

These pages should also load on your web browser:
* `http://localhost:30001/` - OpenAPI Documentation
* `http://localhost:30001/api/` - Base path for API
* `http://localhost:30000/` - Frontend ReactJS Application

# Project Steps

## Step 1: Review and Plan
- Review the [project](https://github.com/udacity/nd064-c2-message-passing-projects-starter)
- Determine which message passing strategies would integrate well when refactoring to a microservice architecture.

## Step 2: Design and Document
- Using the design decisions from the Step 1, create an architecture diagram of our microservice architecture showing the services and message passing techniques between them.
- Continue to use Kubernetes and maintain the core functionality of the starter project.
- We have to include at least three message passing strategies into our microservice architecture implementing Kafka, gRPC, and either enhancing or creating a RESTful API endpoint.

The Architecture diagram can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/docs/architecture_design.PNG)

![architecture_design](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/docs/architecture_design.PNG)

## Step 3: Justify our Decisions
- Write a 2-3 sentence rationale for each message passing strategy to justify our decision. 

The Architecture decision can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/docs/architecture_decisions.txt) and 
the gRPC doc can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/docs/grpc.txt)

## Step 4: Refactor into Microservices
- Refactor the starter code into a microservice architecture.
- While microservices can be technology-agnostic, we want to make sure that we use tools that our company is comfortable with. Therefore, this project should be done in Python.

### 4.1: New Services
- New services can be created inside of the `modules/` subfolder. We can choose to write something new with Flask, copy and rework the `modules/api` service into something new, or just create a very simple Python application.

As a reminder, each module should have:
1. `Dockerfile`
2. Its own corresponding DockerHub repository
3. `requirements.txt` for `pip` packages
4. `__init__.py`

### 4.2: Docker Images
- `udaconnect-app` and `udaconnect-api` use docker images from `isjustintime/udaconnect-app` and `isjustintime/udaconnect-api`. 
- To make changes to the application, we need to build our own Docker image and push it to our own DockerHub repository. Replace the existing container registry path with our own.

### 4.3: Configs and Secrets
- In `deployment/db-secret.yaml`, the secret variable is `d293aW1zb3NlY3VyZQ==`. The value is simply encoded and not encrypted -- this is ***not*** secure! Anyone can decode it to see what it is.
```bash
# Decodes the value into plaintext
echo "d293aW1zb3NlY3VyZQ==" | base64 -d

# Encodes the value to base64 encoding. K8s expects your secrets passed in with base64
echo "hotdogsfordinner" | base64
```
This is okay for development against an exclusively local environment and we want to keep the setup simple so that you can focus on the project tasks. However, in practice we should not commit our code with secret values into our repository. A CI/CD pipeline can help prevent that.

### 4.4: PostgreSQL Database
- The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_We may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from us. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.

### 4.5: Database Connection
- While the Kubernetes service for `postgres` is running (we can use `kubectl get services` to check), you can expose the service to connect locally:
```bash
kubectl port-forward svc/postgres 5432:5432
```
This will enable us to connect to the database at `localhost`. we should then be able to connect to `postgresql://localhost:5432/geoconnections`. This is assuming we use the built-in values in the deployment config map.

### 4.6: Software
To manually connect to the database, we will need software compatible with PostgreSQL.
* CLI users will find [psql](http://postgresguide.com/utilities/psql.html) to be the industry standard.
* GUI users will find [pgAdmin](https://www.pgadmin.org/) to be a popular open-source solution.

The microservices for Conenction,Person and Location can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/UdaConnect/modules)

# Step 5: Implement Message Passing Technique 
- Implementing gRPC with Python involves two libraries:
    - grpcio to run client and server code
    - grpcio-tools to generate definition code.
 
![gRPC](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/Images/gRPC.PNG)

### 5.1: Creating a gRPC Client and Server
- Define a protobuf request messages, response messages, and service in a .proto file.
- Use grpcio-tools command on the .proto file to generate a pair of Python files representing the messages and the services.
- Import the pair of Python files into our application logic and implement our client/server.

The Protobuf file can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/modules/grpc/orders.proto)

Remember: orders.proto is used only to generate the Python files.

###  5.2: Generate gRPC Files
Using grpcio-tools, generate a pair of files that can be directly imported into ur Python code:
```
grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ orders.proto
```
The path ./, can be replaced with another path or an absolute path to our .proto file.

The files orders_pb2.py and orders_pb2_grpc.py should have been generated.

The generated files can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/UdaConnect/modules/grpc)

### 5.3: Import gRPC Files
Import the files to your application to use class definitions.
```
import orders_pb2
import orders_pb2_grpc
```
Creating a message with data would look like the following:
```
item = orders_pb2.ItemMessage(
               name="xxx",
               brand_name="yyy",
               id=34,
               weight=1.2
           )
```

### Tips
1. Install `grpc-io` with `pip install grpcio-tools`
2. Verify installation with `pip list`
3. Run the `grpc-io` command in the same directory as orders.proto. 
4. orders_pb2.py and orders_pb2_grpc.py should have been created
5. Install grpcio with `pip install grpcio`. This may have already been installed when grpcio-tools was installed
6. orders_pb2_grpc.py and orders_pb2.py should not be edited. The files even have lines that explicitly state DO NOT EDIT!.

### 5.4: gRPC Server
- gRPC server logic is implemented in `main.py`
- grpc is imported to use gRPC in Python code
- orders_pb2 and orders_pb2_grpc is imported to handle the ItemMessage and ItemService that was defined in the .proto file
- ItemServicer is the implementation of the ItemService protobuf stub
- Create in ItemServicer defines our custom logic. It is set up in a simple manner where a Python dictionary is printed and returned as an orders_pb2.ItemMessage object instead of an unstructured dict
- The file handles a lot of boilerplate for setting up a gRPC server since we aren't using a framework like Flask that can reduce boilerplate

The main.py file can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/modules/grpc/main.py)

### 5.5: Running the gRPC Server
```
python main.py 
```
will serve the gRPC server on localhost:5005 import gprc to use gRPC

### 5.6: Create gRPC Client
- gRPC client logic is implemented in `writer.py`
- grpc is imported to use gRPC in Python code
- orders_pb2 and orders_pb2_grpc is imported to handle the ItemMessage and ItemService that was defined in the .proto file. These files don't need to be regenerated.
- Client is configured to send messages to localhost:5005 where the gRPC server is running.
- orders_pb2.ItemMessage object is created with expected fields and values.

The writer.py can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/modules/grpc/writer.py)

### 5.7: Running the gRPC Client
```
python writer.py 
```
- The above command will run the gRPC client
- Changing tabs to where the gRPC server is running, it prints the payload that was passed by the gRPC client.

Note: 
As a reminder, each module should have:
1. `Dockerfile`
2. Its own corresponding DockerHub repository
3. `requirements.txt` for `pip` packages

# Step 6: Implement Kafka Broker
### Kafka Use Cases
- Kafka is a special type of message queue that is often used to handle large volumes of data generated continuously as events.
- Some examples include application logs and user activity — things that represent that "something has happened."

### Architecture Overview
- Kafka is a distributed system, which means that it is an application that is powered by multiple nodes.
- When a producer writes data to Kafka, it stores the data inside of topics.

![Kafka](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/Images/Kafka.PNG)

### Topics
- Topics are abstractions of Kafka where messages can be stored and referenced.
- Internally, topics are distributed as partitions in different nodes and allow parallelized operations.


