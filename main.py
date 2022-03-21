import requests
from bs4 import BeautifulSoup



steam_link='https://steamcommunity.com/market/listings/570/'
items_link='https://www.dotaweb.com/en/store/'

heroes = ['abaddon', 'alchemist', 'ancient-apparition', 'anti-mage', 'arc-warden', 'axe', 'bane', 'batrider',
          'beastmaster', 'bloodseeker', 'bounty-hunter',
          'brewmaster', 'bristleback', 'broodmother', 'centaur-warrunner',
          'chaos-knight', 'chen', 'clinkz', 'clockwerk', 'crystal-maiden', 'dark-seer', 'dark-willow', 'dazzle',
          'death-prophet', 'disruptor', 'doom', 'dragon-knight',
          'drow-ranger', 'earth-spirit', 'earthshaker', 'elder-titan', 'ember-spirit', 'enchantress', 'enigma',
          'grimstroke', 'gyrocopter', 'huskar', 'invoker', 'jakiro', 'juggernaut', 'keeper-of-the-light', 'kunkka',
          'legion-commander', 'leshrac', 'lich',
          'lifestealer', 'lina', 'lion', 'lone-druid', 'luna',
          'lycan', 'magnus', 'medusa', 'meepo', 'mirana', 'monkey-king', 'morphling', 'naga-siren', 'natures-prophet',
          'necrophos', 'night-stalker', 'nyx-assassin',
          'ogre-magi', 'omniknight',
          'oracle', 'outworld-devourer', 'pangolier', 'phantom-assassin', 'phantom-lancer', 'phoenix', 'puck', 'pudge',
          'pugna', 'queen-of-pain', 'razor', 'riki', 'rubick',
          'sand-king', 'shadow-demon', 'shadow-fiend',
          'shadow-shaman', 'silencer', 'skywrath-mage', 'slardar', 'slark', 'sniper', 'spectre', 'spirit-breaker',
          'storm-spirit', 'sven', 'techies',
          'templar-assassin', 'terrorblade', 'tidehunter', 'timbersaw', 'tinker', 'tiny', 'treant-protector',
          'troll-warlord', 'tusk', 'underlord',
          'undying', 'ursa', 'vengeful-spirit', 'venomancer', 'viper', 'visage', 'warlock', 'weaver', 'windranger',
          'winter-wyvern', 'witch-doctor', 'wraith-king', 'zeus', 'faceless-void']

headers = {'Cookie':'ActListPageSize=10; timezoneOffset=10800,0; steamMachineAuth76561198154056380=9FA18B4F28A3962D66631B7F7848569ED4FC30AD; browserid=2424629783349362335; _ga=GA1.2.1335292428.1646068412; cookieSettings={"version":1,"preference_state":1,"content_customization":null,"valve_analytics":null,"third_party_analytics":null,"third_party_content":null,"utm_enabled":true}; recentlyVisitedAppHubs=1079200; steamRememberLogin=76561198154056380||470914c5b6b079d453b117ff7f964d1e; strInventoryLastContext=730_2; _gid=GA1.2.520696773.1647453176; sessionid=44b69e616cb76818ca7e1afb; steamLoginSecure=76561198154056380||04D4CB50D35D6C78784E184D4B97E623F2AA9F04; webTradeEligibility={"allowed":1,"allowed_at_time":0,"steamguard_required_days":15,"new_device_cooldown_days":7,"time_checked":1647494918}; steamCountry=RU|8e7a56e73cbd549bbf19e8061cafecfe' }
stonks=[]


def all_items_finder(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    want = soup.find_all('a', {"title": True})
    hrefs = []
    for x in want:
        if ((x.get('title')).find("Items Skins") < 1):
            hrefs.append(x.get('href'))

    return hrefs

def set_finder(href):
    wanted = []
    newurl = href
    response1 = requests.get(newurl)
    soup_sets = BeautifulSoup(response1.text, 'lxml')
    quotes = soup_sets.find_all('img', {'alt': True})
    for i in quotes:
        attribute = i.get('alt')[:-9]
        wanted.append(attribute)
    wanted.pop(-1)

    return wanted

def price_finder(set_names):
    wanted = []
    prices = []
    best_price=[]
    clone=set_names
    sum=0.0
    for k in range(len(clone)):
        newurl = steam_link + clone[k]
        response = requests.get(newurl, headers=headers)
        soup_price = BeautifulSoup(response.text, 'lxml')
        quotes = soup_price.find_all('span', {'class': 'market_listing_price market_listing_price_with_fee'})
        if len(quotes)>0:
            for i in quotes:
                wanted.append(i.text.strip()[:-5])

            for x in wanted:
                a = x.replace(",", ".")
                if(len(x)>0):
                    prices.append(float(a))

            prices.sort()
            if len(prices)>0:
                best_price.append(prices[0])
            print(clone[k])
            print(best_price)
            prices = []
            wanted=[]

            continue
        else:
            if k==0:
                break
            continue
    for p in range(1,len(best_price)):
        sum+=best_price[p]
    sum-= sum*0.13
    if len(best_price)>0:
        sum -= best_price[0]
    print(sum)
    return sum






for iter in heroes:

    print(f"I am checkin'   {iter}")
    url = items_link
    url += iter
    hrefs = all_items_finder(url)
    for i in hrefs:

        sets_names = set_finder(i)
        print(sets_names)
        if len(sets_names)>1:
            name=sets_names[0]
            print(sets_names)
            stonks=price_finder(sets_names)

            if(stonks>1):
                print(f"FOUND STONKS: {stonks} | {name}")
                with open("stonks.txt", "a") as file:
                    file.write(f"FOUND STONKS: {stonks} | {name}  \n")




file.close()



