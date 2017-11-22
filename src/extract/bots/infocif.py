import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from xvfbwrapper import Xvfb

from utils.bot import Bot


class BotInstance(Bot):
    collection = 'bots.infocif.organizations'
    key = 'cif'

    def process_item(self, db=None):
        stop_words = ['-', 'No facilitada']
        collections = [
            ('crawlers.cdti.projects', 'nombre_empresa'),
            ('bots.cdti.projects', 'Entidad')
        ]

        organizations = set()
        for k, v in collections:
            organizations = organizations.union(db[k].distinct(v))

        xvfb = Xvfb()
        xvfb.start()
        url = 'http://www.infocif.es/'
        driver = webdriver.Chrome()

        try:
            for organization in organizations:
                driver.get(url)
                try:
                    field = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.ID, "txtempresabusquedaprincipal"))
                    )
                except TimeoutException as e:
                    logging.debug(e.msg)
                    continue
                field.clear()
                field.send_keys(organization)
                field.send_keys(Keys.RETURN)
                try:
                    row = WebDriverWait(driver, 10).until(
                        ec.presence_of_element_located((By.ID, "collapsecargos"))
                    )
                except TimeoutException as e:
                    logging.debug(e.msg)
                    continue
                lines = row.find_elements_by_xpath('.//h2[contains(@class, "text-right")]') + row.find_elements_by_xpath('.//p[contains(@class, "text-right")]')
                fields = ['other', 'matriz', 'administrador', 'n_empleados', 'sector', 'web', 'registro', 'telefono', 'ciudad', 'cp', 'calle', 'antiguedad', 'cif', 'nombre']
                data = dict()
                data[fields.pop()] = organization
                for line in lines:
                    try:
                        span = line.find_element_by_xpath('.//span')
                        text = line.text.replace(span.text, '')
                    except NoSuchElementException as e:
                        logging.debug(e.msg)
                        text = line.text
                    finally:
                        if text in stop_words:
                            data[fields.pop()] = None
                        else:
                            s = text.split('  ')
                            if len(s) == 3:
                                data[fields.pop()] = s[0]
                                data[fields.pop()] = s[1]
                                data[fields.pop()] = s[2].split('- ')[-1]
                            else:
                                data[fields.pop()] = text
                yield data

        finally:
            driver.quit()
            xvfb.stop()
