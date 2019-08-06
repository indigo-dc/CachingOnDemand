# USAGE

## Available options

* `--nogsi`: avoid client server gsi auth
* `--nogrid`: avoid WLCG CAs installation
* `--health_port`: port for healthcheck process listening, type=int, default=80
* `--config`: specify xrootd config file

## Important container paths

* `/data/xrd/`: saved file location for both cache and std modes
* `/etc/xrootd/`: config files dir
* `/var/log/xrootd/cmsd.log`: log of cmsd service
* `/var/log/xrootd/xrootd.log`: log of xrootd service

## Running by hand

Just put your xrootd config file in $PWD/config:/etc/xrootd

```bash
# with your xrd_cache.conf on $PWD/config
sudo docker run --rm --privileged -p 32294:32294 -p 31113:31113 -v $PWD/config:/etc/xrootd cloudpg/cachingondemand --config /etc/xrootd/xrd_test.conf
```

* REMEMBER To expose the ports indicated in your config file. In the case of config/xrd_test.conf are: 32294, 31113

* File saved will be put on /data/xrd, so you may want to mount your storage backend there

An health check is available on:

```bash
# response 0 everything running, response 1 something went wrong
curl <container_ip>/check_health
```

In case of response 1, with `docker logs` you can see a log dump of the crashed daemon.

## Local stack deployment with docker compose: Origin+Cache+CacheRedirector

You need to first install [docker-compose](https://docs.docker.com/compose/install/#install-compose).
Then run use the docker-compose.yml file provided to bring up locally:

* an origin server with config in config/xrd_test_origin.conf
* a file cache server with config in config/xrd_test.conf
* a file cache redirector with config in config/xrd_test-redir.conf
* a [portainer](https://www.portainer.io/) webUI for quickly debug and move throught the containers (available on `localhost:9000` once deployed)

The command for bringing the full stack up is:

```bash
git clone https://github.com/Cloud-PG/cachingondemand.git
cd cachingondemand/docker
/usr/local/bin/docker-compose up -d
```

To shutdown the stack:

```bash
/usr/local/bin/docker-compose down
```

### First functional test

```bash
# Put a test file on the remote host
sudo docker exec -ti docker_client_1 sh -c "echo \"This is my file\" > test.txt & xrdcp test.txt root://docker_origin_1:1194//test.txt"
# Request that file from the cache redirector xrootd process 
# that is listening on 1094
sudo docker exec -ti docker_client_1 xrdcp -f -d3 root://docker_redirector_1//test.txt remote_test.txt
# If you find no error you can now check that the file is correctly cached on cache server
sudo docker exec -ti docker_cache_1 ls /data/xrd/
# you should see these two files: test.txt  test.txt.cinfo
```
