#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os.path
import subprocess
import sys

from flask import Flask


APP = Flask(__name__)
FORMAT = '%(asctime)s %(message)s'
DEFAULT_CONFIG = '/etc/xrootd/xrd_cache.conf'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-P', '--proxy', help='XrootD proxy file cache mode', action="store_true")
group.add_argument('-R', '--redirector', help='XrootD cache redirector mode', action="store_true")
group.add_argument('--config', help='XrootD config file path')

parser.add_argument('--nogrid', help='avoid grid CAs installation', action="store_true")
parser.add_argument('--health_port', help='port for healthcheck listening', type=int, default=80)


def check_env():
    """check env variable and set defaults for configuration
    """
    env_vars = {'REDIR_HOST': '0.0.0.0',
                'REDIR_CMSD_PORT': '1213',
                'ORIGIN_HOST': '0.0.0.0',
                'ORIGIN_XRD_PORT': '1094',
                'CACHE_PATH': '/data/xrd',
                'CACHE_RAM_GB': '12',
                'STREAMS': '256',
                'N_PREFETCH': '0',
                'BLOCK_SIZE': '512k',
                'CACHE_LOG_LEVEL': 'info',
                'LOW_WM': '0.80',
                'HI_WM': '0.90'
                }

    for key, value in env_vars.iteritems():
        # TODO: logging
        if os.environ.get(key) is None:
            os.environ[key] = value


@APP.route('/check_health', methods=['GET'])
def check_health():
    """Check health of xrootd daemons

    Arguments:
        xrd_proc {subprocess.Popen} -- xrootd daemon process
        cmsd_proc {subprocess.Popen} -- cmsd daemon process

    Returns:
        int -- 0 if healthy, 1 if down
    """

    xrd_check = APP.xrd_proc.poll()
    cmsd_check = APP.cmsd_proc.poll()

    logging.debug("Return code xrd_check: %s", xrd_check)
    logging.debug("Return code cmsd_check: %s", cmsd_check)

    if xrd_check is not None or cmsd_check is not None:
        logging.error("ERROR: one deamon down! Take a look to the logs:")
        if xrd_check is not None:
            log_path = '/var/log/xrootd/xrd.log'
            if os.path.exists(log_path):
                with open(log_path, 'r') as fin:
                    logging.debug('%s: \n %s' % (log_path, fin.read()))
        if cmsd_check is not None:
            log_path = '/var/log/xrootd/cmsd.log'
            if os.path.exists(log_path):
                with open(log_path, 'r') as fin:
                    logging.debug('%s: \n %s' % (log_path, fin.read()))
        return "1"
    else:
        logging.info("It's all good! Checking certificate timeleft now")
        try:
            subprocess.check_output("/opt/xrd_proxy/refresh_cert.sh", stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as ex:
            logging.warn("WARNING: failed to install CAs: \n %s" % ex.output)
        return "0"


if __name__ == "__main__":

    args = parser.parse_args()

    if not args.nogrid:
        logging.info("Intalling certificates...")
        #try:
        #    subprocess.check_output("/opt/xrd_proxy/install_ca.sh", stderr=subprocess.STDOUT, shell=True)
        #except subprocess.CalledProcessError as ex:
        #    logging.warn("WARNING: failed to install CAs: \n %s" % ex.output)

        logging.info("Intalling CAs... - DONE")

    check_env()
    if args.proxy:
        DEFAULT_CONFIG = "/etc/xrootd/xrd_cache_env.conf"
    if args.redirector:
        DEFAULT_CONFIG = "/etc/xrootd/xrd_redirector_env.conf"

    logging.info("Using configuration file: %s" % DEFAULT_CONFIG)

    cmsd_command = "sudo -E -u xrootd /usr/bin/cmsd -k 3 -l /var/log/xrootd/cmsd.log -c " + DEFAULT_CONFIG
    logging.debug("Starting cmsd daemon: \n %s", cmsd_command)
    try:
        cmsd_proc = subprocess.Popen(cmsd_command, shell=True)
    except ValueError as ex:
        logging.error("ERROR: when launching cmsd daemon: %s \n %s" % (ex.args, ex.message))
        sys.exit(1)
    logging.debug("cmsd daemon started!")

    xrd_command = "sudo -E -u xrootd /usr/bin/xrootd -k 3 -l /var/log/xrootd/xrd.log -c " + DEFAULT_CONFIG
    logging.debug("Starting xrootd daemon: \n %s", xrd_command)
    try:
        xrd_proc = subprocess.Popen(xrd_command, shell=True)
    except ValueError as ex:
        logging.error("ERROR: when launching xrootd daemon: %s \n %s" % (ex.args, ex.message))
        sys.exit(1)
    logging.debug("xrootd daemon started!")

    APP.cmsd_proc = cmsd_proc
    APP.xrd_proc = xrd_proc
    APP.run(host="0.0.0.0", port=args.health_port)
