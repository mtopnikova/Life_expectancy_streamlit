import pandas as pd
import streamlit as st
import plotly.express as px


# загрузка данных
df = pd.read_csv('./data/WHOregionLifeExpectancyAtBirth.csv')
df = df.drop('Indicator', axis=1).rename({'Dim1':'Gender', 'First Tooltip':'Life expectancy(years)'}, axis=1)

# добавление вкладок
# в первой вкладке - сам датафрейм с возможностью фильтрации
# во второй вкладке - графики по странам
tab1, tab2 = st.tabs(["General Data Info", "Plots"])

with tab1:
    st.header('Life Expectancy')
    # отображение датафрейма
    st.dataframe(df)

    # создание кнопки "Click to filter the data" для возможности отображать только интересующую часть данных
    # после нажатия кнопка меняет название на "Click to clear filters" для возможности сбросить фильтры
    btnlst = ["Click to filter the data", "Click to clear filters"]
    if "btnptr" not in st.session_state:
        st.session_state.btnptr = 0

    def btnCB():
        if st.session_state.btnptr == 0:
            st.session_state.btnptr = 1
            st.write("Clearing filters")
        else:
            st.session_state.btnptr = 0
            st.write("Filtering data")

    st.button(btnlst[st.session_state.btnptr], on_click=btnCB)

    if st.session_state.btnptr == 1:
        locations = st.sidebar.multiselect('Show which location(s)?', df.Location.unique())
        period = st.sidebar.multiselect('Show which period?', df['Period'].unique())
        sex = st.sidebar.multiselect('Show which gender(s)?', df['Gender'].unique())
        filtered = df[(df['Location'].isin(locations)) & (df['Period'].isin(period)) & (df['Gender'].isin(sex))]
        st.write(filtered)

with tab2:
    st.header('Plots by country')

    for country in df["Location"].unique():
    
        fig = px.line(df[df["Location"] == country], x="Period", y="Life expectancy(years)", color="Gender")
        fig.update_layout(
            title=f'Life expectancy dynamic in {country}')

        st.plotly_chart(fig) # отображение графиков, нарисованных plotly