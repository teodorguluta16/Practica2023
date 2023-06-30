import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Movies", page_icon=":movie_camera:", layout="wide")
st.title("Movies :movie_camera:")
st.markdown("##")

url = 'https://www.imdb.com/search/title/?count=20&groups=top_1000&sort=user_rating'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []
description = []
Director = []
Stars = []
movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

for store in movie_data:
    name = store.h3.a.text
    movie_name.append(name)

    year_of_release = store.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
    year.append(year_of_release)

    runtime = store.p.find('span', class_='runtime').text.replace(' min', '')
    time.append(runtime)

    rate = store.find('div', class_='inline-block ratings-imdb-rating').text.replace('\n', '')
    rating.append(rate)

    meta = store.find('span', class_='metascore').text.replace(' ', '') if store.find('span',class_='metascore') else '0'
    metascore.append(meta)
    value = store.find_all('span', attrs={'name': 'nv'})

    vote = value[0].text
    votes.append(vote)

    grosses = value[1].text if len(value) > 1 else '0'
    gross.append(grosses)
    describe = store.find_all('p', class_='text-muted')
    description_ = describe[1].text.replace('\n', '') if len(describe) > 1 else '0'
    description.append(description_)

    cast = store.find("p", class_='')
    cast = cast.text.replace('\n', '').split('|')
    cast = [x.strip() for x in cast]
    cast = [cast[i].replace(j, "") for i, j in enumerate(["Director:", "Stars:"])]
    Director.append(cast[0])
    Stars.append([x.strip() for x in cast[1].split(",")])

movie_DF = pd.DataFrame(
    {'Name of movie': movie_name,
     'Year of relase': year,
     'Watchtime': time,
     'Movie Rating': rating,
     'Nota': metascore,
     'Votes': votes,
     'Gross collection': gross,
     'Description': description,
     "Director": Director, 'Star': Stars
     })

movie_DF.to_excel("Top_20_Movies.xlsx")
st.table(movie_DF)
left_column, middle_column, right_column = st.columns(3)
sir = []
for string_value in gross:
    if string_value:
        numeric_value = float(''.join(filter(str.isdigit, string_value)))
        sir.append(numeric_value)
with left_column:
    st.subheader('Movie Ratings')
    import plotly.express as px

    data = {
        'Name of movie': movie_name,
        'Gross collection': sir,
    }
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Name of movie', y='Gross collection', orientation='v', barmode='group')
    fig.update_layout(height=900, width=900)
    fig.update_layout(bargap=0.1)
    st.write(fig)

fig = px.pie(values=sir, labels=movie_name)
fig.update_layout(height=800, width=800)

# Display the chart in Streamlit
st.plotly_chart(fig)