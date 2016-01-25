# ssh keyscanner - search shodan for a given ssh hostkey fingerprint.

This tool has two modes, currently. It can search given a public-key you provide it, or, it can fingerprint a host and search shodan for similar hosts.

It currently is incomplete (see the todo list), but works for those uses.

It now has support for doing the keygrab over tor, and works on hidden services. This is useful for finding, uh, shittily configured ones.

## Howto:
The tool has 4 args, outlined below.   
* "-i", for target host. You must set either this, -l, or -f. 
* "-f", for SSH Public Key file. You must set either this, -f, or -i.  
* "-l", for lists of target hosts. Alternative to -i or -f.  
* "-d", for directories of keys. Not yet implemented!
* "-p", for target port. This defaults to 22.
* "-t", uses Tor for the SSH key grabbing. Good for Hidden Services ;)

You should also edit the script to put in your own [Shodan](https://www.shodan.io/) API key, as you can't have mine. You can probably just borrow someone elses, [as people leave them all over github](https://github.com/0x27/shodan_key_checker).

## Requirements
This tool depends on the following:  
[Paramiko](http://www.paramiko.org/)  
[sshpubkeys](https://github.com/ojarva/python-sshpubkeys)  
[shodan](https://github.com/achillean/shodan-python)  
[PySocks](https://github.com/Anorov/PySocks)  
You can get them with ```pip install -r requirements.txt``` or whatever. The rest should be stdlib.

Note: I only bothered testing on python2.

## Todo  
* Private-Key support so I can also use privkeys as well as pubkeys.
* Directory of keyfile support.
* List of hosts support.
* idk, make a git issue with your ideas...

## Licence
[Licenced under the WTFPL (do Whatever The Fuck you want Public Licence)][Licence]

## Beer?
Send yer cryptologically generated beer tokens to fuel further opensource software:  
[coinbase, for convenience][coinbase], or the following bitcoin address: `13rZ67tmhi7M3nQ3w87uoNSHUUFmYx7f4V`

## Mandatory asciicast until I finish it and make a proper video  
[![asciicast](https://asciinema.org/a/0hi7u7c3ju6q2vc4xzt4v7saf.png)](https://asciinema.org/a/0hi7u7c3ju6q2vc4xzt4v7saf)

## Bug Reports and Feature Requests
Please submit all bug reports and feature requests to the [Github Issue Tracker][tracker]. Give me stacktraces by enabling debug mode.

## Changelog  
18-01-2015 (01:26): - Added Tor support on a whim. Completely untested, will get tested in the morning when I wake up.

[coinbase]: https://www.coinbase.com/infodox/
[Licence]: http://www.wtfpl.net/txt/copying/
[tracker]: https://github.com/0x27/ssh_keyscanner/issues
