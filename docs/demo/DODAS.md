# DEPLOY CACHINGONDEMAND STACK WITH DODAS

## What's DODAS

Please take a look at [this article](https://doi.org/10.22323/1.327.0024)

## COMPONENTS

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

## IM CLIENT AND DODAS TEMPLATE

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

### TOSCA TEMPLATE

[Available on github](https://github.com/indigo-dc/tosca-templates/tree/k8s_cms/dodas/XCache-demo.yaml)

### CachingOnDemand Helm values

[Available on github]()

### Prometheus Helm values

[Available on github]()

### Grafana Helm values

[Available on github]()


## CREATE A CLUSTER WITH IM CLIENT


## CREATE SECRETS AND CONFIGMAPS



## TEST FUNCTIONALITIES

## MONITOR SYSTEM AND DUMMY DASHBOARD


# Future improvements