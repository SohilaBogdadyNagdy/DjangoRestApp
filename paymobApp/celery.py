from celery.task.schedules import crontab
from celery.decorators import periodic_task

from paymobApp.api.utils import getRatesFromBaseCurrency

@periodic_task(run_every=(crontab(minute='*/15')), name="fetch_lastest_currencies_rates", ignore_result=True)
def fetch_lastest_currencies_rates():
    # do something
    print('inside celery task')
    data = getRatesFromBaseCurrency('USD')
    #set data into redius