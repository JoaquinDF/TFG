#!/usr/bin/env bash
GECKO_DRIVER="https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz";

set -e;

sudo apt-get install xvfb;

wget ${GECKO_DRIVER};
tar -xvzf geckodriver*.tar.gz;
chmod +x geckodriver;

sudo mv -f geckodriver /usr/local/share/geckodriver;
sudo ln -s -T -f /usr/local/share/geckodriver /usr/local/bin/geckodriver;
sudo ln -s -T -f /usr/local/share/geckodriver /usr/bin/geckodriver;

sudo rm -r geckodriver*.tar.gz
