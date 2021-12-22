# Building a Metrics dashboard

## Overview
In this project, we will create dashboards that use multiple graphs to monitor our sample application that is deployed on a Kubernetes cluster. We will be using [Prometheus](https://prometheus.io/), [Jaeger](https://www.jaegertracing.io/), and [Grafana](https://grafana.com/) in order to monitor, trace and visualize your experience.

## Main Steps
Here are the main steps we'll carry out for this project:

1. Deploy the sample application in our Kubernetes cluster.
2. Use Prometheus to monitor the various metrics of the application.
3. Use Jaeger to perform traces on the application.
4. Use Grafana in order to visualize these metrics in a series of graphs that can be shared with other members on our team.
5. Document our project in a README.

At the end of this process, we'll have our own observability dashboard!

The process is summarized in the diagram below.

![Architecture_Diagram](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Building%20a%20Metrics%20Dashboard/image/Architecture_Diagram.PNG)

# Project Steps
## Step 1: Project Setup
- By the end of this task, we should have our dependencies installed and our project set up.
- We have been provided with some starter files to help us get started with our project. If we haven't already, we can download the starter files from this [GitHub repository.](https://github.com/udacity/CNAND_nd064_C4_Observability_Starter_Files)
- The files we'll need are located in the Project_Starter_Files directory. It's recommended that we work within the existing directory structure.

## 1.1: Open the README template
- A major part of showing our work for this project consists of filling out a README file. 
- A template README with TODOs for us to complete is provided. We will probably want to work on this as we go through the other project steps, so it is encouraged us to open it now and revisit it as we go through the instructions.

## 1.2: Preparing Kubernetes
- Before we start anything, we need to ensure that you have a Kubernetes cluster available. 
- While we can use a myriad of managed Kubernetes providers, It's encouraged us to use K3s with Vagrant. 
- The good news is that the Vagrantfile calls a k3s.sh to simplify the process. 
- Feel free to look at the file if we want to learn how to stage it manually.

To create a vagrant box and ssh into it, use the following commands:
```
# create a vagrant box using the Vagrantfile in the current directory
vagrant up

# SSH into the vagrant box
# Note: this command uses the .vagrant folder to identify the details of the vagrant box
vagrant ssh
```

## Step 2: Setting up Observability
- Using Prometheus, Jaeger, and Grafana, we will be able to start monitoring our applications in real time. We need to get these components installed on our cluster before installing the application.

## 2.1: Install Helm
- Helm is a popular package manager for Kubernetes. It is similar to Aptitude for Ubuntu or Homebrew in Mac OS X.
- First we will need to install Helm v3. We can do it by running the command below.
```
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

## 2.2: Installing Grafana and Prometheus
- With Helm installed, it is much easier to install Grafana and Prometheus.
- These are the lines of code we will want to run

1. We want to create the monitoring namespace
```
kubectl create namespace monitoring
```
2. Now, let's install Grafana and Prometheus
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm repo add stable https://kubernetes-charts.storage.googleapis.com # this is deprecated
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml
```
3. Grafana site can be accessed by `https://127.0.0.1:3000/` or `localhost:3000`
![4.Grafana_Home_Page](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Building%20a%20Metrics%20Dashboard/answer-img/4.Grafana_Home_Page.PNG)

4. Verify that it installed
```
kubectl get pods,svc --namespace=monitoring
```
![2.Monitoring](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Building%20a%20Metrics%20Dashboard/answer-img/2.Monitoring.PNG)
![3.Monitoring_pods_services](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Building%20a%20Metrics%20Dashboard/answer-img/3.Monitoring_pods_services.PNG)

### Note:
When installing via the Prometheus Helm chart, the default Grafana credentials are:
```
username: admin 
password: prom-operator
```

## 2.3: Install Jaeger
- We will now install Jaeger Tracing to our cluster
- Run the below code to create the "observability" namespace and install the Jaeger components:
```
kubectl create namespace observability
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/operator.yaml
```

## 2.4: Cluster wide Jaeger
- Because we want to observe other namespaces, we'll need to go ahead and give Jaeger cluster wide visibility. In the real world, we may limit visibility to specific namespaces, but it isn't unheard of to give ourself cluster visibility.
- Run the below commands:
```
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/
```
![5.Jaegar](https://github.com/Harini-Pavithra/Cloud-Native-Application-Architecture-Nanodegree/blob/main/Building%20a%20Metrics%20Dashboard/answer-img/5.Jaegar.PNG)

Great! We have installed Jaeger, Prometheus, and Grafana. We are now ready to work!
