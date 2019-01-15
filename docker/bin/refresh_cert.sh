#!/bin/bash

chown -R xrootd:xrootd /data/xrd

VALID=`sudo -u xrootd grid-proxy-info -f /tmp/x509up_u998 -e -h 24 && echo "VALID" || echo "EXPIRED"`

if [ "$VALID" == "VALID" ]; then
    echo "Proxy is valid"
else
    echo "Proxy $VALID. Retrieving a new one..."
    sudo -u xrootd grid-proxy-init -cert /etc/grid-security/xrd/usercert.pem -key /etc/grid-security/xrd/userkey.pem -valid 48:00

    echo "Done. Refreshing CAs..."
    yum install -y ca-policy-egi-core ca-policy-lcg

    /usr/sbin/fetch-crl -q

    wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/view/dodas/job/ca_DODAS-TTS/job/master/lastSuccessfulBuild/artifact/ca_DODAS-TTS.repo
    yum -y install ca_DODAS-TTS

    echo "DONE."
fi