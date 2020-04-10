# What is turnipScraper?
`turnipScraper` is a Python scraper for [Turnip Exchange](https://turnip.exchange/) that helps to find the best island to sell turnip in Animal Crossing New Horizon

# Features
- Headless process
- Easy research for available islands
- Evaluation of the worthiness of islands 
- Classification of islands
- Automatic queue waiting

# Installation
- Download the latest python version from the [official site](https://www.python.org/downloads/) for Windows users or from your system package manager for Linux users
- Download the selenium package 
```python
pip install -U selenium
```
- Make sure to have chrome browser (at the moment supports only chrome) otherwise download it from the [official site](https://www.google.com/intl/it_it/chrome/)
- Download the chromedriver for your chrome version from the [official site](https://chromedriver.chromium.org/downloads)

# How to use it
- From a terminal go to the cloned directory
- Start the island research with the following command, passing as parameters the path of your driver and your in-game nickname
```bash
main.py -d <driverPath> -n <name>
```