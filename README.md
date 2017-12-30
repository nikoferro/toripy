# Toripy

Lightweight python interface to easily make HTTP(s) requests over the Tor network

## Usage

The 3 following code examples cover this 3 different scenarios

* Using Toripy minimal config to run a Tor process and make a request over the Tor network.
* Using Toripy custom config to run a Tor process and make a request over the Tor network using an specific exit node.
* Using Toripy custom config to run a Tor process, launch Firefox with selenium using this Tor process as a proxy, and automate actions while connected to this proxy.

### Minimal config

```
from toripy import Toripy

LOCAL_TOR = '/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/tor'

with Toripy(tor_cmd=LOCAL_TOR) as toripy:
    ip_adress = toripy.get('http://www.icanhazip.com').text
    print('This should not be your IP adress:')
    print(ip_adress)
```

### Custom Config

In this example we choose '{ru}' as the exit node. This means that our exit node will be located in Russia (meaning also that our disclosed IP will be from Russia). You can also choose a group of exit nodes, or one exit node IP in particular, so your proccess uses always the same exit node.

```
from toripy import Toripy

LOCAL_TOR = '/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/tor'
SOCKS_HOST = "127.0.0.1"
SOCKS_PORT = 7000

tor_config = {
    'SocksPort': str(SOCKS_PORT),
    'ControlPort': str(9051),
    'ExitNodes': '{ru}',
    'GeoIPFile': r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip',
    'GeoIPv6File': r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip6'
}

with Toripy(tor_cmd=LOCAL_TOR, verbose=True, tor_config=tor_config) as toripy:
    ip_adress = toripy.get('http://www.icanhazip.com').text
    print('This should be a russian ip adress:')
    print(ip_adress)
```

### Custom Config + Selenium w/Firefox

To run this example make sure you have Firefox, Geckodriver and Selenium installed.

```
import time
from toripy import Toripy
from selenium import webdriver

LOCAL_TOR = '/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/tor'
SOCKS_HOST = "127.0.0.1"
SOCKS_PORT = 7000

tor_config = {
    'SocksPort': str(SOCKS_PORT),
    'ControlPort': str(9051),
    'ExitNodes': '{ru}',
    'GeoIPFile': r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip',
    'GeoIPv6File': r'/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/geoip6'
}

with Toripy(tor_cmd=LOCAL_TOR, verbose=True, tor_config=tor_config, use_default_proxy=True):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",SOCKS_HOST)
    fp.set_preference("network.proxy.socks_port",int(SOCKS_PORT))
    fp.update_preferences()
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("https://www.infobyip.com/")
```
