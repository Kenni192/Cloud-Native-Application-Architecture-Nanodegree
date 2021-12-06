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
