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
