
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
# Resolve dns:
import dns.resolver
# Selenium webdriver:
from selenium import webdriver
# Selenium webdriver Chrome:
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

###################################  Class  ###################################
###############################################################################
c = Counter('ErrorCount', 'Amount of mistakes')
with open('fronts.yml') as f:
    templates = yaml.safe_load(f)
    for key, value in templates['fronts'].items():
        key = Counter('ErrorCount_'+ key, 'Amount of mistakes for url' + key)

class LoggingRequests:

###############################################################################
##############################  Initializations  ##############################
###############################################################################
    #--------------------------------------------------------------------------
    # Class instance constructor
    #--------------------------------------------------------------------------
    def __init__(self,key,value,logger):

        self.Errors = 0

        self.Summ  = 0

    def request(self):
        try:
            result = dns.resolver.query(value[8:])
        except dns.resolver.NXDOMAIN:
            logger.info("ошибка домен не найден в списке DNS: ", value)
        else:
            try:
                rs = requests.get(value)
            except requests.ConnectionError:
                self.Errors+=1
                c.inc()
                key.inc()
                self.Summ+=1
                logger.info("ошибка подключения к url: ", value)
            except requests.Timeout:
                self.Errors+=1
                c.inc()
                key.inc()
                self.Summ+=1
                logger.info("ошибка timeout, url:", value)
            except requests.HTTPError as err:
                code = rs.status_code
                self.Errors+=1
                c.inc()
                key.inc()
                self.Summ+=1
                logger.info(f"ошибка url: {value}, code: {code}")
            except requests.RequestException:
                self.Errors+=1
                c.inc()
                key.inc()
                self.Summ+=1
                logger.info("ошибка скачивания url: ", value)
            except requests.TooManyRedirects:
                self.Errors+=1
                c.inc()
                key.inc()
                self.Summ+=1
                logger.info("ошибка слишком много обращений к url: ", value)
            else:
                code = rs.status_code
                self.Summ+=1
                logger.info(f"Запрос к url: {value} завершился с кодом: {code}")
                #  Open Chrom
                driver = Chrome('C:\Chromiuuus\chromedriver.exe')
                #  Go to url
                driver.get(value)
                driver.implicitly_wait(4)
                search_input = driver.find_element_by_id('login' or 'loginInput')
                if search_input:
                #  Input text
                    search_input.send_keys('Selenium')
                    search_input.send_keys(Keys.RETURN)
                else:
                    self.Errors+=1
                    c.inc()
                    key.inc()
                    self.Summ+=1
                    logger.info("ошибка сайт не отображается в браузере: ", value)


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
    # add handler to logger object

    logger = logging.getLogger("exampleApp")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    headfh = value[8:0]
    fh = logging.FileHandler(f"log-CDEK.log")

    logger.addHandler(fh)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # Initializations fronts.
    with open('fronts.yml') as f:
        templates = yaml.safe_load(f)
    for key, value in templates['fronts'].items():
        loging = LoggingRequests(key,value,logger)
        loging.request()


    # Count only one type of exception
    with c.count_exceptions(ValueError):
        pass
    # Start up the server to expose the metrics.
    start_http_server(8000)