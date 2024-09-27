from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import reverse_splitter.bin.logger as logger
import os
import reverse_splitter.jobs.research as research
import reverse_splitter.jobs.send_newsletter as send_newsletter


log = logger.setup_logger('Scheduler')
scheduler = BackgroundScheduler()

RESEARCH_CRON = os.getenv('RESEARCH_CRON', '0 2 * * *')
NEWSLETTER_CRON = os.getenv('NEWSLETTER_CRON', '0 7 * * *')

def schedule_jobs():
    research_job = scheduler.add_job(research.research_job, CronTrigger.from_crontab(RESEARCH_CRON))
    newsletter_job = scheduler.add_job(send_newsletter.send_newsletter_job, CronTrigger.from_crontab(NEWSLETTER_CRON))
    log.debug('Jobs scheduled')
    
    return research_job, newsletter_job

if __name__ == '__main__':
    from datetime import datetime
    import time
    def tick():
        print('Tick! The time is: %s' % datetime.now())
        
    tick_job = scheduler.add_job(tick, CronTrigger.from_crontab('* * * * *'))
    scheduler.start()
    print('Next tick job scheduled at', tick_job.next_run_time)
    
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        print('Press Ctrl+C to exit')
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()