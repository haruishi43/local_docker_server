FROM ubuntu:18.04
LABEL maintainer="Haruya Ishikawa hauryaishikawa@keio.jp"
ENV DEBIAN_FRONTEND "noninteractive"

# NOTE: Removed a lot of things for testing!

RUN apt-get update
RUN apt-get -y \
        -o Dpkg::Options::="--force-confdef" \
        -o Dpkg::Options::="--force-confold" dist-upgrade && \
# Mainly dev dependencies:
    apt-get install -y --no-install-recommends \
        make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev libxmlsec1-dev libxml2-dev liblzma-dev python-openssl \
        git && \
# Other handy stuff
    apt-get install -y \
        zsh python-dev libgtk2.0-dev \
        htop pkg-config libevent-dev automake \
        sudo software-properties-common locales \
        openssh-server \
        tmux neofetch neovim

# set local
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:UTF-8
ENV LC_ALL en_US.UTF-8

# changes pam configuration from required to optional
RUN mkdir /var/run/sshd && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile && \
    useradd -m -d /home/ubuntu ubuntu && \
    gpasswd -a ubuntu sudo && \
    echo 'ubuntu:password' | chpasswd && \
    chown -R ubuntu:ubuntu /home/ubuntu

USER ubuntu
WORKDIR /home/ubuntu
ENV HOME /home/ubuntu

USER root
WORKDIR /
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
