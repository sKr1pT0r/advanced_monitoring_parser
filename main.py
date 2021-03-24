import requests
import sys
import pyfiglet
import json
from bs4 import BeautifulSoup
from colorama import Fore, init

arguments = {"without-aternos": False,
            "only-aternos": False,
            "only-default-port": False,
            "without-default-port": False,
            "nothing": True}

if str(sys.argv).find('--help') != -1:
    print('\n\npy main.py (Start page)-(End page) (Minecraft version) (Advanced options)')
    print('\nExample: py main.py 5-10 1.12.2 --without-aternos')
    print('Example: py main.py 1-100 all --only-default-port\n')
    print('Advanced options:')
    print('  --without-aternos       -  Display all servers except aternos.me')
    print('  --only-aternos          -  Display only servers aternos.me')
    print('  --only-default-port     -  Display only servers with a port 25565')
    print('  --without-default-port  -  Display all servers without a port 25565\n')
    exit()

elif str(sys.argv).find('--without-aternos') != -1 and str(sys.argv).find('--only-aternos') == -1:
    arguments["without-aternos"] = True
    arguments["nothing"] = False
elif str(sys.argv).find('--only-aternos') != -1 and str(sys.argv).find('--without-aternos') == -1:
    arguments["only-aternos"] = True
    arguments["nothing"] = False
elif str(sys.argv).find('--only-default-port') != -1 and str(sys.argv).find('--without-default-port') == -1:
    arguments["only-default-port"] = True
    arguments["nothing"] = False
elif str(sys.argv).find('--without-default-port') != -1 and str(sys.argv).find('--only-default-port') == -1 and str(sys.argv).find('--only-aternos') == -1:
    arguments["without-default-port"] = True
    arguments["nothing"] = False

def serverprint(i):
    print(soup.select('kbd')[i].text)
    out_file.write(soup.select('kbd')[i].text + '\n')

not_split_page_range = sys.argv[1].split('-')
start_page = int(not_split_page_range[0])
end_page = int(not_split_page_range[1])

minecraft_version = str(sys.argv[2])

out_file = open('out' + ' ' + str(start_page) + '-' + str(end_page) + '.txt', 'w')

pyfiglet.print_figlet('Advanced-MP', font='big')

for now_page in range(start_page,end_page + 1):
    if minecraft_version == 'all':
        page = requests.get('http://minecraftrating.ru/page/' + str(now_page))
    elif minecraft_version != 'all':
        page = requests.get('http://minecraftrating.ru/servera-' + minecraft_version + '/page/' + str(now_page))

    soup = BeautifulSoup(page.content, 'html.parser')
    
    print('-' * 30)
    print('Now page:', now_page)
    print('IP addresses found: ', len(soup.select('kbd')))
    print('-' * 30)

    for i in range(0,len(soup.select('kbd'))):     
        if arguments["nothing"] == True:
            serverprint(i)
        elif arguments["without-aternos"] == True and str(soup.select('kbd')[i].text).find('aternos.me') == -1 and arguments["nothing"] == False: 
            serverprint(i)
        elif arguments["only-aternos"] == True and str(soup.select('kbd')[i].text).find('aternos.me') != -1 and arguments["nothing"] == False:
            serverprint(i)
        elif arguments["without-default-port"] == True and soup.select('kbd')[i].text.split(':')[1] != '25565':
            serverprint(i)
        elif arguments["only-default-port"] == True and soup.select('kbd')[i].text.split(':')[1] == '25565':
            serverprint(i)
out_file.close()