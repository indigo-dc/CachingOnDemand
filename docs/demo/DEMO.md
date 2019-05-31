# DEPLOY CACHINGONDEMAND STACK ON K8S

## REQUIREMENTS

For part 1:

- Docker
- Docker compose

For part 2:

- [k8s Docker in Docker](https://github.com/kubernetes-sigs/kubeadm-dind-cluster)
- remote xrootd host to connect to
- service certificate authorized to read from remote xrootd host
- voms configuration file (optional)

## PART 1

### START A LOCAL KUBERNETES CLUSTER

Let's start a k8s cluster locally with 4 nodes:

```bash
NUM_NODES=4 k8s-dind up
```

The output should be something like:

```text
* Bringing up coredns and kubernetes-dashboard 
deployment.extensions/coredns scaled
deployment.extensions/kubernetes-dashboard scaled
.............[done]
NAME          STATUS   ROLES    AGE     VERSION
kube-master   Ready    master   2m37s   v1.13.0
kube-node-1   Ready    <none>   116s    v1.13.0
kube-node-2   Ready    <none>   116s    v1.13.0
kube-node-3   Ready    <none>   116s    v1.13.0
kube-node-4   Ready    <none>   116s    v1.13.0
* Access dashboard at: http://127.0.0.1:32769/api/v1/namespaces/kube-system/services/kubernetes-dashboard:/proxy
```

and dashboard should be accessible at the prompted link.
Now your kube config file has been update so you should be able to query the cluster by:

```bash
kubectl get node
```

