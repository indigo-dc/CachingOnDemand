#!/bin/bash

VALID=`sudo -u xrootd grid-proxy-info -f /tmp/x509up_u998 -e -h 24 && echo "VALID" || echo "EXPIRED"`

if [ "$VALID" == "VALID" ]; then
    echo "Proxy is valid"
else
    echo "Proxy $VALID. Retrieving a new one..."
    sudo -u xrootd grid-proxy-init -cert /etc/grid-security/xrd/usercert.pem -key /etc/grid-security/xrd/userkey.pem -valid 48:00

    echo "Done. Refreshing CAs..."
    yum install -y ca-policy-egi-core ca-policy-lcg

    /usr/sbin/fetch-crl -q

    wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/job/cnaf-mw-devel-jobs/job/ca_CMS-TTS-CA/job/master/lastSuccessfulBuild/artifact/ca_CMS-TTS-CA.repo
    yum -y install ca_CMS-TTS-CA

    echo "DONE."
fi