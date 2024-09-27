from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import reverse_splitter.bin.logger as logger
import os
from . import research, send_newsletter


log = logger.setup_logger('Scheduler')
scheduler = BackgroundScheduler()

RESEARCH_CRON = os.getenv('RESEARCH_CRON', '0 2 * * *')
NEWSLETTER_CRON = os.getenv('NEWSLETTER_CRON', '0 7 * * *')

def schedule_jobs():
    scheduler.add_job(research.research_job, CronTrigger.from_crontab(RESEARCH_CRON))
    scheduler.add_job(send_newsletter.send_newsletter_job, CronTrigger.from_crontab(NEWSLETTER_CRON))
    log.debug('Jobs scheduled')
    
    

if __name__ == '__main__':
    from datetime import datetime
    import time
    def tick():
        print('Tick! The time is: %s' % datetime.now())
        
    scheduler.add_job(tick, CronTrigger.from_crontab('* * * * *'))
    scheduler.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        print('Press Ctrl+C to exit')
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()