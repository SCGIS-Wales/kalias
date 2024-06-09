![release](https://github.com/SCGIS-Wales/kalias/actions/workflows/release.yml/badge.svg)


# Kubernetes CLI Aliases for Python

This Python package provides native Kubernetes CLI aliases, allowing users to manage and query Kubernetes resources directly from Python without using `kubectl`.

## Installation

```bash
pip install k8s-cli
```

## Usage

```
ku         # List all Kubernetes pods that are not Running, Complete and any of the containers not in Ready state.
kn         # List all K8S worker nodes and their details (same output as kubectl get nodes -o wide).
kp         # List all K8S pods and their details (same output as kubectl get pods -o wide -A) across all namespaces.
kpf        # Port forward to a pod; example command: kpf podname -n namespace1
kps        # Service forward to a service; example command: kps servicename -n namespace1
kd         # Drain node with --ignore-daemonsets, --delete-emptydir-data, and --chunk-size=500; example: kd worker-node-name
```

## Example output


- all unhealthy pods with a single command

```
ku
Target Kubernetes version: v1.29.2
+-------------+--------------------------------+-------+---------+----------+-------------+-------------+----------------+-----------------+
| NAMESPACE   | POD NAME                       | READY |  STATUS | RESTARTS | IP          | NODE NAME   | NOMINATED NODE | READINESS GATES |
+-------------+--------------------------------+-------+---------+----------+-------------+-------------+----------------+-----------------+
| default     | nginx-7854ff8877-dczdq         |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
| default     | nginx-7854ff8877-fcpjq         |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
| default     | nginx-7854ff8877-p6fgz         |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
| default     | nginx-7854ff8877-q2pf8         |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
| kube-system | metrics-server-98bc7f888-mqcfx |  0/1  | Running |    0     | 10.244.1.45 | kind-worker |      None      |       None      |
| namespace2  | nginx-replicaset-2-2-dbqpf     |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
| namespace2  | nginx-replicaset-2-2-dxpwr     |  0/1  | Pending |    0     | None        | kind-worker |      None      |       None      |
+-------------+--------------------------------+-------+---------+----------+-------------+-------------+----------------+-----------------+
```

- all Kubernetes worker nodes with details

```
kn
Target Kubernetes version: v1.29.2
+--------------------+--------+---------------------+---------+-------------+--------------------------------+-----------------+---------------------+
| NAME               | STATUS |         AGE         | VERSION | INTERNAL-IP | OS-IMAGE                       | KERNEL-VERSION  | CONTAINER-RUNTIME   |
+--------------------+--------+---------------------+---------+-------------+--------------------------------+-----------------+---------------------+
| kind-control-plane | Ready  | 2024-03-23 17:25:55 | v1.29.2 | 172.18.0.2  | Debian GNU/Linux 12 (bookworm) | 6.6.22-linuxkit | containerd://1.7.13 |
| kind-worker        | Ready  | 2024-03-23 17:26:13 | v1.29.2 | 172.18.0.3  | Debian GNU/Linux 12 (bookworm) | 6.6.22-linuxkit | containerd://1.7.13 |
+--------------------+--------+---------------------+---------+-------------+--------------------------------+-----------------+---------------------+
```

- all pods across all Kubernetes namespaces

```
kp
Target Kubernetes version: v1.29.2
+--------------------+--------------------------------------------+-------+---------+----------+-------------+--------------------+----------------+-----------------+
| NAMESPACE          | POD NAME                                   | READY |  STATUS | RESTARTS | IP          | NODE NAME          | NOMINATED NODE | READINESS GATES |
+--------------------+--------------------------------------------+-------+---------+----------+-------------+--------------------+----------------+-----------------+
| default            | nginx-7854ff8877-66mt2                     |  1/1  | Running |    0     | 10.244.1.23 | kind-worker        |      None      |       None      |
| default            | nginx-7854ff8877-6zf5v                     |  1/1  | Running |    0     | 10.244.1.21 | kind-worker        |      None      |       None      |
| default            | nginx-7854ff8877-bm4zw                     |  1/1  | Running |    0     | 10.244.1.24 | kind-worker        |      None      |       None      |
| default            | nginx-7854ff8877-cv8zm                     |  1/1  | Running |    0     | 10.244.1.22 | kind-worker        |      None      |       None      |
| default            | nginx-7854ff8877-hrk8s                     |  1/1  | Running |    0     | 10.244.1.20 | kind-worker        |      None      |       None      |
| kube-system        | coredns-76f75df574-87hnn                   |  1/1  | Running |    0     | 10.244.1.27 | kind-worker        |      None      |       None      |
| kube-system        | coredns-76f75df574-dzpfx                   |  1/1  | Running |    0     | 10.244.1.25 | kind-worker        |      None      |       None      |
| kube-system        | etcd-kind-control-plane                    |  1/1  | Running |    1     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | kindnet-5r5lr                              |  1/1  | Running |    0     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | kindnet-g88vs                              |  1/1  | Running |    0     | 172.18.0.3  | kind-worker        |      None      |       None      |
| kube-system        | kube-apiserver-kind-control-plane          |  1/1  | Running |    1     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | kube-controller-manager-kind-control-plane |  1/1  | Running |    8     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | kube-proxy-67msl                           |  1/1  | Running |    0     | 172.18.0.3  | kind-worker        |      None      |       None      |
| kube-system        | kube-proxy-f95rg                           |  1/1  | Running |    0     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | kube-scheduler-kind-control-plane          |  1/1  | Running |    7     | 172.18.0.2  | kind-control-plane |      None      |       None      |
| kube-system        | metrics-server-98bc7f888-xg2j9             |  1/1  | Running |    0     | 10.244.1.26 | kind-worker        |      None      |       None      |
| local-path-storage | local-path-provisioner-7577fdbbfb-wnv88    |  1/1  | Running |    0     | 10.244.0.6  | kind-control-plane |      None      |       None      |
| namespace2         | nginx-replicaset-2-2-mxvsv                 |  1/1  | Running |    0     | 10.244.1.28 | kind-worker        |      None      |       None      |
| namespace2         | nginx-replicaset-2-2-r885r                 |  1/1  | Running |    0     | 10.244.1.29 | kind-worker        |      None      |       None      |
+--------------------+--------------------------------------------+-------+---------+----------+-------------+--------------------+----------------+-----------------+
```



### Step 3: Build and Upload to PyPi

Follow these steps to build and upload your package to PyPi:

1. Build the distribution package:

```bash
python setup.py sdist bdist_wheel
```

2. Upload the package to PyPi using twine:

```bash
pip install twine
twine upload dist/*
```

