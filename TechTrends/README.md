# Overview

TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them.

Imagine the following scenario: We joined a small team as a Platform Engineer. The team is composed of 2 developers, 1 platform engineer (you), 1 project manager, and 1 manager. The team was assigned with the TechTrends project, aiming to build a fully functional online news sharing platform. The developers in the team are currently working on the first prototype of the TechTrends website. As a platform engineer, we should package and deploy TechTrends to Kubernetes using a CI/CD pipeline.

The web application is written using the Python Flask framework. It uses SQLite, a lightweight disk-based database to store the submitted articles.

Below we can examine the main components of the firsts prototype of the application:

![TechTrends Application](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/images/TechTrends_Application.png)

Additionally, the initial sitemap of the website can be found below:

![Sitemap](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/images/Sitemap.png)

Where:

- About page - presents a quick overview of the TechTrends site
- Index page - contains the content of the main page, with a list of all available posts within TechTrends
- New Post page - provides a form to submit a new post
- 404 page - is rendered when an article ID does not exist is accessed
- And lastly, the first prototype of the application is storing and accessing posts from the "POSTS" SQL table. A post entry contains the post ID (primary key), creation timestamp, title, and content. The "POSTS" table schema can be examined below:

![Post Schema](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/images/Post_Schema.png)

# Project Steps Overview
1. Apply the best development practices and develop the status and health check endpoints for the TechTrends application.
2. Package the TechTrends application by creating a Dockefile and Docker image.
3. Implement the Continuous Integration practices, by using GitHub Actions to automate the build and push of the Docker image to DockerHub.
4. Construct the Kubernetes declarative manifests to deploy TechTrends to a sandbox namespace within a Kubernetes cluster. The cluster should be provisioned using k3s in a vagrant box.
5. Template the Kubernetes manifests using a Helm chart and provide the input configuration files for staging and production environments.
6. Implement the Continuous Delivery practices, by deploying the TechTrends application to staging and production environments using ArgoCD and the Helm chart.

# Getting Started
The starter files for the TechTrends application can be found in the [course repository](https://github.com/udacity/nd064_course_1/tree/main/project/techtrends)

This repository file structure can be found below:

![Structure](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/images/Structure.PNG)

Where:

- README.md contains the main steps of how to execute the TechTrends application
- __init__.py is a reserved method used to indicate that a directory is a Python package
- app.py contains the main logging of the TechTrends application
- init_db.py is a file that is used to initialize the posts database with a set of articles
- requirements.txt contains a list of packages that need to be installed before running the TechTrends application
- schema.sql outlines the posts database schema
- static/ folder contains the CSS files
- templates/ folder outlines the HTML structure of the TechTrends application

Within the project folder we will notice some extra folders and files. These will be used to record our commands and output screenshots.

- argocd - the folder that will contain the ArgoCD manifests
- helm - the folder that will contain the Helm chart files
- kubernetes - the folder that will contain Kubernetes declarative manifests
- screenshots - the folder that will contain all the screenshots that you take throughout the course
- Vagrantfile - the file containing the configuration for the vagrant box. Will be used to create a vagrant box locally.
- docker_commands - the file will be used to record any used Docker commands and outputs

To run this application follow these steps:

1. Initialize the database by using the python init_db.py command. This creates or overwrites (if the file already exists) the database.db file that is used to store and access the available posts.
2. Run the TechTrends application by using the python app.py command. The application is running on port 3111 and you can access it by querying the http://127.0.0.1:3111/ endpoint.

# Dependencies

1. Fork the [course repository](https://github.com/udacity/nd064_course_1/tree/main/project) containing the Techtrends application.
2. Python 3.6 or higher
3. Git
4. Docker
5. Vagrant 
6. VirtualBox 6.1.16 or higher

# Step 1:

## Best Practices For Application Deployment
Throughout this step, we should apply some of the learned best development practices to the TechTrends project. As a result, we will implement the metrics and health check endpoints, in addition to the logging functionality.

### Healthcheck endpoint
Build the /healthz endpoint for the TechTrends application.The endpoint should return the following response:
 - An HTTP 200 status code
 - A JSON response containing the result: OK - healthy message

### Logs
Extend the TechTrends application to log the events

### Screenshot

![Step_1](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_1/Step_1.png)

Every log line should include the timestamp and be outputted to the STDOUT and STDERR. Also, capture any Python logs at the DEBUG level.

# Step 2: 

## Docker for Application Packaging
This step focuses on packaging the application using Docker. We will write a Dockerfile and build a Docker image for the TechTrends project. By the end of this step, we should have the application running locally inside a Docker container.

## Dockerfile
Build a Dockerfile with instructions to package the TechTrends application. The Dockerfile should contain the following steps:
- Use a Python base image in version 2.7
- Expose the application port 3111
- Install packages defined in the requirements.txt file
- Ensure that the database is initialized with the pre-defined posts in the init_db.py file
- The application should execute at the container start

The completed Docker file can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/techtrends/Dockerfile)

## Docker Image
Using the Dockerfile defined above, create a Docker image and test it locally. The Docker build command should:
- Reference the defined Dockerfile
- Tag the image as techtrends
- Make sure you specify the location of the Dockerfile

## Run and test locally
Test the Docker image locally, with the following specifications:
- Using the detached mode
- Expose the application port on port 7111 on the machine

Access the application in the browser using the http://127.0.0.1:7111 endpoint and try to click on some of the available posts, create a new post, access the metrics endpoint, etc.Once this stage is complete and we can confirm that the application is up and running, use the Docker commands to retrieve the logs from the application.

![docker_run_local](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_2/docker_run_local.png)

# Step 3:

## Continuous Integration with GitHub Actions
This step aims to use the Continuous Integration (CI) fundamentals and automate the packaging of the TechTrends application. We will use GitHub Actions to build, tag, and push the TechTrends Docker image to DockerHub. As a result, we should have a functional GitHub Action that will construct a new image with every new commit to the main branch.

## GitHub Actions
Created a GitHub Action that will package and push the new image for the TechTrends application to DockerHub. The configuration file with the name techtrends-dockerhub.yml is placed in the .github/workflows/ directory. If the directory does not exist, create it using the mkdir -p .github/workflows/ command.

These functionalities should be implemented using the Build and Push Docker images upstream GitHub Action at the basis. The following action uses DockerHub Tokens and encrypted GitHub secrets to login into DockerHub and to push new images. To set up these credentials refer to the following resources:
- Create [DockerHub Tokens](https://www.docker.com/blog/docker-hub-new-personal-access-tokens/)
- Create [GitHub encrypted secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)

Constructed a GitHub Action, that would package and push the TechTrends application with the following requirements:
- name - "TechTrends - Package with Docker"
- Trigger on every push to the main branch
- Run the action on the ubuntu-latest operating system
- For the Docker build and push step:
    - Context should be set to the project directory
    - Reference the Dockerfile for TechTrends application
    - Push the image to DockerHub with the tag techtrends:latest

After creating the GitHub Action verify it executes successfully when a new commit is pushed to the master branch. Verified DockerHub account for the TechTrends image with the tag latest being pushed successfully.

![ci-github-actions](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_3/ci-github-actions.JPG)

# Step 4:

## Kubernetes Declarative Manifests
In this step, we deployed a Kubernetes cluster using k3s and deploy the TechTrends application. We created declarative Kubernetes manifests and release the application to the sandbox environment. By the end of this step, we should have a collection of YAML manifests that will manage the TechTrends application within the cluster.

## Deploy a Kubernetes cluster
Using vagrant, create a Kubernetes cluster with k3s. Refer to the [Vagrantfile](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/Vagrantfile) from the course repository. Make sure to have vagrant and VirtualBox 6.1.16 or higher installed.

To create a vagrant box and ssh into it, use the following commands:
```
# create a vagrant box using the Vagrantfile in the current directory
vagrant up

# SSH into the vagrant box
# Note: this command uses the .vagrant folder to identify the details of the vagrant box
vagrant ssh
```
To deploy the Kubernetes cluster, refer to the [k3s](https://k3s.io/) documentation or use the following command
```
curl -sfL https://get.k3s.io | sh -
```
To interact with the cluster kubectl, you need to have root access to the kubeconfig file. Hence, use sudo su - to become root and use kubectl commands.
Verify if the cluster is operational by evaluating if the node in the cluster is up and running. We can use the below command.
```
kubectl get no
```

![k8s-nodes](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_4/k8s-nodes.JPG)

## Kubernetes Declarative Manifests
Using the declarative approach, deploy the TechTrends application to the Kubernetes cluster. Construct the YAML manifests for the following resources:

- Namespace in namespace.yaml file:
   - name: sandbox
- Deployment in deploy.yaml file:
  - namespace: sandbox
  - image: techtrends:latest
  - name:techtrends
  - replicas: 1
  - resources:
    - requests: CPU 250m and memory 64Mi
    - limits: CPU 500m and memory 128Mi
- container port: 3111
- liveness probe:
  - path: /healthz
  - port: 3111
- readiness probe:
  - path: /healthz
  - port: 3111
- Service in service.yaml file:
  - namespace: sandbox
  - name: techtrends
  - port: 4111
  - target port: 3111
  - protocol: TCP
  - type: ClusterIP

### NOTE: 
namespace.yaml, deploy.yaml and service.yaml in the [kubernetes](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/TechTrends/kubernetes) folder.

## Deploy TechTrends with Kubernetes manifests
Using the Kubernetes manifests and kubectl commands, deploy the TechTrends application to the k3s cluster. As a result, we should have the following resource created:

- a sandbox namespace
- a techtrends deployment, in the sandbox namespace with 1 replica or pod running
- a techtrends service that exposes the TechTrends application on port 4111 using a ClusterIP

To list down all the pods, services in a namespace use the following command,
```
kubectl get all -n sandbox
```

# Step 5:

## Helm Charts
Throughout this step, we used a template configuration manager, such as Helm, to parameterized the TechTrends manifests. We build a Helm Chart to template and release the application to multiple environments. As a result, we should have a collection of parametrized YAML manifests that used an input values file to generate valid Kubernetes objects.

## Helm Chart
Using the YAML manifests build in the previous step, create a Helm chart with the following specifications:

Chart.yaml file:
- apiVersion: v1
- name: techtrends
- keywords: techtrends
- version: 1.0.0
- list yourself as a maintainer

[templates/](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/TechTrends/helm/templates) folder has the following parameterized files:

- deploy.yaml
- namespace.yaml
- service. yaml

values.yaml file should provide input for the following parameters (Note: these input values act as defaults for the Helm chart):
- namespace name: sandbox
- service:
  - port: 4111
  - targetPort: 3111
  - protocol: TCP
  - type: ClusterIP
- image:
  - repository: techtrends
  - tag: latest
  - pullPolicy: IfNotPresent
- replicaCount: 1
- resources:
  - requests: memory 64Mi and CPU 250m
  - limits: memory 128Mi and CPU 500m
- containerPort: 3111
- livenessProbe path: /healthz check on containerPort
- readinessProbe path: /healthz check on containerPort

## Values.yaml files for multiple environments
Once we have constructed the Helm chart with a default "values.yaml" file, create 2 more input files with the following specifications:

values-staging.yaml file:
- namespace name: staging
- service port: 5111
- replicaCount: 3
- resources:
  - requests: memory 90Mi and CPU 300m
  - limits: memory 128Mi and CPU 500m

values-prod.yaml file:
- namespace name: prod
- service port: 7111
- image pullPolicy: Always
- replicaCount: 5
- resources:
  - requests: memory 128Mi and CPU 350m
  - limits: memory 256Mi and CPU 500m

### Note: 
Helm chart files are placed in the [helm](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/TechTrends/helm) folder.

# Step 6:

## Continuous Delivery with ArgoCD
In this final step, we deployed the TechTrends automatically using Continuous Delivery fundamentals. We made use of ArgoCD to release the application to staging and production environments using the templated manifests from the Helm chart. By the end of this step, we should have an automated and templated procedure to deploy TechtTends to multiple environments.

## Deploy ArgoCD
Given the k3s cluster, install ArgoCD and access it through the browser. Make sure to reference the instructions below:

- Official [install guide for ArgoCD](https://argoproj.github.io/argo-cd/getting_started/#1-install-argo-cd)
- The YAML manifest for the NodePort service can be found under the [argocd-server-nodeport.yaml](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/argocd/argocd-server-nodeport.yaml) file in the course repository
- Access the ArgoCD UI by going to https://192.168.50.4:30008 or http://192.168.50.4:30007
- Login credentials can be retrieved using the steps in the [credentials guide](https://argoproj.github.io/argo-cd/getting_started/#4-login-using-the-cli)

![argocd_ui](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_5/argocd_ui.PNG)

## ArgoCD Applications
Create ArgoCD Applications resources to deploy TechTrends to staging and production environments. We need to reference the TechTrends Helm chart built in the previous step and use the respective input files. As such, create the following ArgoCD application manifests:

helm-techtrends-staging.yaml:
 - name: techtrends-staging
 - values file: values-staging.yaml

helm-techtrends-prod.yaml:
 - name: techtrends-prod
- values file: values-prod.yaml

### Note: 
ArgoCD manifests is placed in the [argo folder](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/tree/main/TechTrends/argocd)

## Deploy TechTrends with ArgoCD
Using kubectl commands apply the ArgoCD Applications manifests. Make sure to synchronize the application in ArgoCD, so that all the TechTrends resources is deployed successfully. As a result, we should have 2 new namespaces, staging and prod, a deployment for each environment (each with a different amount of pods), and a service exposing the application on different ports.

![argocd-techtrends-staging](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_5/argocd-techtrends-staging.PNG)

![argocd-techtrends-prod](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/screenshots/Step_5/argocd-techtrends-prod.PNG)

# Mentor Review from Udacity

![Mentor_Review_TechTrends](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/TechTrends/images/Mentor_Review_TechTrends.PNG)
