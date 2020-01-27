Polycom Reboot Tool
===================

This reboots polycom phones via HTTP. Previous strategies no longer work for me with UC 4.x, due to XSS mitigations in the phones. This has been tested with several phones on UC 4.x, and may work for later ones.

This will reboot a default phone:

``` console
$ polyboot.py 1.2.3.4
```

A few other options are available:

``` console
usage: polyboot.py [-h] [--password PASSWORD] [--verbose] [--debug] [--timeout TIMEOUT] [--action {Reboot,Restart}] phone

positional arguments:
  phone                 IP or hostname of the phone

optional arguments:
  -h, --help            show this help message and exit
  --password PASSWORD, -p PASSWORD
  --verbose, -v
  --debug
  --timeout TIMEOUT
  --action {Reboot,Restart}
```

