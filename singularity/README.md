# Singularity container for XRootD proxy server

## Set up log directory

The log directory should have the correct permisions:

``` bash
sudo chown -R 998:996 /var/log/xrootd
```

## Start the service from local image

Build the image from github repo:

```bash
git clone https://github.com/Cloud-PG/CachingOnDemand_singularity.git
cd CachingOnDemand_singularity

sudo singularity build xrd_proxy.sif Singularity
```

Then start the service:

```bash
sudo REMOTE_HOST=XXX.XXX.XXX.XX PROXY_PORT=1124 REMOTE_PORT=31094 singularity instance start -B /var/log/xrootd/:/var/log/xrootd/ xrd_proxy.sif myproxy
```


## Start the service with SingularityHub image

Start the service with:

```bash
sudo REMOTE_HOST=XXX.XXX.XXX.XX PROXY_PORT=1124 REMOTE_PORT=31094 singularity instance start -B /var/log/xrootd/:/var/log/xrootd/ shub://Cloud-PG/CachingOnDemand_singularity:latest myproxy
```

