import logging
import asyncio
import multiprocessing
from flask import Flask, render_template
from config import load_flask_config
from utils.filter import Filters
from utils.cache import cache_read

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Set up flask app
app = Flask(__name__)
load_flask_config(app)


# Define a function to run the asyncio event loop in a separate process
def start_filters():
    logger.debug("Starting filters process")
    asyncio.run(run_filters())
    logger.debug("Filters process ended")


# Filters init:
async def run_filters():
    logger.debug("Initializing filters")
    filters = Filters()
    await filters.run()
    logger.debug("Filters run completed")


@app.route('/')
def index():
    intrusion_rules = app.config['rules']['ai_methods'] + app.config['rules']['intrusions']
    cache_content = cache_read()
    has_cache = len(cache_content) > 0
    # Find how many of them are tagged as 'True'
    threads = []
    for thread in cache_content:
        tags = thread["tag"]
        is_thread = False
        for _, val in tags.items():
            if val:
                threads.append(thread)
                is_thread = True
                break
            if is_thread:
                break

    return render_template("index.html",
                           intrusion_rules=intrusion_rules,
                           has_cache=has_cache, cache_content=cache_content, threads=len(threads))


def run_flask():
    logger.debug("Starting Flask app")
    # Load configuration:
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    # Run Flask app
    app.run(host=host, port=port)
    logger.debug("Flask app ended")


def main():
    logger.debug("Main process started")
    # Create a process for the Flask app
    flask_process = multiprocessing.Process(target=run_flask)

    # Create a process for the filters
    filters_process = multiprocessing.Process(target=start_filters)

    # Start the processes
    flask_process.start()
    filters_process.start()

    logger.debug("Started both Flask and filters processes")

    # Join the processes to ensure they run concurrently
    flask_process.join()
    filters_process.join()

    logger.debug("Both processes completed")


if __name__ == '__main__':
    # Set the start method for multiprocessing
    multiprocessing.set_start_method('spawn')  # or 'fork' depending on your platform and needs
    main()
    