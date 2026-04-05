from apscheduler.schedulers.blocking import BlockingScheduler
from main import run

def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(run, "cron", hour=18, minute=0, timezone="America/New_York")
    print("Scheduler iniciado. Esperando las 18:00 EST...")
    scheduler.start()