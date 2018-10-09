Role Name
=========

You can look at the [official XrootD documentation](http://xrootd.org/docs.html) for detailed information about the tool:

* [basic configuration](http://xrootd.org/doc/dev47/xrd_config.htm)
* [cmsd configuration](http://xrootd.org/doc/dev45/cms_config.htm)
* [proxy file cache](http://xrootd.org/doc/dev47/pss_config.htm)

Requirements
------------

* Ansible 2.4
* OS: Centos7
* valid CMS /etc/vomses
* Port: one open service port
* Valid grid host certifate
* Valid service certificate that is able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

Role Variables
--------------

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

Example Playbook
----------------

```yaml
---
- hosts: localhost
  remote_user: root
  roles:
    - role: dciangot.xcache 
```

Author Information
------------------

diego.ciangottini@cern.ch
