# FanCat
A Python3 script to auto-control NVIDIA GPU fans during password cracking 

Requires Python daemon module (`apt install pythyon3-daemon`)

```
usage: fancat.py [-h] [--debug] [-t [40-90]] [--daemon] [-m [30-100]]

Auto-Fan control for Hashcat with NVIDIA

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable debug messages
  -t [40-90], --target-temp [40-90]
                        Target temperature (celcius) to maintain GPU. Defaults to 80.
  --daemon              Daemonize this process. Default is False
  -m [30-100], --min-fan-speed [30-100]
                        Minimum fan speed allowed (30-100). Defaults to 40.
```

#### EXAMPLE RUN
Running with default settings:

```
$ ./fancat.py --debug

Enabling fan control: True
Polling..
  Current GPU fan speed: 40
  Current GPU temp: 60
```
Hashcat process has been started in another terminal and GPU's are heating up:

```
Polling..
  Current GPU fan speed: 40
  Current GPU temp: 70
Polling..
  Current GPU fan speed: 40
  Current GPU temp: 72
Polling..
  Current GPU fan speed: 40
  Current GPU temp: 75
Polling..
  Current GPU fan speed: 40
  Current GPU temp: 77
```

Max temp setting of 80 being passed, FanCat ramping up fans:

```
Polling..
  Current GPU fan speed: 68
  Current GPU temp: 84
  Adjusting fan speed to: 73
Polling..
  Current GPU fan speed: 72
  Current GPU temp: 83
  Adjusting fan speed to: 77
Polling..
  Current GPU fan speed: 76
  Current GPU temp: 82
  Adjusting fan speed to: 81
Polling..
  Current GPU fan speed: 80
  Current GPU temp: 81
  Adjusting fan speed to: 90
Polling..
  Current GPU fan speed: 89
  Current GPU temp: 81
  Adjusting fan speed to: 99
  ```
Hashcat session has ended and GPUs are cooling, slowly spinning down fans
```
Polling..
  Current GPU fan speed: 45
  Current GPU temp: 57
  Adjusting fan speed to: 43
Polling..
  Current GPU fan speed: 43
  Current GPU temp: 57
  Adjusting fan speed to: 41
Polling..
  Current GPU fan speed: 42
  Current GPU temp: 57
  Adjusting fan speed to: 40
```
