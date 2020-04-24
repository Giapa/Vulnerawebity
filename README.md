# Vulnerawebity

## Simple tool for checking web vulnerabilities

### First you need to install some dependancies:

```bash
pip install selenium
```
```bash
pip install bs4
```
```bash 
pip install requests
```

### You will need also to download the geckodriver.
#### For linux
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
```
```bash
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.26.0-linux64.tar.gz -O > /usr/bin/geckodriver'
```
```bash
sudo chmod +x /usr/bin/geckodriver
```
```bash
rm geckodriver-v0.26.0-linux64.tar.gz
```
#### For windows
Uninstall windows and follow the linux instructions
