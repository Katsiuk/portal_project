FROM jenkins/ssh-agent:latest

# Change the timezone
ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Make sure the package repository is up to date.
RUN apt-get update && \
    apt-get -qy full-upgrade

#kubectl setup

RUN apt-get install curl -y
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

# Standard SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]