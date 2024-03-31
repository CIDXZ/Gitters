import requests
from bs4 import BeautifulSoup
import tkinter as tk

def get_race_info():
    url = "https://www.bing.com/sportsdetails?q=Bahrain%20Grand%20Prix%20Formula%201&gameid=SportRadar_Racing_Formula1_2024_Game_1107549&league=Racing_Formula1&scenario=GameCenter&intent=Game&iscelebratedgame=True&TimezoneId=India%20Standard%20Time&sport=MotorRacing&seasonyear=2024&venueid={%22id%22:%22SportRadar_Racing_Formula1_2024_Venue_1013%22}:version-1&segment=sports&isl2=true&IsAutoRefreshEnabled=true&&PC=DCTS"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print HTML content for inspection
    print(soup.prettify())
    
    # Extracting score and player names
    scores = []
    player_names = []
    for score_div in soup.find_all('div', class_='score-line'):
        score_text = score_div.get_text().strip()
        scores.append(score_text)
    
    for player_div in soup.find_all('div', class_='team-name'):
        player_text = player_div.get_text().strip()
        player_names.append(player_text)
    
    return scores, player_names

def update_display():
    scores, player_names = get_race_info()
    score_text = "\n".join(scores)
    player_text = "\n".join(player_names)
    score_label.config(text=score_text)
    player_label.config(text=player_text)
    root.after(5000, update_display)  # Refresh every 5 seconds

# Create tkinter GUI
root = tk.Tk()
root.title("Formula One Racing Score")

# Labels for displaying scores and player names
score_label = tk.Label(root, text="", font=("Arial", 12))
score_label.pack()

player_label = tk.Label(root, text="", font=("Arial", 12))
player_label.pack()

# Start updating display
update_display()

root.mainloop()



