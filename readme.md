docker container run -d --name jenkins -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock --mount source=jenkins_vol,target=/var/jenkins_home jenkins_docker_img

docker container run -d --name jenkins -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v /home/radek/ngrok:/var/jenkins_home/workspace/setup_github_hook --mount source=jenkins_vol,target=/var/jenkins_home jenkins_docker_img


eval $(ssh-agent -s)

docker container run --name java --rm -p 8080:8080 -d davout123/pi
