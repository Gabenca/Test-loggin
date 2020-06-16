
##################################  Imports  ##################################
###############################################################################


# HTTP requests:
import requests
# Logging:
import logging
# Prometheus instrumenting:
from prometheus_client import start_http_server, Summary, Counter
# Random:
import random
# Time:
import time
# Yaml reader:
import yaml

###################################  Class  ###################################
###############################################################################
c = Counter('ErrorCount', 'Amount of mistakes')

class LoggingRequests:

###############################################################################
##############################  Initializations  ##############################
###############################################################################
    #--------------------------------------------------------------------------
    # Class instance constructor
    #--------------------------------------------------------------------------
    def __init__(self,
        url):

        self.Errors

        self.Summ

        def _request(self, url):
            logger = logging.getLogger("exampleApp")
            logger.setLevel(logging.INFO)

            # create the logging file handler
            headfh = url[8:-1]
            fh = logging.FileHandler(f"log-{headfh}.log")

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            # add handler to logger object
            logger.addHandler(fh)
            try:
                rs = requests.get(url)
            except requests.ConnectionError:
                self.Errors+=1
                c.inc()
                self.Summ+=1
                logger.info("ошибка подключения к url: ", url)
            except requests.Timeout:
                self.Errors+=1
                c.inc()
                self.Summ+=1
                logger.info("ошибка timeout, url:", url)
            except requests.HTTPError as err:
                code = rs.status_code
                self.Errors+=1
                c.inc()
                self.Summ+=1
                logger.info(f"ошибка url: {url}, code: {code}")
            except requests.RequestException:
                self.Errors+=1
                c.inc()
                self.Summ+=1
                logger.info("ошибка скачивания url: ", url)
            except requests.TooManyRedirects:
                self.Errors+=1
                c.inc()
                self.Summ+=1
                logger.info("ошибка слишком много обращений к url: ", url)
            else:
                code = rs.status_code
                self.Summ+=1
                logger.info(f"Запрос к url: {url} завершился с кодом: {code}")

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time."""
    time.sleep(t)

@c.count_exceptions()
def f():
  pass


###################################  Main  ####################################
###############################################################################

if __name__ == '__main__':
    # Initializations fronts.
    with open('fronts.yml') as f:
        templates = yaml.safe_load(f)
    for key, value in templates['fronts'].items():
        print(value)

    # Count only one type of exception
    with c.count_exceptions(ValueError):
        pass
    # Start up the server to expose the metrics.
    start_http_server(8000)