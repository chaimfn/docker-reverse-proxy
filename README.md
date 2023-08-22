# Intro:
Here is an example of reverse-proxy to some web-apps, all on docker. <br />
We running some apps as docker-containers without public ports, and publishing them by reverse-proxy (nginx), which is a docker-container too. <br />
The reverse-proxy is published as ssl (with self-signd-certificate), and so does each app behind it. <br />
Each app is published (by reverse-proxy) with its domain. And because of that, with its ssl-cert (self-signd). <br />
In the reverse-proxy config, the references to apps is based on the apps NAMES instead of apps IPs! <br />
It's makes the configuration easier. <br />
This is possible because of using private-network, see ```docker-compose.yaml``` file, first code-block.

# Steps:
### 1. Navigate to root of this project:
```cd docker-reverse-proxy```

### 2. Install:
```docker compose -p reverse_proxy up -d``` <br />
Expected: ```[+] Running 3/0```

### 3. Check:
We are going to check by 'curl'. <br />
But first, your OS must to know the domains we're using, and to know the public-certificate the nginx is published by. <br />
Therfor:

#### Add host:
Add this line to end of ```/etc/hosts``` file:

```127.0.0.1	localhost nginx.docker.local express.docker.local flask.docker.local```

#### Install SSL-Cert:
1. ```sudo cp ./nginx/etc/ssl/*.docker.local.crt /usr/local/share/ca-certificates/```
2. ```sudo update-ca-certificates```

Make shure one cert is updated.

#### Now - check:
##### First, by simple http:
1. ```curl http://nginx.docker.local:8880/```. Expected: the nginx-welcome-page.
2. ```curl http://express.docker.local:8880/```. Expected: ```hello express!```.
3. ```curl http://flask.docker.local:8880/```. Expected: ```hello flask!```.

##### Finally, by https:
Repeat the 3 tests above, but now with the ```https``` protocol (```4443```).

# Restart:
For now, when you restart your machine, all those containers will be stopped.<br />
You may test it by restart, and then ```docker ps``` or ```docker compose ls```. <br />
We're going to make them 'persistent'. <br />

### 1. Edit 'docker-compose' file:
Edit the ```docker-compose.yaml``` file. <br />
Uncomment lines ```12, 19 and 26```: ~~```#restart: unless-stopped```~~ -> ```restart: unless-stopped```.

### 2. Run once again:
```docker compose -p reverse_proxy up -d``` <br />

### 3. Restart your machine.

### 4. Check:
By docker compose: ```dokcer compose ls``` and ```docker compose -p reverse_proxy ps```<br />
or, natively: ```docker ps```.
