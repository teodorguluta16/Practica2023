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
    #ligi
    file_path = r'C:\Users\Teo G\Desktop\proiect2\nume_ligi'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        values = line.strip()
        optiuni.append(values)

    #echipe
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

                element = soup.find_all("div", class_="sc-bqWxrE dcUFbK")
                info = [div.text for div in element]
                title_text = "<h1 style='color: yellow; font-size: 36px;'>{}</h1>".format(info[0])
                st.markdown(title_text, unsafe_allow_html=True)

                element = soup.find_all("div", class_="sc-bqWxrE jgPEwK")
                info = [div.text for div in element]
                element = soup.find_all("span", class_="sc-bqWxrE CQaWk")
                info2 = [div.text for div in element]

                left_column, middle_column, right_column = st.columns(3)
                total_juc=0
                with left_column:
                    st.markdown(f'<span style="color: orange; font-weight: bold;">{info[0]}</span>', unsafe_allow_html=True)
                    st.subheader(info2[0])
                    total_juc=info2[0]
                    st.markdown(f'<span style="color: orange; font-weight: bold;">{info[1]}</span>', unsafe_allow_html=True)
                    st.subheader(info2[1])
                with middle_column:
                    st.markdown(f'<span style="color: orange; font-weight: bold;">{info[2]}</span>',
                                unsafe_allow_html=True)
                    element=soup.find_all("span",class_="sc-bqWxrE bGmDyb")
                    info2 = [div.text for div in element]
                    st.subheader(info2[0])
                    import matplotlib.pyplot as plt
                    nr_juc= []
                    labels= []
                    labels.append("Forigner players")
                    labels.append("National players")
                    nr_juc.append(info2[0])
                    nr_juc.append(int(total_juc)-int(info2[0]))
                    colors = ['red', 'blue']
                    fig, ax = plt.subplots()
                    ax.pie(nr_juc, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                    ax.set_title('Statistica')
                    ax.axis('equal')
                    st.pyplot(fig)
                with right_column:
                    st.markdown(f'<span style="color: orange; font-weight: bold;">{info[3]}</span>',
                                unsafe_allow_html=True)
                    element = soup.find_all("span", class_="sc-bqWxrE bGmDyb")
                    info2 = [div.text for div in element]
                    st.subheader(info2[1])
                    import matplotlib.pyplot as plt

                    nr_juc = []
                    labels = []
                    labels.append("National team players")
                    labels.append("")
                    nr_juc.append(info2[0])
                    nr_juc.append(int(total_juc) - int(info2[1]))
                    colors = ['red', 'yellow']
                    fig, ax = plt.subplots()
                    ax.pie(nr_juc, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                    ax.set_title('Statistica')
                    ax.axis('equal')
                    st.pyplot(fig)
            else:
                cod = -1
                new_string = ops[1:]
                ops=new_string
                sir = "Informatii esentiale despre " + ops
                size = 30
                st.markdown(f'<span style="color: blue; font-weight: bold; font-size: {size}px">{sir}</span>',
                            unsafe_allow_html=True)

                url = 'https://fbref.com/en/comps/'
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    premier_league_link = soup.find('a', text=ops)
                    if premier_league_link:
                        league_url = premier_league_link['href']
                        id =league_url.split('/')[3]

                cod=id
                url = 'https://fbref.com/en/comps/{}/'.format(cod)
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
                    notes.append(columns[17].text.strip())

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

                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)

                left_column, middle_column, right_column = st.columns(3)
                with left_column:
                    st.markdown("<h3 style='color: green;'>European qualification:</h3>", unsafe_allow_html=True)
                with middle_column:
                    st.markdown("<h3 style='color: red;'>Relegated:</h3>", unsafe_allow_html=True)
                for index, note in enumerate(notes):
                    if note != '' and note !='Relegated':
                        with left_column:
                            st.subheader(teams[index]+": "+note)
                    else:
                        if note =='Relegated':
                            with middle_column:
                                st.subheader(teams[index])

                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)

                st.title("Current ranking")
                st.table(styled_table)
                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)

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

                xG_double=list(map(float, xG))
                xGA_double=list(map(float, xGA))

                import plotly.express as px

                data = {'Echipa': teams, 'Nr. Spectators': int_spec}
                df = pd.DataFrame(data)
                fig = px.bar(df, x='Echipa', y='Nr. Spectators', orientation='v')
                fig.update_layout(height=800, width=1000)
                fig.update_layout(bargap=0.1)
                st.write(fig)


                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)

                st.title("Winning chances")
                import plotly.express as px

                data = {'Teams': teams, 'xG': xG_double, 'xGA': xGA_double}
                df = pd.DataFrame(data)
                fig = px.bar(df, x=['xG', 'xGA'], y='Teams', orientation='h', barmode='group')
                fig.update_layout(height=800, width=1000)
                fig.update_layout(bargap=0.4)
                st.write(fig)

                table = soup.find('table', {'id': 'stats_squads_standard_for'})
                teams = []
                posesie = []
                asisturi = []
                goluri_penaltiuri = []
                penaltiuri_primite = []
                cartonase_rosii = []
                cartonase_galbene = []
                rows = table.find_all('tr')
                for row in rows[2:]:
                    columns=row.find_all('th')
                    teams.append(columns[0].text.strip())
                for row in rows[2:]:
                    columns = row.find_all('td')
                    posesie.append(columns[2].text.strip())
                    asisturi.append(columns[8].text.strip())
                    goluri_penaltiuri.append(columns[11].text.strip())
                    penaltiuri_primite.append(columns[12].text.strip())
                    cartonase_galbene.append(columns[13].text.strip())
                    cartonase_rosii.append(columns[14].text.strip())


                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)
                st.title("Possesion percentage")
                import plotly.express as px

                data = {'Teams': teams, 'Possesion': posesie}
                df = pd.DataFrame(data)
                fig = px.bar(df, x='Possesion', y='Teams', orientation='h')
                fig.update_layout(height=800, width=1000)
                fig.update_layout(bargap=0.1)
                st.write(fig)


                st.markdown('<hr style="background-color: yellow;">', unsafe_allow_html=True)
                st.title("Actions statistics: ")
                left_column, right_column = st.columns(2)

                with left_column:
                    st.subheader("Possesion percentage")
                    import plotly.express as px
                    data = {'Teams': teams, 'Possesion': posesie}
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Possesion', y='Teams', orientation='h')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)
                with right_column:
                    st.subheader("Assists")
                    import plotly.express as px

                    data = {
                        'Teams': teams,
                        'Asisturi': asisturi,
                    }
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Asisturi', y='Teams', orientation='h', barmode='group')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)
                with left_column:
                    st.subheader('Got penalties')
                    import plotly.express as px
                    data = {
                        'Teams': teams,
                        'Got penalties': penaltiuri_primite
                    }
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Got penalties', y='Teams', orientation='h', barmode='group')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)
                with right_column:
                    st.subheader('Penalty goals')
                    import plotly.express as px
                    data = {
                        'Teams': teams,
                        'Penalty goals': goluri_penaltiuri
                    }
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Penalty goals', y='Teams', orientation='h', barmode='group')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)
                with left_column:
                    st.subheader('Yellow cards')
                    import plotly.express as px
                    data = {
                        'Teams': teams,
                        'Yellow cards': cartonase_galbene,
                    }
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Yellow cards', y='Teams', orientation='h', barmode='group')
                    fig.update_traces(marker_color='yellow')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)
                with right_column:
                    st.subheader('Red cards')
                    import plotly.express as px
                    data = {
                        'Teams': teams,
                        'Red cards': cartonase_rosii
                    }
                    df = pd.DataFrame(data)
                    fig = px.bar(df, x='Red cards', y='Teams', orientation='h',barmode='group')
                    fig.update_traces(marker_color='red')
                    fig.update_layout(height=600, width=600)
                    fig.update_layout(bargap=0.1)
                    st.write(fig)

