import time
from toripy import Toripy

LOCAL_TOR = '/Applications/TorBrowser.app/Contents/Resources/TorBrowser/Tor/tor'

with Toripy(tor_cmd=LOCAL_TOR, verbose=True) as toripy:

    print toripy.get('http://canihazip.com/s').text
    toripy.new_identity()
    print toripy.get('http://canihazip.com/s').text
