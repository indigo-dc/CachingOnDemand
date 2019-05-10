# On-Demand XCache cluster

## What's XCache

You can look at the [official XrootD documentation](http://xrootd.org/docs.html) for detailed information about the tool:

* [basic configuration](http://xrootd.org/doc/dev47/xrd_config.htm)
* [cmsd configuration](http://xrootd.org/doc/dev45/cms_config.htm)
* [proxy file cache](http://xrootd.org/doc/dev47/pss_config.htm)

## XCache components

Please find an overview description of the architecture in [this presentation](https://github.com/Cloud-PG/CachingOnDemand/blob/master/docs/XDC-AH_%20Distributed%20cache%20with%20XRootD.pdf)

## Ansible deployment

### Requirements

* Ansible 2.4
* OS: Centos7
* valid CMS /etc/vomses
* Port: one open service port
* Valid grid host certifate
* Valid service certificate that is able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

### Role Variables

``` yaml
BLOCK_SIZE: 512k # size of the file block used by the cache
CACHE_LOG_LEVEL: info # server log level
CACHE_PATH: /data/xrd # folder for cached files
CACHE_RAM_GB: 12 # amount of RAM for caching in GB. Suggested ~50% of the total
HI_WM: "0.9" # higher watermark of used fs space
LOW_WM: "0.8" # lower watermark of used fs space
N_PREFETCH: "0" # number of blocks to be prefetched
ORIGIN_HOST: origin # hostname or ip adrr of the origin server
ORIGIN_XRD_PORT: "1094" # xrootd port to contact origin on
REDIR_HOST: xcache-service # hostname or ip adrr of the cache redirector
REDIR_CMSD_PORT: "31213" # cmsd port of the cache redirector
metricbeat_polltime: 60s # polling time of the metricbeat sensor
metric_sitename: changeme # sitename to be displayed for monitoring
elk_endpoint: localhost:9000 # elasticsearch endpoint url
elastic_username: dodas # elasticsearch username
elastic_password: testpass # elasticsearch password
```

### Example Playbook

```yaml
---
- hosts: localhost
  remote_user: root
  roles:
    - role: dciangot.xcache 
```

### Deployment example: CMS XCache

[https://xcache.readthedocs.io/en/latest/automated-grid.html](https://xcache.readthedocs.io/en/latest/automated-grid.html)

## Deployment with Docker

[https://hub.docker.com/r/cloudpg/xrootd-proxy/](https://hub.docker.com/r/cloudpg/xrootd-proxy/)

### On-demand XCache docker image

Please find the Dockerfile in this repository [here](https://github.com/Cloud-PG/CachingOnDemand/blob/master/docker/Dockerfile)

To personalize and build your own image, just apply you changes in the Dockerfile and run:

``` bash
docker build . -t my_image
```

### Deploy a cluster with docker compose

If you want to try a demo deployment with docker compose, you can do it with the compose file [here](https://github.com/Cloud-PG/CachingOnDemand/blob/master/docker/docker-compose.yml)

## Deployment on Kubernetes

### Components recipe

Please take a look at the demonstration presented [here](https://cloud-pg.github.io/XDC-AH-demo). That will guide you through a step by step deployment of a cache cluster in K8s.

### Deployment with Helm

```bash
helm init --upgrade
helm repo add  cloudpg https://dodas-ts.github.io/docker-img_cms/
helm repo update
helm install cloudpg/cachingondemand
```

## TOSCA description files for PaaS orchestration

- [Kubernetes cluster](https://github.com/Cloud-PG/CachingOnDemand/blob/master/toscaTemplates/DODAS-TS/kube_deploy.yml)
  - [Kubernetes deployment charts](https://github.com/Cloud-PG/CachingOnDemand/tree/master/toscaTemplates/k8s)
- [Real case example: TOSCA template for XCache in CMS experiment with Marathon](https://github.com/Cloud-PG/CachingOnDemand/blob/master/toscaTemplates/DODAS-TS/cms_marathon_cluster.yml)

