from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import reverse_splitter.bin.logger as logger
import os
import reverse_splitter.jobs.research as research
import reverse_splitter.jobs.send_newsletter as send_newsletter
import reverse_splitter.jobs.add_new_subscribers as new_subs


log = logger.setup_logger('Scheduler')
scheduler = BackgroundScheduler()

CRON_RESEARCH = os.getenv('CRON_RESEARCH', '0 2 * * *')
CRON_NEWSLETTER = os.getenv('CRON_NEWSLETTER', '0 7 * * *')
CRON_ADD_NEW_SUBSCRIBERS = os.getenv('CRON_ADD_NEW_SUBSCRIBERS', '* * * * *')

def schedule_jobs():
    research_job = scheduler.add_job(research.research_job, CronTrigger.from_crontab(CRON_RESEARCH))
    newsletter_job = scheduler.add_job(send_newsletter.send_newsletter_job, CronTrigger.from_crontab(CRON_NEWSLETTER))
    subscribe_job = scheduler.add_job(new_subs.add_new_subscribers_job, CronTrigger.from_crontab(CRON_ADD_NEW_SUBSCRIBERS))
    log.debug('Jobs scheduled')
    
    return research_job, newsletter_job, subscribe_job

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
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()