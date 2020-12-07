FROM ubuntu:18.04
MAINTAINER Haruya Ishikawa <haruyaishikawa@keio.jp>
ENV DEBIAN_FRONTEND "noninteractive"

COPY motd /etc
RUN apt-get update
RUN apt-get -y \
            -o Dpkg::Options::="--force-confdef" \
            -o Dpkg::Options::="--force-confold" dist-upgrade
RUN apt-get install -y zsh git curl wget build-essential \
                       python-dev libgtk2.0-dev make libssl-dev \
                       zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
                       llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev \
                       htop pkg-config libevent-dev libncurses5-dev automake \
                       sudo software-properties-common locales liblzma-dev
RUN apt-get install -y openssh-server

# install vim
RUN add-apt-repository ppa:jonathonf/vim -y
RUN apt-get update
RUN apt-get install -y vim

# install tmux
RUN mkdir /tmp/tmux
WORKDIR /tmp/tmux
RUN curl -LO https://github.com/tmux/tmux/releases/download/2.8/tmux-2.8.tar.gz
RUN tar xfvz tmux-2.8.tar.gz
WORKDIR /tmp/tmux/tmux-2.8/
RUN ./configure && make
RUN cp -p /tmp/tmux/tmux-2.8/tmux /usr/local/sbin
WORKDIR /

# set local
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:UTF-8
ENV LC_ALL en_US.UTF-8

RUN mkdir /var/run/sshd
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN useradd -m -d /home/ubuntu ubuntu
RUN gpasswd -a ubuntu sudo
RUN echo 'ubuntu:password' | chpasswd
RUN chown -R ubuntu:ubuntu /home/ubuntu
RUN chsh -s /usr/bin/zsh ubuntu

USER ubuntu
WORKDIR /home/ubuntu
ENV HOME /home/ubuntu

RUN bash -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
RUN git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

COPY --chown=ubuntu:ubuntu .zshrc /home/ubuntu
COPY --chown=ubuntu:ubuntu .zshenv /home/ubuntu

RUN chown -R ubuntu:ubuntu /home/ubuntu

RUN git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN eval "$(pyenv init -)"
RUN pyenv install anaconda3-5.2.0
RUN pyenv install 3.8.2
RUN pyenv rehash
RUN pyenv global 3.8.2
RUN pip install --upgrade pip

RUN mkdir $HOME/private
RUN touch $HOME/private/.zsh_history

USER root
WORKDIR /
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

