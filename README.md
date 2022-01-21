# docker-tor-api
## Building from Dockerfile
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
cat /var/lib/tor/hidden_service/hostname 
cat authorized_clients/torkey.auth_private && rm authorized_clients/torkey.auth_private
systemctl restart tor && service tor restart
python3 main.py
```
or download script to run these commands:
```
wget https://raw.githubusercontent.com/Bski3/docker-tor-api/main/docker-tor-api/commands.sh
chmod +x commands.sh
sudo ./commands.sh
```

## Pulling and running from Docker repo
If you have an image pulled from my bski3/tor-flask-api Docker repo run these commands:
```
sudo python3 tor-auth-x25519-gen.py -d "$(sudo cat hostname)" -f authorized_clients/torkey
```
```
sudo systemctl restart tor
```
```
sudo service tor restart
```
```
cat /var/lib/tor/hidden_service/hostname
```
```
sudo cat /var/lib/tor/hidden_service/authorized_clients/torkey.auth_private
```
```
sudo rm /var/lib/tor/hidden_service/authorized_clients/torkey.auth_private
```
```
python3 main.py
```
