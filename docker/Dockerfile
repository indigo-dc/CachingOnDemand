FROM cloudpg/centos-7-grid as base
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server sudo \
    && yum --setopt=tsflags=nodocs -y install python python-pip \
        xrootd-devel.x86_64 xrootd-server-devel.x86_64 \
        gcc gcc-c++ cmake git \
        libcurl libcurl-devel jsoncpp-devel\
    && pip install flask 

# Compile plugins
FROM base as plugins

COPY src src
COPY spec spec
COPY cmake cmake
COPY config/cmake/CMakeLists.txt CMakeLists.txt

RUN cmake ./
RUN make && mkdir /usr/local/smartDecisionPlugin && cp -rfdav ./* /usr/local/smartDecisionPlugin && chown -R xrootd:xrootd /usr/local/smartDecisionPlugin

# Install server without plugins
FROM base as server

RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

ADD config /etc/xrootd
RUN chown -R xrootd:xrootd /etc/xrootd 

RUN mkdir -p /opt/xrd_proxy
ADD bin /opt/xrd_proxy 
RUN chown -R xrootd:xrootd /opt/xrd_proxy 

RUN chmod +x /opt/xrd_proxy/install_ca.sh
RUN /opt/xrd_proxy/install_ca.sh
RUN chmod +x /opt/xrd_proxy/refresh_cert.sh

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

RUN mkdir -p /var/log/xrootd/
RUN chown -R xrootd:xrootd /var/log/xrootd/

RUN echo 'xrootd ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

EXPOSE 80

ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]

# Install server with plugins
FROM plugins as plugin_server

RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

ADD config /etc/xrootd
RUN chown -R xrootd:xrootd /etc/xrootd 

RUN mkdir -p /opt/xrd_proxy
ADD bin /opt/xrd_proxy 
RUN chown -R xrootd:xrootd /opt/xrd_proxy 

RUN chmod +x /opt/xrd_proxy/install_ca.sh
RUN /opt/xrd_proxy/install_ca.sh
RUN chmod +x /opt/xrd_proxy/refresh_cert.sh

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

RUN mkdir -p /var/log/xrootd/
RUN chown -R xrootd:xrootd /var/log/xrootd/

RUN echo 'xrootd ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

EXPOSE 80

ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]