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

### Tips
* We can access a running Docker container using `kubectl exec -it <pod_id> sh`. From there, we can `curl` an endpoint to debug network issues.
* The starter project uses Python Flask. Flask doesn't work well with `asyncio` out-of-the-box. Consider using `multiprocessing` to create threads for asynchronous behavior in a standard Flask application.

# Project Steps

## Step 1: Review and Plan
- Review the [project](https://github.com/udacity/nd064-c2-message-passing-projects-starter)
- Determine which message passing strategies would integrate well when refactoring to a microservice architecture.

## Step 2: Design and Document
- Using the design decisions from the Step 1, create an architecture diagram of our microservice architecture showing the services and message passing techniques between them.
- Continue to use Kubernetes and maintain the core functionality of the starter project.
- We have to include at least three message passing strategies into our microservice architecture implementing Kafka, gRPC, and either enhancing or creating a RESTful API endpoint.

### 2.1 Architecture Diagrams
Our architecture diagram should focus on the services and how they talk to one another. For our project, we want the diagram in a `.png` format. Some popular free software and tools to create architecture diagrams:
1. [Lucidchart](https://www.lucidchart.com/pages/)
2. [Google Docs](docs.google.com) Drawings (In a Google Doc, _Insert_ - _Drawing_ - _+ New_)
3. [Diagrams.net](https://app.diagrams.net/)

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
### 6.1: Kafka Use Cases
- Kafka is a special type of message queue that is often used to handle large volumes of data generated continuously as events.
- Some examples include application logs and user activity — things that represent that "something has happened."

### 6.1.1: Architecture Overview
- Kafka is a distributed system, which means that it is an application that is powered by multiple nodes.
- When a producer writes data to Kafka, it stores the data inside of topics.

![Kafka](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/Images/Kafka.PNG)

### 6.1.2: Topics
- Topics are abstractions of Kafka where messages can be stored and referenced.
- Internally, topics are distributed as partitions in different nodes and allow parallelized operations.
- Data in Kafka is organized into topics. Internally, topics are partitioned in different servers.

### 6.2: Kafka Set up
- First, the [kafka.yaml](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/deployment/Kafka.yaml) manifests needs to be applied to the cluster
```
kubectl apply -f kafka.yaml
```
- This would bring up two pods, it can take 5-10 minutes, during that time pods may be in "ImagePullBackOff" or "PodInitializing" state several times.
- It is useful to use the "kubectl wait" to wait until the kafka pod is ready
```
kubectl wait pod --timeout 300s --for=condition=Ready \
       -l app.kubernetes.io/name=kafka
```
- Now let's create a Topic
```
kubectl exec -it kafka-0 -- kafka-topics.sh \
       --create --bootstrap-server kafka-headless:9092 \
       --replication-factor 1 --partitions 1 \ 
       --topic mytopic
# output:
# Defaulted container "kafka" out of: kafka, volume-permissions (init)
# Created topic mytopic.
```
If this step fails, we need to verify that the kafka-0 and kafka-zookeeper-0 pods are in "Running" state.

### 6.3: Kafka Python
Kafka Python is a library that can be used to set up Kafka Producers or Kafka Consumers. The library is simply a client and we will need to run the Kafka broker separately.

### 6.3.1: Producers
- Once a producer is configured, we can send a message with the `.send()` method.
- The `.flush()` method is used to write a message immediately.
   - It's useful for a demo to view the results immediately.
   - In practice, flush() helps with performance by sending a batch of messages instead of a request for every message that is sent.

The producer.py can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/modules/Kafka/producer.py)

### 6.3.2: Consumers
- Consumers are helpful to receive messages from a message broker.
- Kafka consumers are typically part of a consumer group . 
- When multiple consumers are subscribed to a topic and belong to the same consumer group, each consumer in the group will receive messages from a different subset of the partitions in the topic.

The consumer.py can be found [consumer.py](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/modules/Kafka/consumer.py)

### 6.4: Running Producer and Consumer
- Once the Topic is created, in separate terminals start the consumer and producer.
```
kubectl exec -it kafka-0 -- kafka-console-consumer.sh \
        --bootstrap-server kafka-headless:9092 \
        --topic mytopic
# output:
# Defaulted container "kafka" out of: kafka, volume-permissions (init)
```
```
kubectl exec -it kafka-0 -- kafka-console-producer.sh \
       --broker-list kafka-headless:9092 \
       --topic mytopic
# output:
# Defaulted container "kafka" out of: kafka, volume-permissions (init)
# >message 1
# >message 2
```
- The "message 1" and "message 2" should appear in the consumer output. Exit producer with ctrl+d, and consumer with ctrl+c.

### 6.5: Kafka Deletion
The kafka/zookeeper installation can be deleted by removing the k8s resources and storage persistent-volume-claims "pvc" (the persistent volumes "pv" should be deleted automatically)
```
kubectl delete -f kafka.yaml
kubectl delete pvc data-kafka-0 data-kafka-zookeeper-0
```

# Step 7: Kubernetes Configurations
- Once the files for Microservices(Person,Location,Conenction) are created, we need to deploy them using the configuration files.
- We need to write our configuration files for microserives services and message passing techinque and it can be placed under `deployment/` folder
- After applying the configuration files successfully, we can see the Pods is in `Running` state
- The following command can be executed to deploy the services:
```
kubectl apply -f deployment/
```

The deployment files can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/UdaConnect/deployment)

# Step 8: OpenAPI
- The OpenAPI Specification, previously known as the Swagger Specification, is a specification for machine-readable interface files for describing, producing, consuming, and visualizing RESTful web services.
- OpenAPI is a specification that provides us with a framework for documenting our RESTful APIs.

### 8.1: REST Relies on Documentation
- RESTful APIs are highly reliant on their documentation.
- REST has little built-in enforcement for message structure and can be changed very easily.

### 8.1.1: Documentation Can Be Formatted Differently
- Documentation is very open-ended and can use different types of formatting and notation.

### 8.1.2: OpenAPI
- The OpenAPI specification provides us with a uniform way to detail our API resources and query for them
- OpenAPI includes a wide range of optional fields that enrich our documentation
- OpenAPI can be loaded into a tool called Swagger, a user-friendly, interactive API documentation accessible through a web page

### 8.2: Creating Swagger Documentation
- Swagger is an interactive tool that accepts OpenAPI documentation as input and provides a user interface for API documentation.
- Swagger libraries are available for most programming languages and provide various ways to populate our API documentation.
- [SwaggerHub](https://app.swaggerhub.com/) is a hosted version of Swagger that provides live previews and an interactive editor to check our OpenAPI syntax.

### 8.3: Maintaining Documentation
- Writing and maintaining documentation is often tedious. When we make a few changes to our code, we need to revisit our API documentation and reflect the latest changes.
- API documentation often drifts and becomes cumbersome to maintain.
- Rather than writing separate documentation for the work that we do, we can use integration tools to make our upkeep of documentation more manageable.

### 8.4: Options for OpenAPI
1. Manually update and maintain an OpenAPI specification file
   - This is the traditional way in how we have separate sets of documentation for our APIs.
- Example:
```
paths:
  /items/{itemId}:
     get:
      description: Retrieve the item with itemId
      parameters:
        - in: path
          name: itemId
          schema:
            type: string
          required: true
          description: ID of the item to get
```
2. Write our API specification as comments, and our libraries translate this into OpenAPI specifications
   - This makes it easier to upkeep our documentation by keeping the documentation in the same area as our application code. This way, our code and documentation live in the same file, so there is more accountability to keep them consistent.
- Example:
```
"""
@oas [get] /items/{itemId}
description: "By passing in an itemId you can retrieve the items information"
parameters:
- (path) category=all* {String} Item itemId
"""
def retrieve_items(item_id):
    # Route logic here
    pass
```
3. Use tightly-integrated libraries that will automatically detect how our code is structured and generate OpenAPI specifications for us
   - Some libraries will allow us to auto-generate documentation. This is the easiest to maintain and provides us little overhead on managing our documentation at the expense of flexibility. When it works, this is a powerful way to optimize productivity.
- Example:
```
@api.route("items/<item_id>")
@api.param("item_id", "Unique Item ID", _in="query")
class ItemResource(Resource):
    @responds(schema=ItemSchema)
    def get(self, item_id) -> Item:
        # API Logic
        pass
```
OpenAPI files can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/UdaConnect/docs)

# Step 9: Postman
- Postman is a commonly-used application to test APIs.
- It is an HTTP client that tests HTTP requests, utilizing a graphical user interface, through which we obtain different types of responses that need to be subsequently validated.

### 9.1: Getting Started With Postman
- Postman provides useful tools to make HTTP requests and view the data in the HTTP responses. It can also be used for:
    - Organizing and sharing HTTP requests as collections
    - API documentation
- To get started with Postman, go to: [Download Postman](http://postman.com/downloads/)

### 9.2: Validating the Solution
- To validate the solution, an API server is set up and the GET and POST requests are verified.

### 9.3: Run the API Server
- Run the application with python run in the same directory as app.py
- The application will be served on localhost:30001

### 9.4: Verify GET Request with Postman
- Create a new tab in the workspace
- Set up a GET request to localhost:30001/api/locations
- Sending a GET request returns the JSON payload, the HTTP status and the time to process the request.

### 9.5: Verify POST Request with Postman
- Create a new tab in the workspace
- Set up a POST request to localhost:30001/api/locations
- Set up a JSON body so that data can be passed in the request
- Sending a POST request returns the JSON payload, the HTTP status, the time to process the request, and the payload size

The postman.json file can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/docs/postman)

# Mentor Review from Udacity
![Mentor_Review_UdaConnect](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/UdaConnect/Images/Mentor_Review_UdaConnect.PNG)
