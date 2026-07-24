# ☸️ Kubernetes HPA Auto-Scaling & Self-Healing with GitLab CI/CD

[![GitLab Pipeline Status](https://img.shields.io/gitlab/pipeline-status/doanhiep169/loadtest-api?branch=main&style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com/doanhiep169/loadtest-api/-/commits/main)
[![Kubernetes Version](https://img.shields.io/badge/kubernetes-v1.30-blue?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/docker-container-blue?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

<details>
<summary><strong>📑 Table of Contents (Click to expand)</strong></summary>

- 📌 [Introduction](#introduction)
- 🚀 [Key Features](#key-features)
- 🏗️ [Architecture Overview](#architecture-overview)
- 📁 [Project Structure](#project-structure)
- 🛠️ [Technologies Used](#technologies-used)
- 🎬 [Demo Videos](#demo-videos)
- ☁️ [AWS Infrastructure Setup](#aws-infrastructure-setup)
- 💻 [Quick Start](#quick-start)
- ✅ [1. 2-Node Cluster Status](#step-1)
- 🔒 [2. Custom Domain & Valid HTTPS Certificate](#step-2)
- 📈 [3. HPA Auto-scaling Pods](#step-3)
- 🚀 [4. GitLab CI/CD Pipeline](#step-4)
- 📊 [5. Monitoring Dashboard](#step-5)
- 🌐 [6. Live Web Demo Interface](#step-6)
- 🔄 [7. Self-healing Verification](#step-7)
- ⚠️ [Troubleshooting & Lessons Learned](#troubleshooting-lessons-learned)
- 🔮 [Production Gaps & Future Improvements](#future-production-improvements)
- 👤 [Author](#author)

</details>

---

<h2 id="introduction">📌 Introduction</h2>

This repository contains a complete GitOps implementation of a **2-node Kubernetes cluster** (Master + Worker) deployed on AWS EC2 using `kubeadm`. 

The project demonstrates robust DevOps patterns in a self-managed cluster, including **Horizontal Pod Autoscaling (HPA)** triggered by CPU load, **Self-healing infrastructure** during worker node maintenance, a fully automated **GitLab CI/CD pipeline** (build & push to Container Registry with manual deployment gating), secure ingress routing via **HTTPS/TLS** (cert-manager & Let's Encrypt), and full-stack observability with **Prometheus & Grafana**.

---

<h2 id="key-features">🚀 Key Features</h2>

*   🛡️ **Custom Domain & TLS Ingress Routing**: Dynamic traffic routing using a custom domain (`app.yourdomain.com` and `grafana.yourdomain.com`) with automated SSL/TLS termination via `cert-manager` and Let's Encrypt.
*   ⚖️ **Dynamic Auto-Scaling**: Horizontal Pod Autoscaler (HPA) dynamically scales Flask app instances between 1 and 5 replicas based on real-time CPU utilization metrics.
*   🔄 **Infrastructure Self-Healing**: Zero-downtime node drain (`cordon`/`drain`) demo where Pods are automatically evicted and rescheduled on healthy nodes.
*   🚀 **GitOps-driven CI/CD**: Automatic Docker image builds on code changes, pushed to GitLab Registry and deployed to Kubernetes with manual approval gates.
*   📊 **Observability Stack**: Real-time cluster metrics collection and visualization using Helm-deployed Prometheus Operator and Grafana.

---

<h2 id="architecture-overview">🏗️ Architecture Overview</h2>

```mermaid
flowchart TB
    User(["👤 Users"])
    Developer(["👨‍💻 Developer"])

    subgraph K8s["☸️ Kubernetes Cluster (kubeadm — 2 nodes: Master + Worker)"]
        direction TB

        subgraph IngressLayer["🌐 Ingress Layer"]
            Ingress["NGINX Ingress Controller
            (hostPort 80/443)"]
            CertManager["cert-manager
            + Let's Encrypt"]
        end

        Service["ClusterIP Service"]

        subgraph Deployment["📦 Deployment"]
            Pod1["Flask Pod"]
            Pod2["Flask Pod"]
            Pod3["Flask Pod"]
        end

        HPA["⚖️ Horizontal Pod
        Autoscaler"]
        MetricsServer["📊 metrics-server"]

        subgraph Monitoring["📈 Monitoring Stack"]
            Prom["Prometheus"]
            Grafana["Grafana"]
        end

        Runner["🏃 GitLab Runner
        (shell executor)"]
    end

    GitLab["📁 GitLab Repository"]
    Pipeline["🔄 GitLab CI/CD
    Pipeline (.gitlab-ci.yml)"]
    Registry["🐳 Container Registry"]

    User -->|"HTTPS
    app.domain.com"| Ingress
    CertManager -.->|"issues TLS cert"| Ingress
    Ingress --> Service
    Service --> Pod1
    Service --> Pod2
    Service --> Pod3

    MetricsServer -.->|"CPU/Memory"| HPA
    HPA -.->|"scale 1↔5"| Deployment

    Pod1 & Pod2 & Pod3 --> Prom
    Prom --> Grafana

    Developer -->|"git push"| GitLab
    GitLab -->|"trigger"| Pipeline
    Pipeline -->|"runs job"| Runner
    Runner -->|"1. build & push"| Registry
    Runner -->|"2. kubectl set image
    (manual approve)"| Deployment
    Deployment -->|"pull image"| Registry

    classDef userStyle fill:#FFE0B2,stroke:#E65100,stroke-width:2px,color:#000,font-weight:bold
    classDef trafficStyle fill:#BBDEFB,stroke:#1565C0,stroke-width:2px,color:#000
    classDef podStyle fill:#C8E6C9,stroke:#2E7D32,stroke-width:2px,color:#000
    classDef controlStyle fill:#E1BEE7,stroke:#6A1B9A,stroke-width:2px,color:#000
    classDef monitorStyle fill:#FFF9C4,stroke:#F57F17,stroke-width:2px,color:#000
    classDef cicdStyle fill:#FFCCBC,stroke:#BF360C,stroke-width:2px,color:#000
    classDef runnerStyle fill:#F8BBD0,stroke:#AD1457,stroke-width:2px,color:#000

    class User,Developer userStyle
    class Ingress,CertManager,Service trafficStyle
    class Pod1,Pod2,Pod3 podStyle
    class HPA,MetricsServer controlStyle
    class Prom,Grafana monitorStyle
    class GitLab,Pipeline,Registry cicdStyle
    class Runner runnerStyle

    style K8s fill:#F1F8E9,stroke:#558B2F,stroke-width:3px
    style IngressLayer fill:#E3F2FD,stroke:#1976D2,stroke-width:1.5px
    style Deployment fill:#E8F5E9,stroke:#43A047,stroke-width:1.5px
    style Monitoring fill:#FFFDE7,stroke:#FBC02D,stroke-width:1.5px
```

---

<h2 id="project-structure">📁 Project Structure</h2>

```text
loadtest-api/
├── .gitlab-ci.yml          # GitLab CI/CD Pipeline pipeline stages (build/deploy)
├── app.py                  # Flask API containing CPU-heavy Fibonacci endpoints
├── Dockerfile              # Optimized multi-stage container image build
├── docker-compose.yml      # Local development and container testing stack
├── loadtest.js            # k6 JavaScript load testing target scenario
├── requirements.txt        # Python dependency manifest
├── k8s/                    # Kubernetes declarative manifests
│   ├── deployment.yaml     # Application deployment and ClusterIP service definitions
│   ├── hpa.yaml            # Horizontal Pod Autoscaler configuration parameters
│   └── ingress.yaml        # Nginx Ingress resource routing with SSL annotations
└── templates/
    └── index.html          # Web dashboard displaying local metric charts via Chart.js
```

---

<h2 id="technologies-used">🛠️ Technologies Used</h2>

| Component | Technology / Badge | Description |
|---|---|---|
| **Cloud Provider** | ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white) | EC2 infrastructure (t3.medium instances) hosting the Kubernetes cluster |
| **Orchestration** | ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) | Cluster bootstrapped via `kubeadm`, CNI powered by Calico |
| **Container Engine** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Application builds packaged via Docker multi-stage Dockerfiles |
| **Package Management** | ![Helm](https://img.shields.io/badge/Helm-0F1626?style=flat-square&logo=helm&logoColor=white) | Helm charts used for deploying Ingress and the Prometheus Stack |
| **Ingress Controller** | ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white) | Nginx Ingress handling external traffic on host ports 80/443 |
| **SSL/TLS Certificates** | ![Let's Encrypt](https://img.shields.io/badge/Let's_Encrypt-003A70?style=flat-square&logo=letsencrypt&logoColor=white) | Managed TLS cert renewal via `cert-manager` HTTP-01 challenges |
| **Monitoring** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) | `kube-prometheus-stack` scrapes metrics across the cluster |
| **Visualization** | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white) | Custom Grafana dashboards displaying Node, Pod, and App metrics |
| **CI/CD / GitOps** | ![GitLab](https://img.shields.io/badge/GitLab-FC6D26?style=flat-square&logo=gitlab&logoColor=white) | CI/CD pipelines leveraging a custom GitLab shell-executor runner |
| **Load Testing** | ![k6](https://img.shields.io/badge/k6-7B62FF?style=flat-square&logo=k6&logoColor=white) | Distributed CPU load testing using JavaScript scenarios |
| **Demo Application** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white) | Lightweight Flask API calculating CPU-intensive Fibonacci numbers |

---

<h2 id="demo-videos">🎬 Demo Videos</h2>

Click on the cards below to view the video demonstrations on YouTube:

| 📈 HPA Auto-scaling Demo | 🔄 Self-healing (Cordon/Drain) Demo |
| :---: | :---: |
| [![HPA Auto-scaling Demo](https://img.youtube.com/vi/vFYXPUYhfiA/0.jpg)](https://youtu.be/vFYXPUYhfiA) | [![Self-healing Demo](https://img.youtube.com/vi/7viwdsLyjOA/0.jpg)](https://youtu.be/7viwdsLyjOA) |

---

<h2 id="aws-infrastructure-setup">☁️ AWS Infrastructure & Kubernetes Bootstrapping</h2>

Before deploying the Kubernetes manifests, the underlying infrastructure must be provisioned on AWS, and the Kubernetes cluster bootstrapped using `kubeadm`.

### 1. AWS EC2 Instance Provisioning
Create 2 EC2 Instances with the following configuration:
* **AMI**: Ubuntu Server 22.04 LTS
* **Instance Type**: `t3.medium` (Minimum requirement: 2 vCPUs, 4GB RAM)
* **Storage**: 20-30 GB gp3
* **Names**: `k8s-master` and `k8s-worker`
* **Key Pair**: `k8s-lab-key.pem`

### 2. Security Group Configuration (`k8s-lab-sg`)
Create a security group and attach it to both instances with the following inbound rules:
* SSH (Port `22`) -> `My IP` (for management access)
* HTTP (Port `80`) -> `0.0.0.0/0` (for web traffic & Let's Encrypt validation)
* HTTPS (Port `443`) -> `0.0.0.0/0` (for secure web traffic)
* K8s API Server (Port `6443`) -> `k8s-lab-sg` (self-referencing)
* etcd (Ports `2379-2380`) -> `k8s-lab-sg`
* Kubelet/Control Plane (Ports `10250-10252`) -> `k8s-lab-sg`
* NodePort Range (Ports `30000-32767`) -> `My IP` (optional, for debugging)

### 3. Kubernetes Cluster Bootstrap
1. **Prepare Nodes**: Run the pre-requisite script (disabling swap, configuring sysctl, installing `containerd` and Kubernetes packages `kubeadm`, `kubelet`, `kubectl`) on **both** master and worker nodes.
2. **Initialize Master Node**:
   ```bash
   sudo kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-advertise-address=<MASTER_PRIVATE_IP>
   ```
3. **Configure kubectl on Master**:
   ```bash
   mkdir -p $HOME/.kube
   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
   sudo chown $(id -u):$(id -g) $HOME/.kube/config
   ```
4. **Deploy Pod Network (Calico)**:
   ```bash
   kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/tigera-operator.yaml
   kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.28.0/manifests/custom-resources.yaml
   ```
5. **Join Worker Node**: Run the `kubeadm join` command generated by `kubeadm init` on the worker node.

---

<h2 id="quick-start">💻 Quick Start</h2>

### Prerequisites
* Kubernetes Cluster (v1.24+)
* `kubectl` configured on your local machine
* `k6` installed locally for stress testing

### Step 1: Deploy Manifests
Deploy the core application stack, including Ingress, Service, Deployment, and HPA:
```bash
kubectl apply -f k8s/
```

### Step 2: Trigger Stress Test (Local Machine)
Run the load test to trigger the HPA scaling mechanism:
```bash
k6 run loadtest.js
```

### Step 3: Monitor Scaling
Observe the HPA status and pod scaling in real time:
```bash
kubectl get hpa loadtest-hpa -w
```

---

<h2 id="step-1">✅ 1. 2-Node Cluster Status</h2>

Verify that both nodes are successfully bootstrapped and in `Ready` state:

![Nodes Ready](nodes-ready.png.png)

<h2 id="step-2">🔒 2. Custom Domain & Valid HTTPS Certificate</h2>

The cluster exposes services securely over the public internet using custom domains pointing to the ingress controller:
*   **Flask Web App**: `https://app.yourdomain.com`
*   **Grafana Dashboards**: `https://grafana.yourdomain.com`

SSL/TLS certificates are automatically provisioned, validated and renewed by `cert-manager` using Let's Encrypt HTTP-01 challenges. Verify the certificate status:

![Certificate Ready](certificate-ready.png)

<h2 id="step-3">📈 3. HPA Auto-scaling Pods</h2>

Watch the pods scaling dynamically as the CPU metrics hit the target threshold:

![HPA Scaling](hpa-scaling.png)

<h2 id="step-4">🚀 4. GitLab CI/CD Pipeline</h2>

The continuous integration pipeline automates Docker builds, Registry push and rolling update triggers:

![Pipeline Passed](pipeline-passed.png)

<h2 id="step-5">📊 5. Monitoring Dashboard</h2>

Visualize resource metrics and CPU load metrics via Grafana dashboards:

![Grafana Dashboard](grafana-dashboard.png)

<h2 id="step-6">🌐 6. Live Web Demo Interface</h2>

The live user interface features real-time performance graphs powered by Chart.js:

![Web Demo](web-demo.png)

<h2 id="step-7">🔄 7. Self-healing Verification</h2>

1. **Isolate the worker node** (prevent scheduling new pods onto it):
   ```bash
   kubectl cordon k8s-worker
   ```
   ![node cordon](node-cordon.png)

2. **Evict all running pods** off the worker node, rescheduling them on the master:
   ```bash
   kubectl drain k8s-worker --ignore-daemonsets --delete-emptydir-data --force
   ```
   ![pod drain](pod-drain.png)

3. **Restore the worker node** back to service after operations are completed:
   ```bash
   kubectl uncordon k8s-worker
   ```
   ![node uncordon](node-uncordon.png)

---

<h2 id="troubleshooting-lessons-learned">⚠️ Troubleshooting & Lessons Learned</h2>

Building and running a self-managed cluster introduces several real-world deployment challenges. Below are the key issues identified and resolved during this deployment:

### 1. Hardware Instability (`t3.micro` vs `t3.medium`)
*   **Problem**: Nodes randomly entered the `NotReady` state under high CPU stress testing. Kubelet stopped posting node status.
*   **Root Cause**: Bootstrapping a `kubeadm` cluster requires a minimum of 2 vCPUs and 2GB RAM. Using AWS `t3.micro` instances caused CPU credit depletion, leading to severe hypervisor throttling and system freeze.
*   **Fix**: Upgraded both Master and Worker node EC2 instances to `t3.medium` (2 vCPUs, 4GB RAM), eliminating system freezes under stress.

### 2. Private Container Registry Authentication (`ImagePullBackOff`)
*   **Problem**: Kubernetes Pods failed to download the application image with the error `ImagePullBackOff`.
*   **Root Cause**: The GitLab Container Registry containing the built images was set to Private, blocking Kubernetes' pull requests.
*   **Fix**: Generated a GitLab Personal Access Token, registered it as a Kubernetes Registry Secret and configured the deployment YAML with the corresponding `imagePullSecrets` manifest configuration:
    ```yaml
    spec:
      imagePullSecrets:
      - name: gitlab-registry-secret
    ```

### 3. Orphan Namespace Deletion Stack (`Terminating`)
*   **Problem**: Deleting namespaces (e.g., `monitoring`) caused the namespace to hang indefinitely in the `Terminating` state.
*   **Root Cause**: The deletion process was blocked by custom finalizers of CRDs whose controllers were already uninstalled.
*   **Fix**: Patched the finalizers array of the namespace resource to empty `[]` using direct Kubernetes API proxy calls:
    ```bash
    kubectl get namespace monitoring -o json | jq '.spec.finalizers = []' > ns.json
    kubectl replace --raw "/api/v1/namespaces/monitoring/finalize" -f ns.json
    ```

---

<h2 id="future-production-improvements">🔮 Production Gaps & Future Improvements</h2>

This project was built for educational and portfolio demonstration purposes. In a real-world production system, the following practices should be introduced:

- **Control Plane High Availability**: Implement a multi-master control plane using a load balancer to eliminate single points of failure.
- **Automated Backups**: Schedule regular snapshot backups of the `etcd` datastore using tools like `etcdctl` or Velero.
- **Resource Constraints Tuning**: Continuously profile resource requests/limits using Grafana historical data to prevent OOM errors or wasteful over-provisioning.
- **Network Policies & RBAC**: Apply fine-grained Namespace Isolation policies and Kubernetes RBAC permissions to enforce the principle of least privilege.
- **Secret Management Integration**: Replace default Base64 K8s Secrets with a secure external manager like HashiCorp Vault, AWS Secrets Manager or Sealed Secrets.
- **Multi-AZ Worker Allocation**: Ensure worker nodes are spread across multiple Availability Zones (AZs) for physical hardware redundancy.

---

<h2 id="author">👤 Author</h2>

**Doan Minh Hiep**

*   **GitHub**: [@minhhiep05](https://github.com/minhhiep05)
*   **GitLab**: [@doanhiep169](https://gitlab.com/doanhiep169)
*   **Email**: [doanhiep169@gmail.com](mailto:doanhiep169@gmail.com)
