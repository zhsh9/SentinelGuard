import os
import asyncio
import logging
from config import load_config
from flask import current_app


async def tail_f(filepath):
    """
    Asynchronous generator that yields new lines in a file as they are written.
    :param filepath: log file path
    :return: async generator that yields new lines as they are written
    """
    try:
        with open(filepath, 'r') as file:
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    await asyncio.sleep(0.25)
                    yield None
                else:
                    await asyncio.sleep(0.1)
                    yield line.strip()
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {str(e)}")


async def monitor_log_file(filepath, log_parse):
    """
    Start monitoring the log file and yield new log records.
    :param filepath: log file path
    :param log_parse: log parse function
    :return: async generator that yields parsed log records
    """
    log_generator = tail_f(filepath)
    logging.info(f"[+] Monitoring log file {filepath}")
    async for record in log_generator:
        if record is not None:
            yield log_parse(record, load_config())
