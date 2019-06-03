# DEPLOY CACHINGONDEMAND STACK WITH DODAS

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

For a introduction and a quickstart guide for DODAS please see the [documentation page]().
In this demo we will make use of the [IM python client]()

As first step make sure to clone the [TOSCA template repository]():

```bash
git clone ........
cd .....
```

Now this kind of deployment will automatize 2 macro steps:

1. creation of a K8s cluster with [Helm]()
2. installing with Helm the needed applications
3. configuring this application using a yaml file provided by the user

So let's take a look to the main feature of the TOSCA template and Helm configuration files.

### TOSCA TEMPLATE

### CachingOnDemand Helm values

### Prometheus Helm values

### Grafana Helm values

## CREATE SECRETS AND CONFIGMAPS



## TEST FUNCTIONALITIES

## MONITOR SYSTEM AND DUMMY DASHBOARD


# Future improvements