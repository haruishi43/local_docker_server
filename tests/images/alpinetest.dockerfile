FROM alpine:latest
LABEL creator="admin"
LABEL maintainer="hoge@foo.bar"

RUN apk update && \
    apk add --no-cache sudo bash openrc openssh && \
    rm  -rf /tmp/* /var/cache/apk/*
RUN mkdir -p /run/openrc && \
    touch /run/openrc/softlevel && \
    rc-update add sshd default

RUN sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
    && echo "root:root" | chpasswd \
    && sed -ie 's/#Port 22/Port 22/g' /etc/ssh/sshd_config \
    && sed -ri 's/#HostKey \/etc\/ssh\/ssh_host_key/HostKey \/etc\/ssh\/ssh_host_key/g' /etc/ssh/sshd_config \
    && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/g' /etc/ssh/sshd_config \
    && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_dsa_key/HostKey \/etc\/ssh\/ssh_host_dsa_key/g' /etc/ssh/sshd_config \
    && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/HostKey \/etc\/ssh\/ssh_host_ecdsa_key/g' /etc/ssh/sshd_config \
    && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ed25519_key/HostKey \/etc\/ssh\/ssh_host_ed25519_key/g' /etc/ssh/sshd_config \
    && /usr/bin/ssh-keygen -A \
    && ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile && \
    useradd -m -d /home/user user && \
    gpasswd -a user sudo && \
    echo 'user:password' | chpasswd && \
    chown -R user:user /home/user

USER user

USER root
WORKDIR /
EXPOSE 22
# ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/usr/sbin/sshd","-D"]
