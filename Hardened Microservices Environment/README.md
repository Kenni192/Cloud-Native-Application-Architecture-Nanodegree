# Hardened Microservices Environment

## Project Overview
### Background
Security is a highly dynamic topic with ever-changing threats and priorities. Newsworthy topics ranging from Fortune 500 companies like Garmin paying $10 million in ransom 
for ransomware attacks to supply chain attacks such as Solarwinds are ever-present. The Synopsis 2020 Open Source Security Risk Analysis Report revealed that 99% of audited 
codebases contained open source, and within those codebases 75% of open source vulnerabilities were left unpatched, creating risk.

Our company's CTO is worried about what the engineering team is doing to harden and monitor the company's new microservice application against malicious threat actors and payloads.
We’ve completed the course and have a baseline understanding of how to approach this.

In response to the CTO's concerns, we will threat-model and harden a microservices environment based on what we have learned from this course.

### Goal
We will be presented with the challenge to build a secure Microservice environment, threat modeling the container image, run-time environment, and the application itself. 
For the purpose of the project, we will be provided with instructions to build, harden and provision an environment analogous to the company's new microservice application. 
It is a simplified Python Flask application.

Once the Microservice environment is hardened and provisioned, we will configure Sysdig Falco to perform run-time monitoring on the node, sending logs to a Grafana node for visualization. 
To demonstrate to the CTO that the company can respond to a real cyber threat, we will then simulate a tabletop cyber exercise by running a script to introduce an unknown 
binary from the starter code that will disrupt the environment!

No stress, we have the tools and security incident response knowledge to respond ;) Our goal will be to use Grafana to determine what the unknown binary is, contain and remediate the environment, 
write an incident response report and present it to the CTO. There will be a few hidden easter eggs, see if we can find them for extra credit.

## Project Steps Overview
1. Architecture diagram, and threat model the Docker image, Kubernetes infrastructure, and Flask application environment.
2. Create a hardened Docker environment with Docker-bench using the provided hardened OpenSUSE leap image.
3. Create an RKE cluster and walk through a testing methodology for how to harden a Kubernetes cluster.
4. Configure and run Grype and Trivy to identify software composition vulnerabilities, remediate and deploy the app.
5. Implement Falco and Grafana for run-time monitoring.
6. Run a script to introduce an unknown payload intentionally.
7. Identify the unknown binary and take steps to remediate it.

# Getting Started
- The starter files for the project can be found in the [project repository](https://github.com/udacity/nd064-c3-Microservices-Security-project-starter/tree/master/)
- The /starter directory contains everything except the vuln_app which is the root.

![Directory](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/image/Directory.PNG)

Where:

- `Dockerfile` to provision a container image using an OpenSUSE image.
- `LICENSE` is a license for the course content.
- `Vagrantfile` to configure a Vagrant box. It will be used to create a Vagrant box locally.
- `cluster.yml` to provision a Rancher RKE 1-node cluster.
- `reference_hardened_cluster.yml` is a reference hardened cluster.yml to guide you. You cannot use the reference_hardened_cluster.yml file as-is to startup the cluster.
docs contains reference PDFs.
- `incident_response` directory contains a incident_response.txttemplate responding to an incident. You will use it later ;)
- `scripts directory` contains a payload.sh that will be used later in the project. Keep an eye on it!
- `security_architecture` directory contains example security architecture diagrams.
- `threat_modeling` directory contains a threat_modeling_template.txt template for STRIDE threat modeling.

- The `vuln_app` is contained in the repo root as a submodule linked from the [source repo](https://github.com/anxolerd/dvpwa):

![Folder_Structure](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/image/Folder_Structure.PNG)

Where:

- `Dockerfile.app` defines that this is a dockerized application.
- `Dockerfile.db` indicates that there is a Dockerized database.
- `LICENSE` defines a license from the developer of dvpwa.
- `README.rst` contains an application startup readme.
- `config` contains configurations to startup the application.
- `docker-compose.yml`: Run this to bring up the application.
- `migrations` folder contains migration scripts.
- `recreate.sh` allows us to recreate the database.
- `requirements.txt` file defines all the libraries required to run this application.
- `run.py` the primary Python app startup directory.
- `sqli` is the configuration directory for the SQLite database that's run as part of the application.

- To run this vuln_app follow these steps:
1. Run the Flask program by using the docker-compose up command.
2. The application should be running on port 8000. You can access it by querying the http://localhost:8080endpoint.

## Dependencies
1. Clone the project code from [course repo](https://github.com/udacity/nd064-c3-microservices-security-project-starter)
2. Install Python >= 3.0 using the instructions provided in the [Official Python Documentation](https://www.python.org/downloads/)
3. Install Git >= 2.27.o using the instructions provided in the [Official Git Documentation](https://git-scm.com/downloads)
4. Install Docker >= 18.09 using the instructions provided in the [Official Docker Documentation](https://docs.docker.com/get-docker/)
5. Install Vagrant >= 2.2.14 using the instructions provided in the [Official Vagrant Documentation](https://www.vagrantup.com/downloads)
6. Install VirtualBox >= 6.1 using the instructions provided in the [Official VirtualBox Documentation](https://www.virtualbox.org/wiki/Downloads)

# Project Steps

## Step 1: Threat Model the Microservices Environment
- In this first step, we will apply what we learned about STRIDE threat modeling in the lessons to document and threat model your microservices environment. We will define a security architecture for our environment and identify attack surfaces. The environment consists of the following:
   - Single OpenSUSE Linux virtual machine (host)
   - An RKE cluster deploy to the Linux virtual machine node cluster (cluster)
   - The cluster runs a vulnerable python application (service)
   - Docker is running on the host node to manage containers (container daemon)
- Our goal is to think like an attacker and reason about security weaknesses that could be attacked. The intent is to mimic what we should do in the real world, whereby we should perform threat modeling and a security architecture review at the onset of your microservices project.

## Instructions:
- Using [lucid chart free version](https://lucid.app/documents#/dashboard) or [Google docs](https://www.google.com/docs/about/), create a diagram of the environment we are about to implement.
  - Our diagram should minimally abstract the openSUSE host, RKE cluster, Python service, and Docker container daemon we will deploy.
  - We should identify service and security boundaries with lines and data flow with arrows. 
  - Save the file as `security_architecture_design.png` in the `/submissions` directory of the project repo.
- Using the STRIDE threat modeling methodology and the `threat_modeling_template.txt` in the `/starter/threat_modeling` directory of the project repo, document 5 concrete attack surface areas for the Docker environment and 5 concrete attack surface areas for the Kubernetes control plane, etcd, and worker.
  - In our explanation, associate each attack surface area to at least one pillar of the STRIDE model, which includes Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. There can be multiple attack surface areas associated with one pillar, but the attack surface areas have to be distinct.
  - Save the `threat_modeling_template.txt` document in the `/submissions` directory of the project repo.
  - We can reference the following documents if you need a reminder of the attack surfaces:
     - [CIS_Docker_Benchmark_v1.2.0.pdf](https://github.com/udacity/nd064-c3-microservices-security-project-starter/blob/master/starter/docs/CIS_Docker_Benchmark_v1.2.0.pdf) (provided courtesy of the Center for Internet Security)
     - [Rancher_Benchmark_Assessment.pdf](https://github.com/udacity/nd064-c3-microservices-security-project-starter/blob/master/starter/docs/Rancher_Benchmark_Assessment.pdf)
     - [Rancher Hardening Guide with CIS 1.6 Benchmark](https://rancher.com/docs/rancher/v2.x/en/security/rancher-2.5/1.6-hardening-2.5/)

### Note
Think like an attacker and reason from there.

## Step 2: Harden the Microservices Environment
- Here we will focus on hardening the Docker environment by using Docker-bench. Once the hardened container image is committed to a provider registry, we will use it to create an RKE cluster. We will then harden the RKE cluster. By the end of this step, we should have a hardened Docker host running on a hardened RKE cluster.

### 2.1: Docker-Bench Installation
- Follow the below steps to complete the Docker-Bench installation
```
1. go env //Instaling go is one of the important steps for installing docker-bench
2. sudo docker pull opensuse/leap:latest 
3. sudo docker images | grep opensuse
4. sudo docker build . -t opensuse/leap:latest -m 256mb --no-cache=true 
5. sudo docker image ls
6. sudo docker run opensuse/leap
7. git clone https://github.com/udacity/nd064-c3-microservices-security-project-starter.git
8. git clone https://github.com/anxolerd/dvpwa.git
9. git clone https://github.com/aquasecurity/docker-bench.git
```
The Docker-Bench is now successfully installed.

### 2.2: Create a Hardened Docker Environment
### Identify weaknesses
- Using the starter `Dockerfile` in the starter repo and an openSUSE base image, create a hardened Docker environment with Docker-bench.
- Run Docker-bench for the first time. Take screenshots of the result summary and all failed findings, and name the screenshots as `suse_docker_environment_out_of_box.png`` or something similar in the `/submissions` directory of the project repo.
- Using the `CIS_Docker_Benchmark_v1.2.0.pdf` from the starter repo, review the findings from running the docker-bench.
- From the failed findings, select and document 3 failed findings from the Docker-bench results that we want to harden. These 3 findings should confirm 3 out of the 5 attack surface areas we identified for Docker in Step 1. At least 1 of the 3 findings should be different from the ones mentioned in the exercise 
- Document each of the 3 findings we want to harden to the existing threat_modeling_template.txt file and save the file in the `/submissions` directory of the project repo.

### 2.3: Hardening using Docker-Bench
- Follow the below steps to harden the environment.
```
1. cd  /docker-bench  
2. go build -o docker-bench 
3. ./docker-bench --include-test-output > docker-bench.txt --version 20.10.11
4. cat docker-bench.txt | grep FAIL
```
- From the failed findings, let's select 2.14,2.15,2.16 & 3.17 fails and harden them.
- Follow the below steps to harden the above fails 
```
#Procedure 1
create `daemon.json file` in /etc/docker/ path and add the below lines
{
 "live-restore": true
 "no-new-privileges": true
 "userland-proxy": false
 "disable-legacy-registry": true
}
```
```
#Procedure 2
Execute the below commands one by one
1. sudo dockerd --live-restore
2. sudo dockerd --no-new-privileges
3. sudo dockerd --userland-proxy=false
4. sudo dockerd --disable-legacy-registry
```
- If we re-run the docker-bench tool, we will not see the fails and thus the environment is hardened using Docker-Bench tool.

### Before Hardening the Environment

![1.Suse_docker_environment_out_of_box](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/1.Suse_docker_environment_out_of_box.PNG)

### After Hardening the Environment

![2.Suse_docker_environment_hardened](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/2.Suse_docker_environment_hardened.PNG)

### Note:
The docker services can be checked and started using the below commands
```
1. service docker status
2. service docker start 
```
