#!/bin/bash

# Download selenium
mkdir -p selenium
rm -f ./selenium/selenium-server-standalone-3.12.0.jar
wget -P ./selenium/ https://selenium-release.storage.googleapis.com/3.12/selenium-server-standalone-3.12.0.jar

# Download and unpack chromedriver
rm -f ./selenium/chromedriver
rm -f ./selenium/chromedriver_linux64.zip
chromedriver_last_version=`curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -P ./selenium/ https://chromedriver.storage.googleapis.com/${chromedriver_last_version}/chromedriver_linux64.zip
unzip -d ./selenium/ ./selenium/chromedriver_linux64.zip
