#!/bin/bash

sudo voms-proxy-init --cert /etc/grid-security/xrd/cert/cert.pem --key /etc/grid-security/xrd/cert/key.pem -voms cms -out /tmp/proxy