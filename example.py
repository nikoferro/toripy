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
    fp.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A")
    fp.update_preferences()
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("https://www.infobyip.com/")

with Toripy(tor_cmd=LOCAL_TOR, verbose=True, tor_config=tor_config) as toripy:
    ip_adress = toripy.get('http://www.icanhazip.com').text
    print('This should be a russian ip adress:')
    print(ip_adress)