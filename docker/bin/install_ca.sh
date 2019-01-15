#!/bin/bash
yum install -y ca-policy-egi-core ca-policy-lcg

/usr/sbin/fetch-crl -q

wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/view/dodas/job/ca_DODAS-TTS/job/master/lastSuccessfulBuild/artifact/ca_DODAS-TTS.repo
yum -y install ca_DODAS-TTS

chmod 600 /etc/grid-security/xrd/userkey.pem

sudo chown -R xrootd:xrootd /etc/grid-security/xrd/

#echo "Retrieving proxy"
#sudo -u xrootd grid-proxy-init -cert /etc/grid-security/xrd/usercert.pem -key /etc/grid-security/xrd/userkey.pem
