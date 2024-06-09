import click
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import os
from prettytable import PrettyTable

def load_kube_config():
    kubeconfig_path = os.getenv('KUBECONFIG', os.path.expanduser('~/.kube/config'))
    try:
        config.load_kube_config(config_file=kubeconfig_path)
        click.echo(f"Using kubeconfig file: {kubeconfig_path}")
    except FileNotFoundError:
        click.echo("Error: kubeconfig file not found. Please ensure you have the correct kubeconfig file and set the KUBECONFIG environment variable if necessary.", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Error loading kubeconfig: {str(e)}", err=True)
        exit(1)

def print_kubernetes_version():
    try:
        v1 = client.VersionApi()
        version_info = v1.get_code()
        click.echo(f"Target Kubernetes version: {version_info.git_version}")
    except ApiException as e:
        click.echo(f"Error fetching Kubernetes version: {str(e)}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        exit(1)

@click.group()
def cli():
    """Kubernetes CLI Tool"""
    load_kube_config()
    print_kubernetes_version()

@cli.command()
def ku():
    """List all Kubernetes pods that are not Running, Complete and any of the containers not in Ready state."""
    v1 = client.CoreV1Api()
    try:
        click.echo("Querying Kubernetes API for pods...")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        click.echo(f"Received {len(ret.items)} pods")

        if not ret.items:
            click.echo("No pods found.")
            return

        table = PrettyTable()
        table.field_names = ["NAMESPACE", "POD NAME", "READY", "STATUS", "RESTARTS", "IP", "NODE NAME", "NOMINATED NODE", "READINESS GATES"]
        table.align["NAMESPACE"] = "l"
        table.align["POD NAME"] = "l"
        table.align["IP"] = "l"
        table.align["NODE NAME"] = "l"
        
        found = False
        for i in ret.items:
            pod_phase = i.status.phase
            if pod_phase not in ["Running", "Succeeded"]:
                found = True
                ready_containers = sum(1 for cs in i.status.container_statuses if cs.ready)
                total_containers = len(i.status.container_statuses)
                restarts = sum(cs.restart_count for cs in i.status.container_statuses)
                table.add_row([i.metadata.namespace, i.metadata.name, f"{ready_containers}/{total_containers}", pod_phase, restarts, i.status.pod_ip, i.spec.node_name, i.status.nominated_node_name, i.spec.readiness_gates])
            else:
                for container in i.status.container_statuses:
                    if not container.ready:
                        found = True
                        ready_containers = sum(1 for cs in i.status.container_statuses if cs.ready)
                        total_containers = len(i.status.container_statuses)
                        restarts = sum(cs.restart_count for cs in i.status.container_statuses)
                        table.add_row([i.metadata.namespace, i.metadata.name, f"{ready_containers}/{total_containers}", pod_phase, restarts, i.status.pod_ip, i.spec.node_name, i.status.nominated_node_name, i.spec.readiness_gates])
        
        if found:
            click.echo(table)
        else:
            click.echo("No pods found that are not Running, Complete, or have containers not in Ready state.")
    except ApiException as e:
        click.echo(f"RBAC permission error: {str(e)}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        exit(1)

@cli.command()
def kn():
    """List all Kubernetes worker nodes and their details (same output as kubectl get nodes -o wide)."""
    v1 = client.CoreV1Api()
    try:
        click.echo("Querying Kubernetes API for nodes...")
        ret = v1.list_node(watch=False)
        click.echo(f"Received {len(ret.items)} nodes")

        if not ret.items:
            click.echo("No nodes found.")
            return

        table = PrettyTable()
        table.field_names = ["NAME", "STATUS", "AGE", "VERSION", "INTERNAL-IP", "OS-IMAGE", "KERNEL-VERSION", "CONTAINER-RUNTIME"]
        table.align["NAME"] = "l"
        table.align["INTERNAL-IP"] = "l"
        table.align["OS-IMAGE"] = "l"
        table.align["KERNEL-VERSION"] = "l"
        table.align["CONTAINER-RUNTIME"] = "l"
        
        for i in ret.items:
            status = next(cond.type for cond in i.status.conditions if cond.status == "True")
            internal_ip = next(addr.address for addr in i.status.addresses if addr.type == "InternalIP")
            creation_timestamp = str(i.metadata.creation_timestamp).replace("+00:00", "")
            table.add_row([i.metadata.name, status, creation_timestamp, i.status.node_info.kubelet_version, internal_ip, i.status.node_info.os_image, i.status.node_info.kernel_version, i.status.node_info.container_runtime_version])
        
        click.echo(table)
    except ApiException as e:
        click.echo(f"RBAC permission error: {str(e)}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        exit(1)

@cli.command()
def kp():
    """List all Kubernetes pods and their details (same output as kubectl get pods -o wide -A) across all namespaces."""
    v1 = client.CoreV1Api()
    try:
        click.echo("Querying Kubernetes API for pods...")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        click.echo(f"Received {len(ret.items)} pods")

        if not ret.items:
            click.echo("No pods found.")
            return

        table = PrettyTable()
        table.field_names = ["NAMESPACE", "POD NAME", "READY", "STATUS", "RESTARTS", "IP", "NODE NAME", "NOMINATED NODE", "READINESS GATES"]
        table.align["NAMESPACE"] = "l"
        table.align["POD NAME"] = "l"
        table.align["IP"] = "l"
        table.align["NODE NAME"] = "l"
        
        for i in ret.items:
            ready_containers = sum(1 for cs in i.status.container_statuses if cs.ready)
            total_containers = len(i.status.container_statuses)
            restarts = sum(cs.restart_count for cs in i.status.container_statuses)
            table.add_row([i.metadata.namespace, i.metadata.name, f"{ready_containers}/{total_containers}", i.status.phase, restarts, i.status.pod_ip, i.spec.node_name, i.status.nominated_node_name, i.spec.readiness_gates])
        
        click.echo(table)
    except ApiException as e:
        click.echo(f"RBAC permission error: {str(e)}", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        exit(1)

@cli.command()
@click.argument('podname')
@click.option('-n', '--namespace', default='default', help='Namespace of the pod')
def kpf(podname, namespace):
    """Port forward to a pod; example command: kpf podname -n namespace1"""
    print(f"Port forwarding to pod {podname} in namespace {namespace}")
    # Implement port forwarding logic here
    # Handle exceptions as necessary

@cli.command()
@click.argument('servicename')
@click.option('-n', '--namespace', default='default', help='Namespace of the service')
def kps(servicename, namespace):
    """Service forward to a service; example command: kps servicename -n namespace1"""
    print(f"Service forwarding to service {servicename} in namespace {namespace}")
    # Implement service forwarding logic here
    # Handle exceptions as necessary

@cli.command()
@click.argument('nodename')
def kd(nodename):
    """Drain node with --ignore-daemonsets, --delete-emptydir-data, and --chunk-size=500; example: kd worker-node-name"""
    print(f"Draining node {nodename} with --ignore-daemonsets, --delete-emptydir-data, and --chunk-size=500")
    # Implement drain logic here
    # Handle exceptions as necessary

if __name__ == '__main__':
    cli()
