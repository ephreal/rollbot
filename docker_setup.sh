#
# Simple docker container removal/setup script.
# Usage:
#       
#       sh docker_setup
#
# Once ran, run your docker container with a
# name of "bot", otherwise this script will
# not automatically remove the old container
# and image for you.
#
# ie: 
#     # docker run --name bot docker_bot
#
#
# I don't have a docker setup script for
# windows yet, and I might never have one.
# If someone is willing to be awesome and
# create one, send me a pull request with
# it.



current=`docker images docker_bot | tail -n 1 | cut -d " " -f 25`

if [ '$current' != "" ] ; then
	container=`docker ps --filter "name=bot" -a | tail -n 1 | cut -d " " -f 1`
	docker rm $container
	docker rmi $current
fi 

mkdir docker_bot
cp -r ./* docker_bot/
sudo docker build -t docker_bot .

sudo rm -r docker_bot
