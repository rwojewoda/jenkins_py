FROM jenkins/jenkins
COPY id_rsa /var/jenkins_home/.ssh/id_rsa
COPY id_rsa.pub /var/jenkins_home/.ssh/id_rsa.pub
USER root
RUN mkdir -p /tmp/download && \
 curl -L https://download.docker.com/linux/static/stable/x86_64/docker-18.09.3.tgz | tar -xz -C /tmp/download && \
 rm -rf /tmp/download/docker/dockerd && \
 mv /tmp/download/docker/docker* /usr/local/bin/ && \
 rm -rf /tmp/download && \
 groupadd -g 999 docker && \
 usermod -aG staff,docker jenkins
RUN chmod 777 /var/jenkins_home/.ssh/id_rsa
RUN chmod 777 /var/jenkins_home/.ssh/id_rsa.pub
user jenkins