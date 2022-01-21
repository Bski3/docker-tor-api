#use OS:
FROM ubuntu:latest

LABEL maintainer="Github.com/Bski3"

#update:
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends apt-transport-https \
    lsb-release \
    build-essential \
    python3-pip \
    python3.8-venv \
    python3-dev \
    basez \
    systemctl \
    wget \
    sudo \
    tor \
    gnupg

#create and set user permissions:
RUN \
    groupadd -g 999 toruser && useradd -u 999 -g toruser -G sudo -m -s /bin/bash toruser && \
    sed -i /etc/sudoers -re 's/^%sudo.*/%sudo ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^root.*/root ALL=(ALL:ALL) NOPASSWD: ALL/g' && \
    sed -i /etc/sudoers -re 's/^#includedir.*/## **Removed the include directive** ##"/g' && \
    echo "toruser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "Customized the sudoers file for passwordless access to the toruser user!" && \
    echo "toruser user:";  su - toruser -c id

#install requirements with pip:
RUN sudo pip install flask
RUN sudo pip freeze > requirements.txt
RUN sudo pip install -r requirements.txt
RUN sudo pip install virtualenv pynacl

#key generation:
RUN sudo echo "deb [arch=amd64] https://deb.torproject.org/torproject.org $(lsb_release -sc) main" >> /etc/apt/sources.list.d/tor-project.list
RUN sudo gpg --keyserver keyserver.ubuntu.com --recv A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 && \
	sudo gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | \
	sudo apt-key add - && \
	apt update && \
	sudo apt-get install deb.torproject.org-keyring

#create hidden service webroot directory:
RUN sudo mkdir /var/lib/tor/hidden_service

#set ownership and permissions:
RUN sudo chown -R debian-tor:debian-tor /var/lib/tor/
RUN sudo find /var/lib/tor/hidden_service -type d | sudo xargs chmod u+rwx,go=

#set working directory:
WORKDIR /var/lib/tor/hidden_service

#download main.py Flask script and make it executable:
RUN wget https://github.com/Bski3/docker-tor-api/main.py
RUN sudo chmod +x main.py

#copy to the hidden service webroot directory:
COPY main.py /var/lib/tor/hidden_service

#create torrc settings file:
RUN sudo rm /etc/tor/torrc
RUN echo '\n\
HiddenServiceDir /var/lib/tor/hidden_service/\n\
HiddenServicePort 80 127.0.0.1:80'\
>> /etc/tor/torrc

#restart to activate torrc settings:
RUN sudo systemctl enable tor
RUN sudo systemctl restart tor
RUN sudo service tor restart

#generate tor authorization keys:
RUN sudo wget https://raw.githubusercontent.com/AnarchoTechNYC/ansible-role-tor/master/molecule/default/scripts/tor-auth-x25519-gen.py
RUN sudo chmod +x tor-auth-x25519-gen.py
RUN sudo python3 tor-auth-x25519-gen.py -d "$(sudo cat hostname)" -f authorized_clients/torkey

#set ownership and permissions for authorized_clients:
RUN sudo chown -R debian-tor:debian-tor /var/lib/tor/hidden_service/authorized_clients

#add authorized_clients directory to torrc settings file:
RUN echo 'ClientOnionAuthDir /var/lib/tor/hidden_service/authorized_clients/'\
>> /etc/tor/torrc

#restart to activate torrc settings:
RUN sudo systemctl restart tor
RUN sudo service tor restart

#create python virtual environment:
RUN sudo python3 -m venv virtualenv

#print onion address + keys during build and delete private key. Save it for reuse:
RUN echo “onion address:” && sudo cat /var/lib/tor/hidden_service/hostname
RUN echo “pub key:” && sudo cat /var/lib/tor/hidden_service/authorized_clients/torkey.auth
RUN echo “private key, deleting after print. Save it for reuse:” && sudo cat /var/lib/tor/hidden_service/authorized_clients/torkey.auth_private && sudo rm /var/lib/tor/hidden_service/authorized_clients/torkey.auth_private

#set user to start as:
#USER toruser

