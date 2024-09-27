import jobs.scheduler as scheduler
import bin.logger as logger
import time

log = logger.setup_logger('Main')

def main():
    jobs = scheduler.schedule_jobs()
    scheduler.scheduler.start()
    log.info(f'Next research job scheduled for {jobs[0].next_run_time}')
    log.info(f'Next newsletter job scheduled for {jobs[1].next_run_time}')
    log.info(f'Next welcome job scheduled for {jobs[2].next_run_time}')
    
    try:
        log.debug('Entering infinite loop')
        log.debug('Press Ctrl+C to exit')
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        log.debug('Shutting down...')
        scheduler.scheduler.shutdown()




if __name__ == '__main__':
    main()