# pyinstaller --onefile main.py -n pm --icon="images\casne-logo-icon_120x120.ico"
import logging
import re
import subprocess
import sys
from signal import signal, SIGINT
from time import perf_counter
from time import sleep

import toml
from apscheduler.schedulers.background import BackgroundScheduler

from rich.live import Live

from utils.log_utils import initialize_logger
from utils.rich_utils import make_data_table, make_layout
from utils.scheduler_utils import configure_scheduler

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
logging.getLogger('apscheduler').setLevel(logging.ERROR)

CONFIG_FILE = './settings/config.toml'

should_terminate = False

def signal_handler(signal_received, frame):
    # Handle any cleanup here
    logger.info(f'SIGNAL {signal_received} or CTRL-C detected.')
    global should_terminate
    should_terminate = True

signal(SIGINT, signal_handler)

def ping(ip, table_data):
    if sys.platform.startswith("win32"):
        args = ['ping', '-n', '1', '-w', '1000', str(ip)]
        process = subprocess.run(args, capture_output=True, text=True)
        if process.returncode == 0:
            try:
                search = re.search(r'Minimum = (.*)ms, Maximum = (.*)ms, Average = (.*)ms', process.stdout, re.M | re.I)
                ping_rtt = search.group(3)
                table_data[ip] = {
                    "RTT": ping_rtt,
                    "Status": "Online"
                }
            except Exception:
                table_data[ip] = {
                    "RTT": "N/A",
                    "Status": "Offline"
                }
        else:
            table_data[ip] = {
                "RTT": "N/A",
                "Status": "Offline"
            }
    else:
        args = ['ping', '-c', '1', '-W', '1', str(ip)]
        process = subprocess.run(args, capture_output=True, text=True)
        if process.returncode == 0:
            search = re.search(r'round-trip min/avg/max/stddev = (.*)/(.*)/(.*)/(.*) ms', process.stdout, re.M | re.I)
            ping_rtt = search.group(2)
            table_data[ip] = {
                "RTT": ping_rtt,
                "Status": "Online"
            }
        else:
            table_data[ip] = {
                "RTT": "N/A",
                "Status": "Offline"
            }


def main(config):
    logger.info("Running main")

    scheduler = BackgroundScheduler()
    configure_scheduler(scheduler, config)

    ip_addresses = config.get("ip_addresses")

    logger.info("Adding IP addresses to ping")
    table_data = {}
    for ip in ip_addresses:
        scheduler.add_job(ping, 'interval', seconds=5, args=[ip, table_data], executor='default')
        table_data[ip] = {
            "RTT": "N/A",
            "Status": "Offline"
        }

    logger.info("Starting scheduler")
    scheduler.start()

    logger.info("Making layout")
    layout = make_layout()

    logger.info("Doing it live")
    with Live(layout, refresh_per_second=10, screen=True):
        while not should_terminate:
            sleep(0.1)
            layout["body"].update(make_data_table(table_data))

    logger.info("Shutting down scheduler")
    scheduler.shutdown()
    return True


if __name__ == '__main__':
    try:
        config = toml.load(CONFIG_FILE)
    except Exception:
        logger.error(f"Failed to load config from file {CONFIG_FILE} exiting...")
        sys.exit(1)

    initialize_logger(logger, config)

    try:
        total_start = perf_counter()
        if main(config):
            logger.info('Finished successfully!')
        else:
            logger.info('Failed to finish successfully!')
        total_end = perf_counter()
        logger.info(f"Program completed in {total_end - total_start:.2f} seconds")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception("Failed to finish successfully due to uncaught exception!")
