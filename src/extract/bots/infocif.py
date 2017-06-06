import logging
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .bot import Bot
from utils.mongodb import Mongodb


class BotInstance(Bot):
    def run(self):
        organizations = []
        stop_words = ['-', 'No facilitada']
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = db['crawlers.cdti.projects']
            for organization in collection.find({}):
                organizations.append(organization['nombre_empresa'])

            xvfb = Xvfb()
            xvfb.start()
            url = 'http://www.infocif.es/'
            driver = webdriver.Chrome()

            collection = db['bots.infocif.organizations']
            bulk = collection.initialize_ordered_bulk_op()

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
                    fields = ['other', 'matriz', 'administrador', 'n_empleados', 'sector', 'web', 'registro', 'telefono', 'domicilio', 'antiguedad', 'cif', 'nombre']
                    lines = row.find_elements_by_xpath('.//h2[contains(@class, "text-right")]') + row.find_elements_by_xpath('.//p[contains(@class, "text-right")]')
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
                                    data[fields.pop()] = s[0] + ';' + s[1] + ';' + s[2].split('- ')[-1]
                                else:
                                    data[fields.pop()] = text

                    bulk.find({'cif': data['cif']}).upsert().replace_one(data)

                bulk.execute()
            finally:
                driver.quit()
                xvfb.stop()

        return True
