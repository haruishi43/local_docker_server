# CMake

```dockerfile
RUN wget https://github.com/Kitware/CMake/releases/download/v3.17.2/cmake-3.17.2-Linux-x86_64.sh \
    -q -O /tmp/cmake-install.sh \
    && chmod u+x /tmp/cmake-install.sh \
    && mkdir /usr/bin/cmake \
    && /tmp/cmake-install.sh --skip-license --prefix=/usr/bin/cmake \
    && rm /tmp/cmake-install.sh
ENV PATH="/usr/bin/cmake/bin:${PATH}"
```

However, this snippet doesn't seem to work when trying to call `cmake` from inside the container (from the user).

```dockerfile
RUN wget https://github.com/Kitware/CMake/releases/download/v3.13.4/cmake-3.13.4-Linux-x86_64.sh && \
    mkdir /opt/cmake && \
    sh /cmake-3.13.4-Linux-x86_64.sh --prefix=/opt/cmake --skip-license && \
    ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake
```

This snippet works from the user.