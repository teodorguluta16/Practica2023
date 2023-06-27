import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import streamlit as st

st.set_page_config(page_title="Football", page_icon=":soccer:", layout="wide")
st.title("Football :soccer:")
st.markdown("##")


coduri=[]
optiuni=['-']

def atribuie():
    file_path = r'C:\Users\Teo G\Desktop\proiect2\coduri.txt'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        values = line.split()
        coduri.append((values[0], int(values[1])))
        optiuni.append(values[0])
atribuie()


selected_option = st.selectbox("Alege o echipa/campionat", optiuni)

for ops in optiuni:
    if ops==selected_option:
        if(ops != '-'):
            if ops[0]!='_':
                sir = "Informatii esentiale despre " + ops
                size = 30
                st.markdown(f'<span style="color: blue; font-weight: bold; font-size: {size}px">{sir}</span>',
                            unsafe_allow_html=True)

                cod=-1
                for it in coduri:
                    nume_cautat=it[0]
                    id_cautat=it[1]
                    if nume_cautat==ops:
                        cod=id_cautat
                        break

                url = "https://www.sofascore.ro/team/football/{}/{}/".format(ops, cod)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                country_element = soup.select_one('.sc-ksBlkl.iFbjBC')
                country = country_element.get('alt') if country_element else 'N/A'
                text="Country:"
                st.markdown(f'<span style="color: yellow; font-weight: bold;">{text}</span>', unsafe_allow_html=True)
                st.write(country)

                image_url = 'https://www.sofascore.ro' + country_element['src'] if country_element else ''

                if image_url:
                    response = requests.get(image_url)
                    st.image(response.content, caption=country, width=56)

                div_tags = soup.find_all('div', class_='sc-bqWxrE dmCjif')
                league_names = [div.text for div in div_tags]
                txt="Current championships "
                st.markdown(f'<span style="color: yellow; font-weight: bold;">{txt}</span>', unsafe_allow_html=True)
                st.write(league_names[0],', ', league_names[1])
                txt = "Current standings in: "
                st.markdown(f'<span style="color: yellow; font-weight: bold;">{txt}</span>', unsafe_allow_html=True)
                st.write(league_names[1])

                div_tags = soup.find_all('div', class_='sc-993a7cdc-0 vjMQM')
                h2_elements = div_tags[0].find_all('h2')
                p_elements=div_tags[0].find_all('p')
                cnt=0
                for h2_element in h2_elements:
                    h2_text = h2_element.get_text()
                    p_text=p_elements[cnt+1].get_text()
                    st.markdown(f'<span style="color: yellow; font-weight: bold;">{h2_text}</span>', unsafe_allow_html=True)
                    if cnt == 1:
                        p_text = p_elements[cnt + 3].get_text()
                    if cnt == 2:
                        p_text = p_elements[cnt + 7].get_text()
                    st.write(p_text)
                    cnt=cnt+1
                    if cnt == 3:
                        break

                span_elements=soup.find_all('div',class_='sc-bqWxrE bhDRBv')
                span_text=span_elements[0].get_text()
                st.markdown(f'<span style="color: green; font-weight: bold;">{span_text}</span>', unsafe_allow_html=True)

                span_elements=soup.find_all('div',class_='sc-hLBbgP ixIhqb')
                span_text = span_elements[0].get_text()
                result = ""
                for index, char in enumerate(span_text):
                    if char.isupper():
                        if span_text[index-1].isalpha():
                                result =result+" * "
                    result += char
                span_text=result
                st.write(span_text)

                span_elements=soup.find_all('div',class_='sc-bqWxrE loRMgI')
                span_text = span_elements[0].get_text()
                st.markdown(f'<span style="color: red; font-weight: bold;">{span_text}</span>', unsafe_allow_html=True)

                span_elements=soup.find_all('div',class_='sc-hLBbgP ixIhqb')
                span_text = span_elements[1].get_text()
                result = ""
                for index, char in enumerate(span_text):
                    if char.isupper():
                        if span_text[index - 1].isalpha():
                            result = result + " * "
                    result += char
                span_text = result
                st.write(span_text)
            else:
                cod = -1
                for it in coduri:
                    nume_cautat = it[0]
                    id_cautat = it[1]
                    if nume_cautat == ops:
                        cod = id_cautat
                        break
                new_string = ops[1:]
                ops=new_string
                sir = "Informatii esentiale despre " + ops
                size = 30
                st.markdown(f'<span style="color: blue; font-weight: bold; font-size: {size}px">{sir}</span>',
                            unsafe_allow_html=True)


                url = 'https://fbref.com/en/comps/{}/{}-Stats'.format(cod,ops)
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'id': 'results2022-2023{}1_overall'.format(cod)})

                rankings = []
                teams = []
                matches_played = []
                wins = []
                draws = []
                losses = []
                goals_for = []
                goals_against = []
                goal_diffs = []
                points = []
                points_match = []
                xG = []
                xGA = []
                xGD = []
                xGD90 = []
                top_goals = []
                notes = []
                team_logos = []
                spectators= []
                rows = table.find_all('tr')
                for row in rows[1:]:
                    columns = row.find_all('td')
                    teams.append(columns[0].text.strip())
                    matches_played.append(columns[1].text.strip())
                    wins.append(columns[2].text.strip())
                    draws.append(columns[3].text.strip())
                    losses.append(columns[4].text.strip())
                    goals_for.append(columns[5].text.strip())
                    goals_against.append(columns[6].text.strip())
                    goal_diffs.append(columns[7].text.strip())
                    points.append(columns[8].text.strip())
                    points_match.append(columns[9].text.strip())
                    xG.append(columns[10].text.strip())
                    xGA.append(columns[11].text.strip())
                    xGD.append(columns[12].text.strip())
                    xGD90.append(columns[13].text.strip())
                    spectators.append(columns[14].text.strip())
                    top_goals.append(columns[15].text.strip())
                    notes.append(columns[16].text.strip())

                    logo_url = columns[0].find('img')['src']
                    team_logos.append(logo_url)

                row_indices = list(range(1, len(teams) + 1))
                data = {
                    'Rank': row_indices,
                    'Team': teams,
                    'Matches Played': matches_played,
                    'Wins': wins,
                    'Draws': draws,
                    'Losses': losses,
                    'Goals For': goals_for,
                    'Goals Against': goals_against,
                    'Goal Difference': goal_diffs,
                    'Points': points,
                }

                data2={
                    'Rank': row_indices,
                    'Team': teams,
                    'Matches Played': matches_played,
                    'Wins': wins,
                    'Draws': draws,
                    'Losses': losses,
                    'Goals For': goals_for,
                    'Goals Against': goals_against,
                    'Goal Difference': goal_diffs,
                    'Points': points,
                    'Point/match':points_match,
                    'xG':xG,
                    'xGA':xGA,
                    'xGD':xGD,
                    'xGD90':xGD90,
                    'Spectators':spectators,
                    'Top_goals':top_goals,
                    'Notes':notes
                }
                df = pd.DataFrame(data)
                styled_table = df.style.applymap(lambda x: 'color: green; background-color: yellow')


                df2 = pd.DataFrame(data2)

                df2.to_excel("Championship Ranking.xlsx")

                goluri = [int(num) for num in goals_for]  # Convert string numbers to integers
                sum = sum(goluri)
                average = sum / len(goluri)

                top_maractori = []
                topNrgoluri = []

                for scorer in top_goals:
                    numbers = [int(s) for s in scorer.split() if s.isdigit()]
                    print(numbers)
                    topNrgoluri.append(numbers)
                    nume = scorer.split("-")[0].strip()
                    top_maractori.append(nume)

                max_number = max(topNrgoluri)
                marcator = ""
                for index, string in enumerate(topNrgoluri):
                    if topNrgoluri[index] == max_number:
                        marcator = top_maractori[index]
                        break

                most_assists_element = soup.find('strong', text='Most Assists')
                if most_assists_element:
                    most_assists_text = most_assists_element.find_next_sibling('a').text + "  " + most_assists_element.find_next_sibling('span').text

                most_clean_sheets_element = soup.find('strong',text='Most Clean Sheets')
                if most_clean_sheets_element:
                    most_sheets_text = most_clean_sheets_element.find_next_sibling('a').text + "  " + most_clean_sheets_element.find_next_sibling('span').text

                champion_element = soup.find('strong', text='Champion')
                if champion_element:
                    champion_info = champion_element.find_next('a').text

                logo_element = soup.find('img', class_='teamlogo')
                if logo_element:
                    logo_url = logo_element['src']
                st.image(logo_url)

                champion_logo_element = soup.find('p', string="Champion")
                if champion_logo_element:
                    logo_element = champion_logo_element.find_previous('img', class_='teamlogo')
                    if logo_element:
                        logo_url = logo_element['src']
                left_column, middle_column, right_column = st.columns(3)
                with left_column:
                    st.markdown("<h3 style='color: yellow;'>Total goals:</h3>", unsafe_allow_html=True)
                    st.subheader(str(sum))
                    st.markdown("<h3 style='color: yellow;'>Nr goals/per stage:</h3>", unsafe_allow_html=True)
                    st.subheader(str(average))
                with middle_column:
                    st.markdown("<h3 style='color: yellow;'>The best player scorer:</h3>", unsafe_allow_html=True)
                    st.subheader(marcator + " " + str(max_number[0]))
                    st.markdown("<h3 style='color: yellow;'>Most Assists:</h3>", unsafe_allow_html=True)
                    st.subheader(most_assists_text)
                with right_column:
                    st.markdown("<h3 style='color: yellow;'>Most clean sheets:</h3>", unsafe_allow_html=True)
                    st.subheader(most_sheets_text)
                    st.markdown("<h3 style='color: yellow;'>Champion:</h3>", unsafe_allow_html=True)
                    st.subheader(champion_info)
                    st.image(team_logos[0])

                st.markdown("""---""")

                st.table(styled_table)

                import matplotlib.pyplot as plt

                short_name_teams=[]
                for team in teams:
                    result = team.split()[0]
                    short_name_teams.append(result)
                int_spec = []
                for string in spectators:
                    string_without_comma = ''.join(string.split(','))
                    integer_value = int(string_without_comma)
                    int_spec.append(integer_value)
                st.title("Number of spectators per match")

                fig, ax = plt.subplots(figsize=(17, 7))
                ax.bar(short_name_teams, int_spec)
                ax.set_xlabel('Echipa')
                ax.set_ylabel('Nr. Spectators')
                st.pyplot(fig)






