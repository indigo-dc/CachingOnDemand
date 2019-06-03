# DEPLOY CACHINGONDEMAND STACK WITH DODAS

## What's DODAS

Please take a look at [this article](https://doi.org/10.22323/1.327.0024)

## Components

The following components will be intalled with the procedure presented below:

- __XCache server__:
  - GSI authentication for both client and remote storage
- __Cache federator__:
  - allowing dynamic cache server scaling
- __Proxy server__:
  - providing a tunnel between external client and cache servers on internal network.
- __Prometheus server and node exporters__:
  - providing basic knobs for a cluster monitoring
- __Grafana server__:
  - for visualization of dashboard starting from data stored by prometheus

## IM client and DODAS template

For a introduction and a quickstart guide for DODAS please see the [documentation page](https://dodas-ts.github.io/dodas-doc/).
In this demo we will make use of the [IM python client](https://imdocs.readthedocs.io/en/devel/client.html).

As first step make sure to clone the [TOSCA template repository](https://github.com/indigo-dc/tosca-templates/tree/k8s_cms/dodas):

```bash
git clone https://github.com/indigo-dc/tosca-templates
cd tosca-templates/dodas
git checkout k8s_cms
```

Now this kind of deployment will automatize 2 macro steps:

1. creation of a K8s cluster with [Helm](https://helm.sh/docs/using_helm/#installing-helm)
2. installing with Helm the needed applications
3. configuring this application using a yaml file provided by the user

So let's take a look to the main feature of the TOSCA template and Helm configuration files.

### TOSCA template

[Available on github](https://github.com/indigo-dc/tosca-templates/tree/k8s_cms/dodas/XCache-demo.yaml)


### CachingOnDemand Helm values

[Available on github](https://raw.githubusercontent.com/Cloud-PG/CachingOnDemand/master/helm/cachingondemand/values.yaml)

### Prometheus Helm values

[Available on github](https://raw.githubusercontent.com/indigo-dc/tosca-templates/k8s_cms/dodas/config/prom_values.yaml)

### Grafana Helm values

[Available on github](https://raw.githubusercontent.com/indigo-dc/tosca-templates/k8s_cms/dodas/config/grafana.yaml)


## Create a cluster with IM client

```bash
wget https://github.com/indigo-dc/tosca-templates/tree/k8s_cms/dodas/XCache-demo.yaml
im_client.py -a my_auth_file.dat create XCache-demo.yaml
```

## Create K8s secrets and configmaps

First log into the k8s master machine and copy there your certificates wherever you prefer e.g. 

## Test functionalities

## Monitor system and dummy grafana dashboard


# Future improvements