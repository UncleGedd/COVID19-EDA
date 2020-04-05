import numpy as np
import pandas as pd

# data cleaning and summing total events by country
def preprocess_summation(df, description):
    df = df.drop(['Province/State', 'Lat', 'Long'], axis=1) \
        .groupby(['Country/Region']).sum().reset_index()
    col_name = 'Total' + ' ' + description
    df[col_name] = df.apply(lambda r: r[-1], axis=1)
    df = df[['Country/Region', col_name]]
    df.columns = ['Country', col_name]
    df.replace({'Korea, South': 'South Korea', 'Czechia': 'Czech Republic', 
                'Taiwan*': 'Taiwan', 'US': 'United States'}, inplace=True)
    return df

df = pd.read_csv('./prod/covid19_by_country.csv')
df.drop(['Total Infected', 'Total Deaths', 'Total Recovered'], axis=1, inplace=True)

# new infections
df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
total_infections = preprocess_summation(df_confirmed, 'Infected')
df = df.merge(total_infections, how='inner', on='Country')

# new deaths
df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
total_deaths = preprocess_summation(df_deaths, 'Deaths')
df = df.merge(total_deaths, how='inner', on='Country')

# new recoveries
df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
total_recover = preprocess_summation(df_recovered, 'Recovered')
df = df.merge(total_recover, how='inner', on='Country')

df.to_csv('./prod/covid19_by_country.csv', index=False)
