import jobs.scheduler as scheduler
import bin.logger as logger

log = logger.setup_logger('Main')

def main():
    scheduler.schedule_jobs()
    scheduler.scheduler.start()
    try:
        log.debug('Entering infinite loop')
        log.debug('Press Ctrl+C to exit')
        while True:
            pass
    except KeyboardInterrupt:
        log.debug('Shutting down...')
        scheduler.scheduler.shutdown()




if __name__ == '__main__':
    main()