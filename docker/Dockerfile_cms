FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server sudo \
    && yum --setopt=tsflags=nodocs -y install python python-pip \
    && pip install flask 

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

ADD proxy_grid /tmp/x509up_u998
RUN chown -R xrootd:xrootd /tmp/x509up_u998 


EXPOSE 80

ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]
