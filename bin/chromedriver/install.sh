#!/usr/bin/env bash

CHROME="https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
CHROME_DRIVER="https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip"

set -e

sudo apt-get install libxss1 libappindicator1 libindicator7
wget ${CHROME}

sudo dpkg -i google-chrome*.deb
sudo apt-get install -f

sudo apt-get install xvfb

sudo apt-get install unzip

wget -N ${CHROME_DRIVER}
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s -T -f /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s -T -f /usr/local/share/chromedriver /usr/bin/chromedriver

sudo rm -r google-chrome*.deb
sudo rm -r chromedriver_linux64.zip
