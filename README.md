# Vulnerawebity

## Simple tool for checking web vulnerabilities

### First you need to install some dependancies:

```python
pip3 install selenium
```

```python
pip3 install bs4
```

```python 
pip install requests
```

### You will need also to download the geckodriver.
#### For linux
```python
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.26.0-linux64.tar.gz -O > /usr/bin/geckodriver'
sudo chmod +x /usr/bin/geckodriver
rm geckodriver-v0.26.0-linux64.tar.gz
```
#### For windows
Uninstall windows and follow the linux instructions
