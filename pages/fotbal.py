import requests
from bs4 import BeautifulSoup
import re

import streamlit as st
st.title("Fotbal")

coduri=[]

def atribuie():
    file_path = r'C:\Users\Teo G\Desktop\proiect2\coduri.txt'
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        values = line.split()
        coduri.append((values[0], int(values[1])))

atribuie()
optiuni=['-']
optiuni.append('real-madrid')
optiuni.append('barcelona')
optiuni.append('ajax')
optiuni.append('_La-Liga')
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
                print(cod)

                url = "https://www.sofascore.ro/team/football/{}/{}/".format(ops, cod)
                print(url)
                print(url)
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
                new_string = ops[1:]
                ops=new_string
                sir = "Informatii esentiale despre " + ops
                size = 30
                st.markdown(f'<span style="color: blue; font-weight: bold; font-size: {size}px">{sir}</span>',
                            unsafe_allow_html=True)
                st.write("Loading...")

                standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
                data = requests.get(standings_url)
                soup = BeautifulSoup(data.text, 'html.parser')
                standings_table = soup.select('table.stats_table')[0]
                links = standings_table.find_all('a')
                links = [l.get("href") for l in links]
                links = [l for l in links if '/squads/' in l]
                team_urls = [f"https://fbref.com{l}" for l in links]
                data = requests.get(team_urls[0])
                import pandas as pd
                matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
                soup = BeautifulSoup(data.text)
                links = soup.find_all('a')
                links = [l.get("href") for l in links]
                links = [l for l in links if l and 'all_comps/shooting/' in l]
                data = requests.get(f"https://fbref.com{links[0]}")
                shooting = pd.read_html(data.text, match="Shooting")[0]
                shooting.columns = shooting.columns.droplevel()
                team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
                st.write(team_data.head())
                years = list(range(2022, 2020, -1))
                all_matches = []
                standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
