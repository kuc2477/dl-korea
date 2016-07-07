class CronFormatError(Exception):
    def __init__(self, cron):
        self.message = 'Invalid cron format: {}'.format(cron)
