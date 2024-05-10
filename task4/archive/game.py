from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv



# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# deze file uitvoeren in een terminal: python3 game.py
# in een andere terminal, run je je agent
# en vervang de link hieronder met die van je agent
# en vervang de andere link naar een andere agent. 
 
# INFO : 
# commando om 1 keer uit te voeren : npm install -g localtunnel
# commando om dit file uit te voeren : ./websocket_player.py dotsandboxes_agent 8080  

# Ibrahim : 
# website : https://people.cs.kuleuven.be/~wannes.meert/dotsandboxes/dotsandboxes.html
# temporary link : https://tender-lies-drum.loca.lt/
# ip address : 193.190.253.145


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------






def game_ended(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    playing_area = soup.find('div', id='playing-area')

    player_points = {}
    for text_element in playing_area.find_all('text'):
        player_data = text_element.get_text().split(':')
        player_name = player_data[0].strip()
        points = int(player_data[1].strip())
        player_points[player_name] = points

    nb_rows = int(driver.find_element(By.ID, "nb-rows").get_attribute("value"))
    nb_cols = int(driver.find_element(By.ID, "nb-cols").get_attribute("value"))

    total_points = sum(player_points.values())
    total_cells = nb_rows * nb_cols
    return total_points == total_cells, player_points

with open("game.html", "r") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
agent1_ws = "ws://cool-worlds-dance.loca.lt"
agent2_ws = "ws://puny-hoops-do.loca.lt"
soup.find("input", {"id": "agent1"})["value"] = agent1_ws
soup.find("input", {"id": "agent2"})["value"] = agent2_ws

with open("game.html", "w") as f:
    f.write(str(soup))

url = "file:///home/ibrahim/Documents/KuLeuven/Engineering/Master/1e_fase/2e_semester/Machine_Learning_Project/MARL/task4/game.html"
driver = webdriver.Chrome() 
driver.get(url)

for _ in range(50):
    restart_button = driver.find_element(By.ID, "restart-btn")
    restart_button.click()

    b, d = game_ended(driver)
    while not b:
        # kan korter indien nodig:
        time.sleep(1)
        b, d = game_ended(driver)

    with open('points_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['Player', 'Points'])

        for player, points in d.items():
            writer.writerow([player, points])

driver.quit()
