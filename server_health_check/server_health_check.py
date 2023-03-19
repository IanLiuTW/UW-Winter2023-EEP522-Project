from fastapi import APIRouter
import threading
import time
import os
from .openai import openai_health_check
from .config import CHECK_INTERVAL

# This class is a thread that runs the health checks
class ServerHealthCheck(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.health_checks = [openai_health_check]

    def run(self):
        self.running = True
        while self.running:
            for health_check in self.health_checks:
                health_check()
            time.sleep(CHECK_INTERVAL)

    def stop(self):
        self.running = False

# Only one instance of the thread is allowed
shc_thread = None

router = APIRouter()

# This endpoint starts the thread
@router.get("/start")
async def shc_start():
    global shc_thread
    if shc_thread is None:
        shc_thread = ServerHealthCheck()
        shc_thread.start()
        return "Server Health Check: started"
    else:
        return "Server Health Check: already running"

# This endpoint stops the thread
@router.get("/stop")
async def shc_stop():
    global shc_thread
    if shc_thread is not None:
        shc_thread.stop()
        shc_thread.join()
        shc_thread = None
        return "Server Health Check: stopped"
    else:
        return "Server Health Check: not running"

# This endpoint returns the log records from the log file
@router.get("/logs")
async def shc_logs():
    file_path = "./health_check.log"
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            file_contents = file.readlines()
            return file_contents
    else:
        return "Server Health Check: file not found"
