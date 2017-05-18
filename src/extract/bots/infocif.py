from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from .bot import Bot
from utils.mongodb import Mongodb


class BotInstance(Bot):
    def run(self):
        organizations = []
        with Mongodb() as mongodb:
            db = mongodb.db
            collection = db.get_collection('crawlers.cdti.projects')
            for organization in collection.find({}):
                organizations.append(organization['nombre_empresa'])
        with Xvfb() as xvfb:
            url = 'http://www.infocif.es/'
            driver = webdriver.Chrome()
            for organization in organizations:
                driver.get(url)
                field = driver.find_element_by_id('txtempresabusquedaprincipal')
                field.clear()
                field.send_keys(organization)
                field.send_keys(Keys.RETURN)
                try:
                    row = driver.find_element_by_id('collapsecargos')
                except NoSuchElementException:
                    continue
                fields = ['other', 'matriz', 'administrador', 'n_empleados', 'sector', 'web', 'registro', 'telefono', 'domicilio', 'antiguedad', 'cif', 'nombre']
                lines = row.find_elements_by_xpath('.//h2[contains(@class, "text-right")]') + row.find_elements_by_xpath('.//p[contains(@class, "text-right")]')
                data = dict()
                data[fields.pop()] = organization
                for line in lines:
                    try:
                        span = line.find_element_by_xpath('.//span')
                        data[fields.pop()] = line.text.replace(span.text, '')
                    except NoSuchElementException:
                        data[fields.pop()] = line.text
                with Mongodb() as mongodb:
                    db = mongodb.db
                    collection = db.get_collection('bots.infocif.organizations')
                    collection.replace_one({'cif': data['cif']}, data, upsert=True)
            driver.close()
