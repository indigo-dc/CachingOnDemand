# Step by step deployment on bare metal: CMS XCache

## Cache server standalone installation

### Requirements

* OS: Centos7
* Port: one open service port
* Valid CMS /etc/vomses files
* Valid grid host certifate
* Valid service certificate that is able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

### Packages and CAs installation

Create and execute the following script (we are going to install the 4.8.3 version for testing purpose, but consider also the 4.9 and 4.10 as they include new feature and fix):

```bash
#!/bin/bash
XRD_VERSION=4.8.3-1.el7

echo "LC_ALL=C" >> /etc/environment \
    && echo "LANGUAGE=C" >> /etc/environment \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install wget \
    && yum clean all

cd /etc/yum.repos.d
wget http://repository.egi.eu/community/software/preview.repository/2.0/releases/repofiles/centos-7-x86_64.repo \
    && wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo
yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat \
    && yum clean all

yum install -y ca-policy-egi-core ca-policy-lcg
/usr/sbin/fetch-crl -q

yum install xrootd-server-$VERSION

mkdir -p /etc/grid-security/xrd/

chown -R xrootd:xrootd /etc/grid-security/xrd/

systemctl enable fetch-crl-cron
systemctl start fetch-crl-cron

curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-6.2.4-x86_64.rpm
sudo rpm -vi metricbeat-6.2.4-x86_64.rpm
```

### Proxy Renewal service

In order to keep the service proxy valid a simple service che be created on the machine.
First create a service file (e.g. `/usr/lib/systemd/system/xrootd-renew-proxy.service`):

```bash
[Unit]
Description=Renew xrootd proxy

[Service]
User=xrootd
Group=xrootd
Type = oneshot
ExecStart = /bin/voms-proxy-init --cert /etc/grid-security/xrd/cert/cert.pem --key /etc/grid-security/xrd/cert/key.pem -voms cms -valid 48:00

[Install]
WantedBy=multi-user.target
```

Then a timer service is required to manage the frequency of the proxy renewal (`/usr/lib/systemd/system/xrootd-renew-proxy.timer`):

```bash
[Unit]
Description=Renew proxy every day at midnight

[Timer]
OnCalendar=*-*-* 00:00:00
Unit=xrootd-renew-proxy.service

[Install]
WantedBy=multi-user.target
```

At this point you can start and reload the services with:

```bash
systemctl start xrootd-renew-proxy.timer
systemctl daemon-reload
```

### XRootD server configuration

The reference guide for the configuration is the official one [here](http://xrootd.org/doc/dev47/pss_config.htm). For the version 4.9 or newer please refer to the recomended ones [here](http://xrootd.org/docs.html)

What follows is a working point used and tested at different sites, its purpose is to show the main knobs available and how to threat them.
Create a configuration file (e.g. `/etc/xrootd/xrootd-xcache.cfg`)

```bash
# xrd and cmsd process ports
set xrdport=1094
set cmsdport=1213

# cache redirector address
set rdtrCache=0.0.0.0
set rdtrPortCmsd=cmsdport

# address and port of the origin servers
set rdtrGlobal=xrootd-cms.infn.it
set rdtrGlobalPort=1094

# disk occupation water marks
set cacheLowWm=0.80
set cacheHiWm=0.90

# log level for cache processes
set cacheLogLevel=info

# path to folder for storing data, NB it has to be owned by xrootd user
set cachePath=/data/xrd

# ram dedicated to cache (in GB), <=50% of the total is suggested
set cacheRam=16


all.manager $rdtrCache:$rdtrPortCmsd

# logging level for all the different activities
xrootd.trace info
ofs.trace info
xrd.trace info
cms.trace info
sec.trace info
pfc.trace $cacheLogLevel

if exec cmsd

# if the process is the cluster manager, just run in on the chosen port

all.role server
xrd.port $cmsdport

all.export / stage
oss.localroot $cachePath

else

# if the process is the xrd one, configure and start the cache service at the specified port

xrd.port $xrdport

##### GENERAL CONFIGURATION ######

# manage the work directory
all.export /
all.role  server
oss.localroot $cachePath

oss.space meta $cachePath/
oss.space data $cachePath/
pfc.spaces data meta

# in the system is overloaded fallback to remote read
xrootd.fsoverload redirect xrootd-cms.infn.it:1094

# For xrootd, load the proxy plugin and the disk caching plugin.
ofs.osslib   libXrdPss.so
pss.cachelib libXrdFileCache.so

# indicate the origin
pss.origin $rdtrGlobal:$rdtrGlobalPort

##### SECURITY CONFIGURATION ######
xrootd.seclib /usr/lib64/libXrdSec.so

# use gsi as client-cache authN method
sec.protocol /usr/lib64 gsi \
  -certdir:/etc/grid-security/certificates \
  -cert:/etc/grid-security/xrd/xrdcert.pem \
  -key:/etc/grid-security/xrd/xrdkey.pem \
  -d:3 \
  -crl:1

ofs.authorize 1
acc.audit deny grant

# use gsi user<-->namespace mapping file as client-cache authZ method
acc.authdb /etc/xrootd/Authfile-auth
sec.protbind * gsi


##### CACHE CONFIGURATION ######

pfc.diskusage $cacheLowWm $cacheHiWm
pfc.ram       ${cacheRam}g

# Tune the client timeouts to more aggressively timeout.
pss.setopt ParallelEvtLoop 10
pss.setopt RequestTimeout 25
pss.setopt ConnectTimeout 25
pss.setopt ConnectionRetry 2

# Standard values for streaming mode jobs
set cacheStreams=256
set prefetch=0
set blkSize=512k

pss.config streams $cacheStreams
pfc.blocksize   $blkSize
pfc.prefetch    $prefetch

fi
```

In addition for the authZ part, a file has to be created with the desired permission per user (e.g. `/etc/xrootd/Authfile-auth`):

```bash
# full permissions to all users for both /store/* paths and /*
u * /store/ a / a
```

### Start XCache deamons

The only thing left now is to start the respective deamons with:

``` bash
# enable and start xrootd server deamons
systemctl enable xrootd@xcache.service
systemctl enable cmsd@xcache.service

systemctl start xrootd@xcache.service
systemctl start cmsd@xcache.service
```

### Test the deployment

* to check if the daemons started correctly just use systemctl as below:

```bash
systemctl status xrootd@xcache.service
systemctl status cmsd@xcache.service
```

in case of problems logs can be found in `/var/log/xrootd/xcache`

* then you can try to copy a file from the origin:  

```text
xrdcp -f -v xroot://localhost:<xrdport defined in the configuration above>/<path to your file in origin>
```

* the expected outcome is something like:

```text
[root@xrootdcentostest centos]# xrdcp -f -v xroot://localhost:32294//store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/C85940F6-9596-E711-8FD6-D8D385FF1940.root /dev/null
[544MB/3.108GB][ 17%][========>                                         ][19.43MB/s]
```

* Finally you should be able to see your file on the cache disk on the path you indicated in the configuration.

## Redirector installation

The configuration for a cache redirector is really simple (e.g. `/etc/xrootd/xrootd-cacheredir.cfg`)

```bash
set rdtrcache=<redirector host>
set rdtrportcmsd=<redirector cluster manager port>
set rdtrportxrd=<redirector xrd port>

all.manager $rdtrcache:$rdtrportcmsd

# temporary fix for CMS multisource jobs - fixed probably by version 5
cms.sched  maxretries 0 nomultisrc

xrd.allow host *
xrd.port $rdtrportxrd
xrd.port $rdtrportcmsd if exec cmsd
all.export /store stage r/o
all.role manager
```

and then just start the daemons:

```bash
# enable and start xrootd redirector daemons
systemctl enable xrootd@cacheredir.service
systemctl enable cmsd@cacheredir.service

systemctl start xrootd@cacheredir.service
systemctl start cmsd@cacheredir.service
```

## Metricbeat installation

Create a metricbeat configuration file (e.g. `/etc/metricbeat/metricbeat.yml`):

```yaml
# You can find the full configuration reference here:
# https://www.elastic.co/guide/en/beats/metricbeat/index.html

#==========================  Modules configuration ============================
metricbeat.modules:

#------------------------------- System Module -------------------------------
- module: system
  metricsets:
    # CPU stats
    - cpu

    # System Load stats
    - load

    # Per CPU core stats
    - core

    # IO stats
    - diskio

    # Per filesystem stats
    - filesystem

    # File system summary stats
    - fsstat

    # Memory stats
    - memory

    # Network stats
    - network

    # Per process stats
    - process

    # Sockets (linux only)
    #- socket
  enabled: true
  period: 60s
  processes: ['.*']


#================================ General =====================================

# The name of the shipper that publishes the network data. It can be used to group
# all the transactions sent by a single shipper in the web interface.
name: 'DUMMY: cache sitename'

#================================ Outputs =====================================

# Configure what outputs to use when sending the data collected by the beat.
# Multiple outputs may be used.

#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["DUMMY_esHost.com"]
  template.name: "metricbeat_slave"
  template.path: "metricbeat.template.json"
  template.overwrite: false

  # Optional protocol and basic auth credentials.
  protocol: "http"
  username: "dodas"
  password: "DUMMY"

#================================ Logging =====================================

# Sets log level. The default log level is info.
# Available log levels are: critical, error, warning, info, debug
#logging.level: debug
```

and then just start the daemon:

```bash
# enable and start metricbeat service
systemctl enable metricbeat.service
systemctl start metricbeat.service
```
