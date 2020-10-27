#!/usr/bin/env python3

from signal import signal, SIGINT
import sys
import time
import argparse
import subprocess
import daemon


def clean_exit(signal_received, frame):
    if args.debug:
        print('SIGINT or CTRL-C detected. Exiting.')
    adjust_fan_speed(True, exiting=True)
    enable_fan_control(False)
    sys.exit(0)


def enable_fan_control(enable):
    if args.debug:
        print(f'Enabling fan control: {enable}')
    subprocess.run(['nvidia-settings', '-a', f'GPUFanControlState={int(enable)}'], stdout=subprocess.PIPE)


def get_temp():
    cur_temps = []
    results = subprocess.run(['nvidia-settings', '-q', 'gpucoretemp'], stdout=subprocess.PIPE)
    for line in results.stdout.decode().splitlines():
        if '[gpu' in line:
            cur_temps.append(line.split()[3].rstrip('.'))
    cur_max_temp = int(max(cur_temps))

    if args.debug:
        print(f'Current GPU temp: {cur_max_temp}')

    return cur_max_temp


def adjust_fan_speed(increase, exiting=False):
    results = subprocess.run(['nvidia-settings', '-tq', 'GPUCurrentFanSpeed'], stdout=subprocess.PIPE)
    cur_max_speed = max([int(x) for x in results.stdout.decode().splitlines()])

    if args.debug:
        print(f'Current GPU fan speed: {cur_max_speed}')

    adj_value = 2 if increase else -2
    new_speed = cur_max_speed + adj_value

    # Sanity check for max/min fan speeds
    if new_speed > 100:
        new_speed = 100
    elif new_speed < args.min_fan_speed:
        new_speed = args.min_fan_speed

    if exiting:
        new_speed = args.min_fan_speed

    if new_speed != cur_max_speed:
        results = subprocess.run(['nvidia-settings', '-a', f'GPUTargetFanSpeed={new_speed}'], stdout=subprocess.PIPE)
        if args.debug:
            print(f'Adjusting fan speed to: {new_speed}')


def process_loop():
    enable_fan_control(True)

    while True:
        if args.debug:
            print("Polling..")

        cur_temp = get_temp()
        if cur_temp > args.target_temp:
            adjust_fan_speed(True)
        elif cur_temp < args.target_temp - 2:
            adjust_fan_speed(False)

        time.sleep(5)


def start_daemon():
    with daemon.DaemonContext():
        process_loop()


if __name__ == "__main__":
    signal(SIGINT, clean_exit)
    parser = argparse.ArgumentParser(description="Auto-Fan control for Hashcat with NVIDIA")

    parser.add_argument('--debug',
                        dest='debug',
                        help='Enable debug messages',
                        action='store_true',
                        default=False)
    parser.add_argument('-t', '--target-temp',
                        dest="target_temp",
                        help='Target temperature (celcius) to maintain GPU. Defaults to 80.',
                        metavar='[40-90]',
                        type=int, choices=range(40, 90),
                        default=80)
    parser.add_argument('--daemon',
                        dest="daemonize",
                        help='Daemonize this process. Default is False',
                        action='store_true',
                        default=False)
    parser.add_argument('-m', '--min-fan-speed',
                        dest="min_fan_speed",
                        help='Minimum fan speed allowed (20-100). Defaults to 27.',
                        metavar='[20-100]',
                        type=int, choices=range(20, 100),
                        default=30)

    args = parser.parse_args()

    if args.daemonize:
        start_daemon()
    else:
        process_loop()
