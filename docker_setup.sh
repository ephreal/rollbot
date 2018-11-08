# Copyright 2018 Ephreal

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.




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



current=`sudo docker images docker_bot | tail -n 1 | cut -d " " -f 25`

if [ '$current' != "" ] ; then
	container=`sudo docker ps --filter "name=bot" -a | tail -n 1 | cut -d " " -f 1`
	sudo docker rm $container
	sudo docker rmi $current
fi 

mkdir docker_bot
cp -r ./* docker_bot/
sudo docker build -t docker_bot .

sudo rm -r docker_bot
