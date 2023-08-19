# Intro:
Here is an example of reverse-proxy to some web-apps, all on docker.

We running some apps as docker-containers without public ports, and publishing them by reverse-proxy (nginx), which is a docker-container too.

The reverse-proxy is published as ssl (with self-signd-certificate), and so does each app behind it.

Each app is published (by reverse-proxy) with its domain. And because of that, with its ssl-cert (self-signd).

In the reverse-proxy config, the references to apps is based on the apps NAMES instead of apps IPs!

It's makes the configuration easier.

This is possible because of using private-network, as follows.


# Steps:

### Create private network:
docker network create docker-host-network


### Run some apps, without public ports, under the private network:
docker run --name express.docker.local --restart unless-stopped -d --net docker-host-network chaimfn/express-sample:1
docker run --name flask.docker.local --restart unless-stopped -d --net docker-host-network chaimfn/flask-sample:1


### Create self-signd-cert. 
#### (Here we creating a wildcard certificate, for easier use).
Created by this command:

```
openssl req -x509 -sha256 -days 3560 -nodes -newkey rsa:2048 -subj "/CN=*.docker.local/C=IL/L=Jerusalem" -keyout *.docker.local.key -out *.docker.local.crt
```

Those cert-files ('crt' and 'key') are saved in ```./nginx/etc/ssl/``` dir.

### Nginx reverse-proxy configuration:
See ```./nginx/conf.d/default.conf``` file.


### Run nginx reverse-proxy:
#### With 2 public ports (http and https), under the same private network. Cert-files and conf file are mounted as docker-volumes.
```
docker run --name host.docker.local --restart unless-stopped -d --net docker-host-network -p 80:80 -v $PWD/nginx-sample/conf.d:/etc/nginx/conf.d/ chaimfn/nginx:1.25.1.netfree
```

### Check:
We are going to check by 'curl'. But first, your OS must to know the domains we're using, and to know the public-certificate the nginx is published by. Therfor:

#### Hosts:
Add this line to end of ```/etc/hosts``` file:

```127.0.0.1	localhost host.docker.local express.docker.local flask.docker.local```

#### SSL-Cert:
1. ```cp ./nginx/etc/ssl/*.docker.local.crt /usr/local/share/ca-certificates/```
2. ```update-ca-certificates```

Make shure one cert is updated.

#### Now - check:
##### First, by simple http:
1. ```curl http://host.docker.local/```. Expected: the nginx-welcome-page.
2. ```curl http://express.docker.local/```. Expected: ```hello express!```.
3. ```curl http://flask.docker.local/```. Expected: ```hello flask!```.

##### Finally, by https:
Repeat the 3 check above, but now, with the ```https``` protocol.
