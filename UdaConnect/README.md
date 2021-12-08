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
