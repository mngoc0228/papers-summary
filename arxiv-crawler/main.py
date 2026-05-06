import argparse
import asyncio
import logging
import logging.config
from multiprocessing import Process
import signal
import sys

from dotenv import load_dotenv

from store.app_context import app_context

listener_tasks = []

load_dotenv()

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": logging.INFO,
    },
})

async def start_worker():
    global listener_tasks
    try:
        # Start up application context
        await app_context.start_up()

        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logging.info("Main task cancelled. Shutting down listeners...")
        for task in listener_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                logging.info("Listener task cancelled successfully.")
    finally:
        await app_context.shut_down()
        logging.info("Application shut down complete.")


def start(worker_id: int):
    asyncio.run(start_worker())


def main():
    parser = argparse.ArgumentParser(description="Start the arXiv crawler with multiple worker processes.")
    parser.add_argument("-w", "--workers", type=int, default=1, help="Number of worker processes to spawn")
    args = parser.parse_args()
    processes = []

    def signal_handler(sig, frame):
        logging.info("Termination signal received. Shutting down gracefully...")
        for process in processes:
            process.join(timeout=30)
            if process.is_alive():
                logging.warning(f"Process {process.pid} did not terminate in time. Forcing termination.")
                process.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    for i in range(args.workers):
        worker_id = i + 1
        process = Process(target=start, args=(worker_id,))
        processes.append(process)
        process.start()
        logging.info(f"Started worker process with PID: {process.pid}")

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()