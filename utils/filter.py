from flask import current_app
from config import *
import utils.plugin as plugin
import logging
from utils.cache import cache_write
from utils.log_load import monitor_log_file
from utils.log_parse import parse_log_line
from config import load_config
import time
import asyncio


class Filters:
    def __init__(self):
        # Collect configured classifiers && plugin scripts (They must be corresponding)
        self.config_filters = extract_filters_config(CONFIG_FILE_PATH)
        self.plugin_classes = plugin.plugin_classes
        self.init_check()
        self.filters = []
        self.logs = []

    def init_check(self):
        # Initial checking: plugin_classes must be a member of configured filters
        # If some configured filters are not implemented in plugin classes, log it out.
        missing_filters = []
        for filter_name in self.config_filters:
            if filter_name not in self.plugin_classes:
                missing_filters.append(filter_name)
            else:
                logging.info(f"[*] Implemented plugin class: {filter_name}")

        if missing_filters:
            missing_filters_str = ', '.join(missing_filters)
            logging.error(f"[!] The following configured filters are not implemented in plugin classes: {missing_filters_str}")
            # raise Exception(f"[!] Missing plugin implementations for: {missing_filters_str}")

    async def run(self):
        # Load log -> Parse log -> Filter log -> Write into cache
        # Current dev plan: length(logs) = 1 -> single thread processing; TODO: multi-thread processing
        log_gen = self.log_handling()
        self.instantiate_filters()
        while True:
            try:
                log_dict = await log_gen.__anext__()
                if log_dict is not None:
                    self.logs.append(log_dict)
                    self.filtering()
                    logging.info(f"[*] Filtered logs: {self.logs}")
                    self.writing_cache()
                else:
                    logging.debug("[*] No new log entries, waiting...")
                    await asyncio.sleep(1)
            except StopAsyncIteration:
                logging.debug("[*] Log generator stopped, restarting...")
                log_gen = self.log_handling()  # Restart log monitor
            except Exception as e:
                logging.error(f"An error occurred in filters.run: {str(e)}")

    async def log_handling(self):
        # Load & Parse log
        config = load_config()
        async for log in monitor_log_file(config['logs']['file']['path'], parse_log_line):
            yield log

    def instantiate_filters(self):
        for filter_name, _ in self.plugin_classes.items():
            self.filters.append(self.instantiate_filter(filter_name))

    def instantiate_filter(self, filter_name):
        PluginClass = self.plugin_classes[filter_name]
        if not PluginClass:
            logging.error(f"[!] Plugin class to be instantiated is {filter_name} not implemented")
            return
        filter_obj = PluginClass()
        return {
            'name': filter_name,
            'filter': filter_obj
        }

    def filtering(self):
        if len(self.filters) == 0:
            logging.info(f"[*] No filters configured")
            return
        # Recursively load the same logs and go through filter to tag them.
        #   => logs[n]['tag']
        for filter_x in self.filters:
            filter_x['filter'].load_data(self.logs)
            filter_x['filter'].run()
            self.logs = filter_x['filter'].pop_data()

    def writing_cache(self):
        for log in self.logs:
            cache_write(log)
        self.logs.clear()


if __name__ == '__main__':
    # Filters init:
    # filters = Filters()
    # filters.run()

    # Async version filter test:
    async def run_filters():
        filters = Filters()
        await filters.run()
    asyncio.run(run_filters())
