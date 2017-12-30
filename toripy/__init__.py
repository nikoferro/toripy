import sys
import time
from datetime import datetime
import socket
import socks
import requests

import stem
from stem import Signal
from stem.control import Controller
from stem.process import launch_tor_with_config
from stem.util import term


class Toripy(object):
    def __init__(self,
                 proxy_port=9150,
                 controller_port=9051,
                 password=None,
                 socks_port=7000,
                 socks_ip="127.0.0.1",
                 tor_config=None,
                 tor_cmd=None,
                 verbose=False,
                 use_default_proxy=False):

        self.proxy_port = proxy_port
        self.socks_port = socks_port
        self.socks_ip = socks_ip
        self.controller_port = controller_port
        self.password = password
        self.tor_config = tor_config
        self.tor_cmd = tor_cmd
        self.verbose = verbose
        self.use_default_proxy = use_default_proxy

        self.tor_process = None

        self.__start_tor_process()

    def __setup_tor_controller(self):
        if self.verbose:
            print(str(datetime.now()) + ' - ' + term.format(
                'Setting up controller on port: ' + str(self.controller_port), term.Color.BLUE))

        try:
            self.controller = Controller.from_port(port=self.controller_port)
        except stem.SocketError as exc:
            print(str(datetime.now()) + ' - ' + term.format(
                'Unable to connect to tor: %s' % exc, term.Color.RED))
            sys.exit(1)

        try:
            self.controller.authenticate(password=self.password)
        except stem.connection.MissingPassword:
            print(str(datetime.now()) + ' - ' + term.format(
                'Unable to authenticate, password is missing' % exc, term.Color.RED))
            sys.exit(1)
        except stem.connection.PasswordAuthFailed:
            print(str(datetime.now()) + ' - ' + term.format(
                'Unable to authenticate, password is incorrect' % exc, term.Color.RED))
            sys.exit(1)
        except stem.connection.AuthenticationFailure as exc:
            print(str(datetime.now()) + ' - ' + term.format(
                'Unable to authenticate: %s' % exc, term.Color.RED))
            sys.exit(1)

        if self.verbose:
            print(str(datetime.now()) + ' - ' + term.format('Tor is running version %s' %
                                                            self.controller.get_version(), term.Color.BLUE))

    def __setup_sockets_connection(self):
        if self.verbose:
            print(str(datetime.now()) + ' - ' + term.format(
                'Creating socks5 proxy on port: ' + str(self.socks_port), term.Color.BLUE))

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                              self.socks_ip, self.socks_port)
        socket.socket = socks.socksocket

    def __start_tor_process(self):
        if not self.__is_tor_running():
            if self.verbose:
                print(str(datetime.now()) + ' - ' + term.format(
                    'No TOR process found. Creating a new one...', term.Color.GREEN))
            self.tor_process = self.__launch_tor_with_config(
                tor_config=self.tor_config, tor_cmd=self.tor_cmd)

        self.__setup_tor_controller()
        if not self.use_default_proxy:
            self.__setup_sockets_connection()

    def __print_init_msg(self, line):
        if "Bootstrapped " in line:
            print(str(datetime.now()) + ' - ' +
                  term.format(line[42:], term.Color.BLUE))

    def __is_tor_running(self):
        if self.tor_process:
            if self.verbose:
                print(str(datetime.now()) + ' - ' +
                      term.format('TOR process found', term.Color.YELLOW))
                self.close()
            return True
        else:
            return False

    def __launch_tor_with_config(self, tor_config, tor_cmd):
        if not tor_config:
            tor_config = {
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.controller_port)
            };

        if not tor_cmd:
            if self.verbose:
                print(str(datetime.now()) + ' - ' + term.format(
                    '''Missing tor_cmd argument. You need to specify TOR's location in your system''', term.Color.RED))
                print(str(datetime.now()) + ' - ' + term.format(
                    '''We will try using the default value, but it might fail''', term.Color.RED))
            tor_cmd = 'tor'

        if self.verbose:
            init_msg_handler = self.__print_init_msg
        else:
            init_msg_handler = None

        return launch_tor_with_config(
            tor_cmd=tor_cmd,
            config=tor_config,
            init_msg_handler=init_msg_handler,
            take_ownership=True
        )

    def close(self):
        try:
            self.controller.close()
        except:
            pass

        if self.tor_process:
            if self.verbose:
                print(str(datetime.now()) + ' - ' +
                      term.format('Closing current tor process', term.Color.RED))
            self.tor_process.kill()

    def new_identity(self):
        self.controller.signal(Signal.NEWNYM)
        if self.verbose:
            print(str(datetime.now()) + ' - ' +
                  term.format('Changing to new identity in ' + str(self.controller.get_newnym_wait()) + ' seconds', term.Color.RED))
        time.sleep(self.controller.get_newnym_wait())

    def get_latest_heartbeat(self):
        return self.controller.get_latest_heartbeat()

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return requests.put(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return requests.patch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return requests.delete(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
