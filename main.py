from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from sys import argv, exit
import getopt
from spinner import Spinner


class Island:
    def __init__(self, card, bells, queue):
        self.card = card
        self.bells = bells
        self.queue = queue
        self.rating = bells / (queue if queue != 0 else 1)


def connect(driverPath, site='https://turnip.exchange/islands'):
    """
    Returns the driver initialized

    Function that setups the driver and opens the site in background
    At the moment supports only chrome drivers

    Parameters
    ----------
    driverPath : str
        path of the driver to use
    site : str
        URL of the site to scrap

    Returns
    -------
    WebDriver
        selenium driver initialized

    """
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(
        executable_path=driverPath, options=options)
    driver.get(site)
    print("Driver initialized and site reached")
    return driver


def getIslands(driver):
    """
    Returns the list of all the islands

    Function that creates an Island object scraping bells
    and queue informations and that appends it in a list

    Parameters
    ----------
    driver : WebDriver
        the driver initialized

    Returns
    -------
    list
        list of Island objects

    """
    sleep(5)
    cards = driver.find_elements_by_class_name('note')
    islands = []
    for card in cards:
        fields = card.find_elements_by_tag_name('p')
        bells = fields[1].text[:-
                               6] if len(fields) == 5 else fields[0].text[:-6]
        queue = fields[4].text[9:] if len(fields) == 5 else fields[3].text[9:]
        island = Island(card, int(bells), int(queue))
        islands.append(island)
    print("Found " + str(len(islands)) + " islands")
    return islands


def getBestN(islands, n):
    return sorted(islands, key=lambda island: island.rating)[-n:]


def getBestPrice(islands):
    return sorted(islands, key=lambda island: island.bells)[-1]


def startQueue(driver, island, name):
    """
    Joins the queue of a given island

    Function that joins the queue and
    registers the user nickname

    Parameters
    ----------
    driver : WebDriver
        the driver initialized
    island : Island
        island to join
    name : str
        user nickname

    Returns
    -------
    bool
        false if something is gone wrong keks

    """
    print("Island selected:")
    print("- Turnip price: " + str(island.bells))
    print("- Peoples in queue: " + str(island.queue))
    island = island.card
    island.click()
    sleep(5)
    try:
        driver.find_element_by_class_name('bg-info').click()
    except:
        pass
    sleep(5)
    button = driver.find_element_by_xpath(
        '//*[@id="app"]/div[2]/div[3]/div/button')

    if button.text == "Join this queue":
        button.click()
        driver.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[1]/div/input').send_keys(name)
        driver.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[1]/div/div/button[2]').click()
        print("Queue joined")
        return True
    else:
        print("An error occurred during the joining to the queue")
        return False


def getCode(driver):
    """
    Returns the island code

    Recursive function that if the queue is ended, gets and returns
    the island's code, otherwise recalls itself
    Use it after a startQueue() function because it assumes to be in that page

    Parameters
    ----------
    driver : WebDriver
        the driver initialized

    Returns
    -------
    str
        island's code

    """
    sleep(10)
    try:
        banner = driver.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[3]/div[2]/div[2]')
        return getCode(driver)
    except:
        sleep(5)
        banner = driver.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[3]/div[2]')
        banner.find_element_by_class_name('uppercase').click()
        sleep(5)
        return driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/p[2]').text


if __name__ == '__main__':
    driverPath, name = '', ''

    try:
        opts, args = getopt.getopt(argv[1:], "hd:n:", ["driverPath=", "name="])
    except getopt.GetoptError:
        print('main.py -d <driverPath> -n <name>')
        exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <driverPath> -n <name>')
            exit()
        elif opt in ("-d", "--driverPath"):
            driverPath = arg
        elif opt in ("-n", "--name"):
            name = arg

    print("Driver path selected: " + driverPath)
    print("Name selected: " + name)
    driver = connect(driverPath)
    if (startQueue(driver, getBestPrice(getBestN(getIslands(driver), 5)), name)):
        with Spinner():
            print("\n\nThe island code is: " + getCode(driver))
    driver.quit()
