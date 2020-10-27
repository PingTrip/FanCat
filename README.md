# FanCat
A Python3 script to auto-control NVIDIA GPU fans during password cracking 

Requires Python daemon module (`apt install pythyon3-daemon`)

```
usage: fancat.py [-h] [--debug] [-t [40-90]] [--daemon] [-m [20-100]]

optional arguments:
  --debug               Enable debug messages
  -t [40-90], --target-temp [40-90]
                        Target temperature (celcius) to maintain GPU. Defaults to 80.
  --daemon              Daemonize this process. Default is False
  -m [20-100], --min-fan-speed [20-100]
                        Minimum fan speed allowed (20-100). Defaults to 27.
```
