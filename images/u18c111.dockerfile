FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04
LABEL maintainer="Haruya Ishikawa haruyaishikawa@keio.jp"
ENV DEBIAN_FRONTEND "noninteractive"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all

RUN apt-get update && \
    apt-get -y \
        -o Dpkg::Options::="--force-confdef" \
        -o Dpkg::Options::="--force-confold" dist-upgrade && \
# Mainly pyenv dependencies
    apt-get install -y --no-install-recommends \
        make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
        xz-utils tk-dev libffi-dev libxmlsec1-dev libxml2-dev liblzma-dev python-openssl \
        git && \
# Other stuff that's handy
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

# Manage user
RUN mkdir /var/run/sshd && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile && \
    useradd -m -d /home/ubuntu ubuntu && \
    gpasswd -a ubuntu sudo && \
    echo 'ubuntu:password' | chpasswd && \
    chown -R ubuntu:ubuntu /home/ubuntu && \
    chsh -s /usr/bin/zsh ubuntu

USER ubuntu
WORKDIR /home/ubuntu
ENV HOME /home/ubuntu

COPY --chown=ubuntu:ubuntu .zshrc /home/ubuntu
COPY --chown=ubuntu:ubuntu .zshenv /home/ubuntu
RUN chown -R ubuntu:ubuntu /home/ubuntu && \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

RUN git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN eval "$(pyenv init -)" && pyenv install 3.8.6 && pyenv rehash && pyenv global 3.8.6 && \
    pip install --upgrade pip && \
    pip install ipython \
        jupyter ipdb tqdm numpy pandas sklearn matplotlib \
        opencv-python opencv-contrib-python \
        tensorflow keras && \
    pip install torch==1.8.0+cu111 torchvision==0.9.0+cu111 torchaudio==0.8.0 -f https://download.pytorch.org/whl/torch_stable.html && \
    mkdir .jupyter
# COPY --chown=ubuntu:ubuntu jupyter_notebook_config.py $HOME/.jupyter

USER root
WORKDIR /
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
