# docker-tor-api
Sets up a docker container running a Flask hello world API reachable through TOR

If any errors occur and a redo is necessary, run the following command to remove all traces of “flask”:
```
docker image rm flask && docker rmi --force $(docker images -f "dangling=true" -q --no-trunc)
```
Run this command to build the container out of current working directory and tag it as “flask”:
```
docker build --rm --file Dockerfile -t flask . 
```
Copy the onion address and private key from the Build output for user authentication in browser:
```
<onion address - .onion extension>:descriptor:x25519:<COPY THE STRING LOCATED HERE>
```
Run the following commands in the container:
```
cat /var/lib/tor/hidden_service/hostname && cat /tmp/torkey.auth_private && systemctl restart tor && service tor restart && python3 main.py
```

