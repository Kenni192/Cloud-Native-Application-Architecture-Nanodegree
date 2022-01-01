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
## 2.4: Harden Weaknesses
- Harden the three Docker weaknesses we identified.
- We may need to reference the CIS_Docker_Benchmark_v1.2.0.pdf and [Docker security documentation.](https://docs.docker.com/engine/security/) If we get stuck and can’t figure out how to make the change, either pick a different attack surface to harden or try to get help through online research.
- Re-run Docker-bench to verify that the weaknesses we hardened have been addressed. Take screenshots of the result summary and all failed findings, and name the screenshots as `suse_docker_environment_hardened.png` or something similar in the `/submissions` directory of the project repo.

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
### Tip
- Depending our prior knowledge, we may or may not see a direct connection between the hypothesis in our threat model and the actual failed findings. This is common in the industry.
- One threat that we hypothesized in our threat model may be reflected by and related to multiple failed findings.
- In the real world, it is almost impossible or impractical to resolve and remediate all the weaknesses that are threat-modeled and reflected in the failed findings.
- There is not necessarily a right or wrong answer as long as we explain the reasoning using STRIDE.

## 2.5: Create a Hardened Kubernetes Environment
1. Deploy an RKE cluster using the Vagrantfile.
2. Run Kube-bench for the first time. Take screenshots of the result summary and all failed findings, and name the screenshots as `kube_cluster_out_of_box.png` or something similar in the `/submissions` directory of the project repo.
3. Apply [baseline hardening](https://rancher.com/docs/rancher/v2.x/en/security/rancher-2.4/hardening-2.4/) steps to the cluster.
4. Re-run Kube-bench to verify the cluster has been hardened via baseline hardening. Take screenshots of the result summary and all failed findings, and name the screenshots as `kube_cluster_hardened.png` or something similar in the `/submissions` directory of the project repo.

## 2.6: Kubernetes-specific test plan
- The most important aspect of hardening is making sure the hardening does not negatively affect system stability. The last thing we want is for our hardening to lead to an outage of the cluster.
- Write at least 200 words describing a Kubernetes-specific test plan based on what we learned from the course. The test plan does not need to address specific hardening steps. - Answer these two questions in test plan:
  - How will we test the changes?
  - How will we ensure the changes don't negatively affect our cluster?
- Save the test plan as `kube_hardening_test_plan.txt` in the `/submissions` directory of the project repo.

## 2.7: Setting up and Bringing up the RKE Cluster
### Overview
- In this step, we will set up the RKE cluster. We will bring up a 2-node cluster. The first node is a `control plane and etcd node`. The second node is a `worker`.
- The first node has two roles:
   - Control plane: With this role, the stateless components are used to deploy Kubernetes will run on these nodes. These components are used to run the API server, scheduler, and controller roles that are often separate roles in mainline Kubernetes. In RKE these have been packaged into the control plane role with RKE.
  - Etcd: With this role, the etcd container will be run on these nodes. Etcd keeps the state of your cluster and is one of the most important components and a single source of truth for your cluster.
- The second node is intentionally a simple worker:
  - With this role, any workloads or pods that are deployed will land on this node.
- For more details on the nodes, consult [Rancher's documentation on nodes](https://rancher.com/docs/rke/latest/en/config-options/nodes/)

## 2.7.1: RKE Cluster Setup Prerequisites:
- We need to download the RKE binary and add it to our home path directory in order to bring up the cluster. Below we will find the instructions on how to download and check the RKE binary.
   - Make sure you have [Vagrant](https://www.vagrantup.com/downloads) or higher installed
   - Make sure you have [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installed
   - Install the [RKE binary](https://rancher.com/docs/rke/latest/en/installation/)

### Note:
- This section is very important! Follow the steps very closely. Otherwise, we won't be able to bring up the RKE cluster.
- It's very important that we download the correct RKE binary for your system from this [page](https://github.com/rancher/rke/releases) and for this project used this [binary](https://github.com/rancher/rke/releases/download/v1.3.3/rke_linux-amd64)
- Check our path via `echo $PATH` and pick one path directory to move the binary into, e.g. /usr/local/bin /usr/bin
- Rename and move the binary into our chosen path via `mv rke_linux-amd64 /usr/local/bin/rke`. This assumes the downloaded `rke_linux-amd64 binary` is in the current directory.
- The binary must be renamed rke (lowercase) precisely. We will not be able to call the binary if the name is not rke.
- Mac and Linux: Make sure the binary is executable via $ chmod +x rke
- Windows: The file is already executable.
- Confirm that RKE is now executable by running the following command: rke --version. If it does not return something similar to rke version v1.2.6, we don't have RKE defined correctly in our $PATH. Go back and review the instructions.
- On macOS, the RKE binary may not be trusted when running for the first time. We need to go to "Security and Privacy Settings" and confirm "Allow Anyway". We will be hard blocked unless we verify and allow the binary.
- Finish the setup by installing kubectl and cloning the exercise starter repo.
  - Make sure you have [kubectl binary](https://kubernetes.io/docs/tasks/tools/#kubectl) installed
  - Clone the starter repo and cd to the `starter/` directory

## 2.7.2: Provision an RKE Cluster
1. Create Vagrant Boxes
  - On our local machine, cd to the `starter/` folder.
  - Run vagrant up to create Vagrant boxes.
  - Keep the Vagrantfile and the `bootstrap.sh` in the same directory.
  - When bringing up the environment, it's recommended not to use the root user to install Docker and not to have firewall and apparmor enabled. Therefore, the bootstrap.sh         script takes care of the following tasks when we run vagrant up: install Docker, disable firewalld, disable apparmor, set up rke user, and copy auth_keys for rke user.
  - It will take around 5-20 mins, depending on how performant our host machine is. If our host machine starts to hang, close unnecessary programs. If it still doesn't work, edit the Vagrantfile to reduce the VM memory to 2048 MB. If it still hangs try 1024 MB, this is the lower limit.

2. Check SSH Key Pair
  - Verify if `~/.ssh/id_rsa`` and ~/.ssh/id_rsa.pub` files exist by running `cat ~/.ssh/id_rsa` and `cat ~/.ssh/id_rsa.pub`
  - If these are not available, create a new SSH key pair using the following command and press ENTER for each prompt:
         ```
         ssh-keygen -t rsa -b 2048
         ```
  - This adds a new key pair to our `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub` file or create a new file if it doesn't exist.
  - Copy the SSH key for Vagrant box. This allows root access to the boxes without you having to type the password every time. These keys allow RKE to be deployed to the nodes      when we run rke up.
         ```
         sudo ssh-copy-id -i ~/.ssh/id_rsa root@192.168.50.101
         sudo ssh-copy-id -i ~/.ssh/id_rsa root@192.168.50.102
         ```
  - Agree to the prompts. The first password is our sudo machine password. The second password is for the key - vagrant. Provide them when prompted.

### Note:
- Make sure we specify the exact key file (e.g. ~/.ssh/id_rsa) via the -i switch we will use in the copy command. If we do not specify the key file to copy from, we may copy the wrong key and be hard blocked on bringing up the RKE cluster. If we get stuck, troubleshoot as follows:
  - Run `ls -la ~/.ssh/id_rsa` from your host machine to ensure it shows an accessible SSH key file.
  - `cat ssh-keygen -y -f ~/.ssh/id_rsa` should output the same exact public key that is installed on the nodes. Check by running `cat ~.ssh/authorized_keys` on each node by ssh'ing locally via `ssh root@192.168.50.101` / `ssh root@192.168.50.102`. Password is vagrant .
  - The key must match verbatim, no exceptions. If it does not, regenerate the key with the ssh command above and make sure we defined the key file when copying.
  - We may need to delete our old ssh known hosts. Otherwise, they will conflict with our current known_hosts file when we try to connect to the recreated nodes. We can do so by running `vim /Users/harini/.ssh/known_hosts` and removing the offending lines in vim with dd and :wq to save.
  - This is the warning you get when there is a conflict in current `known_hosts` file.
  - If this doesn't work, try to remove the known hosts file via rm -r /Users/harini/.ssh/known_hosts

3. [Optional] Make Sure You Can Access Each Node
  - We can now ssh into each node via
```
ssh root@192.168.50.101
ssh root@192.168.50.102
```
4. Create an RKE Cluster
   - Once the Vagrant boxes are up and running and the root SSH access is configured, we are ready to call the RKE binary to bootstrap the Kubernetes cluster.
   - The cluster.yml file contains an RKE configuration that will create a 2-node Kubernetes cluster. The first node is a control plane and etcd node. The second node is a worker.
  - Once we have all these prerequisites in place, use the following command to bootstrap the Kubernetes cluster: `rke up`

### Note for troubleshooting:
It will take around 10-20 mins to deploy RKE, depending on how performant oour host machine is. If our host machine starts to hang, close unnecessary programs. If it still doesn't work, edit the Vagrantfile to reduce the VM memory to 2048 MB. If it still hangs try 1024 MB, this is the lower limit. If the RKE setup fails, try Step 3 and see if we can ssh into each node without password. If not, try to run rke remove. Also, try the latest RKE release that may have bug fixes. If the cluster doesn't succeed, try to isolate the failing component(s). After running rke remove, scp it from our host to each node and run `./docker-clean.sh`

5.Check RKE Cluster Health
  - Once the installation is complete, a new kube_config_cluster.yml will be created in our `starter/` directory.We can now check the health of the Kubernetes cluster from our local host using the `kube_config_cluster.yml` kubeconfig file:
```
kubectl --kubeconfig kube_config_cluster.yml get nodes
```
  - If some of the pods are not running, we could try running rke up again.
  - If it still does not work, we will likely need to recreate the cluster and troubleshoot cluster creation.
  - Follow these steps:
     - Stop our Vagrant box with `vagrant halt node1` and `vagrant halt node2`
     - Check our Vagrant box status via `vagrant global-status`
  - Destroy our problematic Vagrant nodes via `vagrant destory <id>`
  - Recreate the cluster following the provided [instructions](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cleaning-cluster-nodes/) by Rancher
  - We may need to delete our old ssh known hosts 
### Note for troubleshooting:
- If our RKE cluster does not come up as ready, we may be unable to access the cluster, check the health of the pods that RKE deploys for each of the core services (CNI, DNS, Metrics).

## 2.8: Running Kube-bench to Evaluate Rancher RKE Master Node
- we will use Kube-bench to evaluate the actual attack surface.
- Follow the below steps to run kube-bench
1. SSH into node1 via `root@192.168.50.101`. The password is `vagrant`
2. Run `zypper in docker` to ensure the latest Docker is installed.
3. Execute the Docker container on the cluster nodes:
```
docker run --pid=host -v /etc:/node/etc:ro -v /var:/node/var:ro -ti rancher/security-scan:v0.2.2 bash

```
`rancher/security-scan:v0.2.2 bash` is a Docker container that we will start up. This will then run a security scan against this cluster and give us the results. Once you run this command, the context changes (you will be within the container context), and you can see the container id.
4. Within the container context, run Kube-bench scan against `node1` all components using the `rke-cis-1.6-hardenedbenchmark` profile via
```
kube-bench run --targets etcd,master,controlplane,policies --scored --config-dir=/etc/kube-bench/cfg --benchmark rke-cis-1.6-hardened
```
For the `--targets`, in Rancher's context, master is part of the controlplane, but we need to separately define it for the Kube-bench targets. There are different benchmark files within the local directory and container. In this case, we are running the benchmark profile rke-cis-1.6-hardened. Once we run this command, we will see 4 sets of failures, one for each of the 4 surfaces.
5. Filter for failures only and investigate the failures closely
```
 kube-bench run --targets etcd,master,controlplane,policies --scored --config-dir=/etc/kube-bench/cfg --benchmark rke-cis-1.6-hardened | grep FAIL
 ```
 ![3.Kube_cluster_out_of_box](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/3.Kube_cluster_out_of_box.PNG)
 
 ## 2.9: Harden Rancher RKE via Baseline Hardening
- When setting up an RKE cluster that we intend to harden, we have to create an etcd user and etcd group and change the permission of the etcd data directory to etcd:etcd in the configuration steps. These are part of the baseline RKE hardening steps.
- In the above image on the Running Kube-bench to Evaluate Rancher RKE Master Node, we saw that the check 1.1.12 Ensure that etcd data directory ownership is set to etcd:etcd (scored)fails because we have yet to apply the baseline RKE hardening steps.
-  we will configure etcd user and group hands-on. Here is [Rancher's documentation](https://rancher.com/docs/rancher/v2.x/en/security/rancher-2.5/1.6-hardening-2.5/#configure-etcd-user-and-group) on how to do so.
-  The trick is that we will harden the host on which the cluster is running. So we need to create a group called etcd on the host. /var/lib/etcd is the direction that we are going to change the permissions on.
-  Follow the below steps to harden RKE via baseline hardening
1. To add the etcd group, we run
```
groupadd --gid 52034 etcd
```
2. Then to add the etcd group, we run
```
useradd --comment "etcd service account" --uid 52034 --gid 52034 etcd
```
3. We then change the permission from what it is currently to etcd:etcd by running
```
chown etcd:etcd /var/lib/etcd
```
4. Re-run the Docker container that runs Rancher's security scan via
```
docker run --pid=host -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /etc:/node/etc:ro -v /var:/node/var:ro -ti rancher/security-scan:v0.2.2 bash
```
5. Now that the container has started, we re-run the scan on etcd and check if 1.1.12 still fails by running
```
kube-bench run --targets etcd --scored --config-dir=/etc/kube-bench/cfg --benchmark rke-cis-1.6-hardened | grep FAIL
```
We should see that `1.1.12` now passes and we have completed the hardening for etcd.

![4.Kube_cluster_hardened](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/4.Kube_cluster_hardened.PNG)

## Step 3: Harden and Deploy the Flask App
- Here we will focus on hardening and deploying the [Flask app](https://github.com/anxolerd/dvpwa/tree/b11d0415f86cc2285158d2f07c81cd9777d8fffb) by performing software introspection to identify and remediate vulnerable libraries and code.
  - The application has intentional security flaws in the code that you need to identify and remediate using your knowledge. There are four [documented](https://github.com/anxolerd/dvpwa) vulnerabilities. We will need to minimally remediate the Cross-Site Scripting vulnerability in the code and redeploy the app.
  - Fix the Cross-Site Scripting vulnerability in the `app.py` file located in `dvpwa/sqli/app.py`. Save the remediated `app.py` file in the `/submissions` directory of the project repo.
 
 The app.py can be found [here](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/app.py)
 
 ## 3.1: Configure and run Grype
 - Configure and run [Grype](https://github.com/anchore/grype) to identify vulnerabilities in the libraries and remediate them.
 - Run a Grype scan in the terminal for the first time. Take a screenshot of all Grype findings and save the screenshot as `grype_app_out_of_box.png` in the `/submissions` directory of the project repo.
- Research vulnerable libraries on the NVD website and remediate them.
- Re-run Grype until all vulnerable libraries are remediated. Take a screenshot of the Grype output showing 0 findings and save the screenshot as `grype_app_hardended.png` in the `/submissions` directory of the project repo.

### Note:
Ensure Grype is installed and configured on our machine.
```
brew tap anchore/grype
brew install grype
(or)
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
```

![5.grype_app_out_of_box](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/5.grype_app_out_of_box.PNG)

![6.grype_app_hardened](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Hardened%20Microservices%20Environment/submissions/6.grype_app_hardened.PNG)

## Step 4: Implement Runtime Monitoring and Grafana
Here we will focus on implementing Grafana to visualize run-time security alerts via Sysdig Falco.
1. Deploy Falco drivers, Falco, and falco-exporter.
2. Take a screenshot of the Falco and falco-exporter pods running. Save the screenshot as `kube_pods_screenshot.png` in the `/submissions` directory of the project repo.
3. Prove that Falco is generating security events by reading the content of a sensitive file. Take a screenshot of the warning message(s) from Falco pod logs or from the falco-exporter metrics page and save it as `falco_alert_screenshot.png` in the `/submissions` directory of the project repo.

Next, configure Falco to send security events to Grafana:
1. Configure the Prometheus Operator and Grafana.
2. Import the Falco panel for Grafana. At this point, we should have Grafana running with Falco logs flowing. If the Falco events are not showing up on Grafana, we can repeat Step 3 above to generate Falco events.
3. Take a screenshot of the Falco Grafana panel showing the Falco security event. Save the screenshot as `falco_grafana_screenshot.png` in the `/submissions` directory of the project repo.

## 4.1: Install Helm and Falco Drivers
- We will prepare to install Falco as a DaemonSet on our RKE cluster. DaemonSets are useful for deploying ongoing background tasks, which need to run on all or certain nodes but do not require user intervention. The DaemonSet-style deployment is suitable for Falco, as Falco runs silently on all the nodes in the cluster without user intervention. Falco only needs intervention by the security engineer or administrator.
- We will first need to install Helm, which is what we use to install and deploy Falco. If we don't have Helm installed on our machine, follow Steps 1-3 to install it.
1. From our local machine or the virtual machine, if we are using Windows, we need to curl the following URL to download the get_helm script:
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
```
2. Change the permissions in order to execute the script we downloaded:
```
chmod 700 get_helm.sh
```
3. Run the script to install Helm:
```
./get_helm.sh 
```
4. Check Helm version via `helm version`
```
version.BuildInfo{Version:"v3.5.4", GitCommit:"1b5edb69df3d3a08df77c9902dc17af864ff05d1", GitTreeState:"clean", GoVersion:"go1.15.11"}
```
### Note: 
We should install the latest version of Helm. Refer to this [page](https://helm.sh/docs/intro/install/) for the latest version.

5. Next, we need to add the `falcosecurity` repo using a Helm chart. Helm charts are ways to package applications for Kubernetes native environments. We add the `falcosecurity` repo in order to stage it locally:
```
helm repo add falcosecurity https://falcosecurity.github.io/charts
```
We then need to install special Falco drivers and kernel headers before installing Falco itself. Falco uses either a kernel module driver (also known as kmod) or an extended Berkeley Packet Filter (eBPF) driver in order to intercept syscalls and process them from a security perspective. We need to make sure the drivers are in place so that Falco can intercept syscalls to the kernel. Here are the steps to install Falco drivers and kernel headers:
1. SSH into `node1` and install the driver. Password is `vagrant`
```
ssh root@192.168.50.101
```
2. Execute the below command to install Falco
```
zypper -n install falco 
```
3. Execute the below commands to install necessary packages
```
zypper in kernel-devel
zypper in kernel-source
zypper in make
zypper in gcc
```
4. Reboot the node and ssh into the node again.
5. Download the `falcosecurity-3672BA8F.asc` file, which is a checksum for the drivers. Trust the falcosecurity GPG (GNU Privacy Guard) key:
```
rpm --import https://falco.org/repo/falcosecurity-3672BA8F.asc
```
6. Next, we will curl and configure the zypper repository that contains the drivers:
```
curl -s -o /etc/zypp/repos.d/falcosecurity.repo https://falco.org/repo/falcosecurity-rpm.repo
```
### Note: 
`/etc/zypp/repos.d/falcosecurity.repo` is the name of the repo. `https://falco.org/repo/falcosecurity-rpm.repo` is the location of the repo.

7. Install the kernel headers. This is a key step, where we will apply the SUSE-specific kernel headers prepared by the Falco team in order to intercept syscalls on the SUSE operating system.
```
zypper -n install kernel-default-devel 
```
### Note: 
- The installation will take about 5 minutes. The version should be something close to 5.3.18, specifically for the x86 64-bit operating system that SUSE runs.
- It is important to `reboot` node1 once the installation is complete. Execute the below commands to reboot the node
```
vagrant halt
vagrant up
```
## 4.2: Install Falco as a DaemonSet on RKE and Check Falco Health
we will install Falco as a DaemonSet with specific configurations.
1. Ssh into the node again and add the Falco repo via
```
helm repo add falcosecurity https://falcosecurity.github.io/charts
```
2. Update the Helm repo to get the latest charts:
```
helm repo update
```
3. Install Falco using the provided Helm chart:
```
helm install --kubeconfig kube_config_cluster.yml falco falcosecurity/falco \
  --set falco.grpc.enabled=true \
  --set falco.grpcOutput.enabled=true \
```
### Note:
In this command, we are setting important parameters. falco.grpc.enabled=true and falco.grpcOutput.enabled=true ensure that Falco outputs logs using the gRPC protocol. This will then allow the falco-exporter to collect those logs, stage them, and later be scrapped by Prometheus.

4. Run `kubectl --kubeconfig kube_config_cluster.yml` get pod to check Falco pod health. If the pod is still being created, the status of the Falco pod will say `ContainerCreating`. After a minute or two, the Falco pod status should change to `Running`

## Step 5: Incident Response
Lastly, we will focus on introducing a suspicious command onto the Kubernetes cluster simulating a security incident. A payload is a script or file that delivers a malicious action such as running malware.
1. From the [starter repo](https://github.com/udacity/nd064-c3-microservices-security-project-starter/tree/master/starter/scripts), run the `payload.sh` to introduce a suspicious command intentionally.

The `kubectl run` commands in the payload.sh will run containers instantiated from legacy Docker images, such as [servethehome/monero_cpu_moneropool](https://hub.docker.com/r/servethehome/monero_cpu_moneropool), on our cluster. We use these as a canonical example as they are reliable and clearly illustrate falco in action in a controlled learning environment. Those Docker images will run illegitimate crypto mining software and have multiple security issues, such as not using the secure communication channels and not having a software bill of materials used in the image. We have intentionally chosen these Docker images to simulate a controlled security incident. Executing such suspicious workloads in a controlled environment poses a small security risk, particularly if our system is not patched. To be ultra cautious, make sure our host system is patched before we run the crypto demo to reduce the risk. In the real world, patching is a vital practice, always make sure our host systems are patched, and remember that attackers do not ask for permission to attack.

2. Using the template in the [repo](https://github.com/udacity/nd064-c3-microservices-security-project-starter/blob/master/starter/incident_response/incident_response.txt), write an incident response report to the CTO to describe what happened. Make sure to be thoughtful and precise as we are writing to an executive. Write at least two sentences for each of the questions in Questions 2-6. Save the `incident_response_report.txt` in the `/submissions` directory of the project repo.
