import requests
from bs4 import BeautifulSoup

team_name = "barcelona"  # Replace with the desired team name

search_url = f"https://www.sofascore.ro/search/teams/football/{team_name}"
response = requests.get(search_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    team_link = soup.find('a', class_='entity-link--team')

    if team_link:
        team_url = team_link['href']
        print("Team URL:", team_url)
    else:
        print("Team not found.")
else:
    print("Error retrieving search results.")