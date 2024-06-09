import unittest
from unittest.mock import patch, MagicMock
import click
from click.testing import CliRunner
import kalias.main as kalias

class TestKalias(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('kalias.main.config.load_kube_config')
    def test_load_kube_config(self, mock_load_kube_config):
        result = self.runner.invoke(kalias.cli, ['ku'])
        mock_load_kube_config.assert_called_once()
        self.assertIn("Using kubeconfig file", result.output)

    @patch('kalias.main.client.VersionApi.get_code')
    def test_print_kubernetes_version(self, mock_get_code):
        mock_get_code.return_value.git_version = "v1.20.0"
        result = self.runner.invoke(kalias.cli, ['ku'])
        self.assertIn("Target Kubernetes version: v1.20.0", result.output)

    @patch('kalias.main.client.CoreV1Api.list_pod_for_all_namespaces')
    def test_ku(self, mock_list_pod_for_all_namespaces):
        mock_list_pod_for_all_namespaces.return_value.items = []
        result = self.runner.invoke(kalias.cli, ['ku'])
        self.assertIn("Received 0 pods", result.output)
        self.assertIn("No pods found.", result.output)

    @patch('kalias.main.client.CoreV1Api.list_node')
    def test_kn(self, mock_list_node):
        mock_list_node.return_value.items = []
        result = self.runner.invoke(kalias.cli, ['kn'])
        self.assertIn("Received 0 nodes", result.output)
        self.assertIn("No nodes found.", result.output)

    @patch('kalias.main.client.CoreV1Api.list_pod_for_all_namespaces')
    def test_kp(self, mock_list_pod_for_all_namespaces):
        mock_list_pod_for_all_namespaces.return_value.items = []
        result = self.runner.invoke(kalias.cli, ['kp'])
        self.assertIn("Received 0 pods", result.output)
        self.assertIn("No pods found.", result.output)

    def test_kpf(self):
        result = self.runner.invoke(kalias.cli, ['kpf', 'mypod', '-n', 'mynamespace'])
        self.assertIn("Port forwarding to pod mypod in namespace mynamespace", result.output)

    def test_kps(self):
        result = self.runner.invoke(kalias.cli, ['kps', 'myservice', '-n', 'mynamespace'])
        self.assertIn("Service forwarding to service myservice in namespace mynamespace", result.output)

    def test_kd(self):
        result = self.runner.invoke(kalias.cli, ['kd', 'mynode'])
        self.assertIn("Draining node mynode with --ignore-daemonsets, --delete-emptydir-data, and --chunk-size=500", result.output)

if __name__ == '__main__':
    unittest.main()
