#!
clear
echo "installing python, pip, and requirements"
echo
echo
echo "If you did not move all the files to the VM, this script will not work"
echo
echo
echo "assuming you are using the home directory, a tmp folder will be created within the working directory"
echo
echo
export TMPDIR=/home/isaiasjasso/tmp/
sudo dnf install python3 -y
sudo dnf install python3-pip -y
sudo pip install -r requirements.txt -y
# python3 -m pip install openlit
echo
echo
echo is this an upgrade? yes or no?
read upgrade
echo
echo
echo "installing docker"
if [ $upgrade == "yes" ]

then
echo yum is an alias for the dnf utility.
        echo
        echo
        sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc
        echo
        echo
        echo setting up repo
        echo
        echo
sudo yum upgrade -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
        echo
        echo
        echo installing docker engine
        echo
        echo
        sudo yum upgrade -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        sudo systemctl start docker
        echo
        echo

else
echo yum is an alias for the dnf utility.
echo
echo
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc
echo
echo
echo setting up repo
echo
echo
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
echo
echo
echo installing docker engine
echo
echo
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
echo
echo
fi
echo
echo
echo "git clone the openlit repo and docker compose the openlit Dockerfile"
echo
echo
git clone https://github.com/openlit/openlit.git
echo
echo
cd openlit
echo
echo
docker compose up -d
echo
echo
echo "go to browser, url will be 127.0.0.1:3000"
echo
echo
echo "Login username is user@openlit.io and password is openlituser"
echo
echo
