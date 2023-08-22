## How did those cert-files creared:
```
openssl req -x509 -sha256 -days 3560 -nodes -newkey rsa:2048 -subj "/CN=*.docker.local/C=IL/L=Jerusalem" -keyout *.docker.local.key -out *.docker.local.crt
```
