# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:34:45 2019

@author: CJP
"""

from django import template
from flask import Flask, render_template,request
import plotly
import plotly.graph_objs as go

import plotly.plotly as py
from plotly.graph_objs import *
from django.utils.html import urlize
#It is necessary to create a plotly account and get an api_key
plotly.tools.set_credentials_file(username='chandnijoshi', \
                            api_key='1oq3uylKGBNiAwi6o4Fv')

import pandas as pd
import numpy as np
import json
import plotly.offline as pyo
from plotly.graph_objs import *
import plotly.graph_objs as go

import pandas as pd
from ast import literal_eval
import seaborn as sns
import json
from scipy import arange
import sklearn as sk
import pydotplus

register = template.Library()

@register.simple_tag
def display_plotname(name):
    plt_text = name

    return plt_text

@register.simple_tag
def display_moviesheading():
    
    return urlize('visit google.com')
     #plt_text

@register.simple_tag
def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'], # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@register.simple_tag
def pipe_flatten_names(keys):
    return '|'.join([x['name'] for x in keys])
@register.simple_tag
def create_movies_plot():
    global be,bn
    path_m = 'C:/Users/CJP/DSA Project/movies.csv'
    df_m = pd.read_csv(path_m)
    df_m.drop(columns=['homepage','status','spoken_languages','title','overview'],inplace=True)
    df_m.dropna(subset=['revenue'],inplace=True)
    df_m.dropna(subset=['original_language','release_date'],inplace=True)
    df_m['runtime'].replace(to_replace=np.nan,value=0.0,inplace=True)
    df_m['budget'].replace(to_replace=[0.0],value=np.NaN,inplace=True)
    df_m['revenue'].replace(to_replace=[0.0],value=np.NaN,inplace=True)
    df_m['tagline'].replace(to_replace=np.nan,value='',inplace=True)
    df_m['popularity']=df_m.popularity.astype(float)
    df_m['id']=df_m['id'].astype('int64')
    df_m['release_date'] = pd.to_datetime(df_m['release_date']).apply(lambda x: x.date())   
    json_columns = ['genres', 'production_countries', 'production_companies']
    df_m.dropna(how='any',subset=['genres', 'production_countries', 'production_companies'],inplace=True) 
    df_m['genres'] = df_m['genres'].apply(json.loads)
    df_m['genres'] = df_m['genres'].apply(pipe_flatten_names)
    list_genres = set()
    for s in df_m['genres'].str.split('|'):
        list_genres = set().union(s, list_genres)
    list_genres = list(list_genres)
    list_genres.remove('')
    for genre in list_genres:
        df_m[genre] = df_m['genres'].str.contains(genre).apply(lambda x:1 if x else 0)
    df_m['year'] = pd.to_datetime(df_m['release_date']).apply(lambda x: x.year)
    df_m['month'] = pd.to_datetime(df_m['release_date']).apply(lambda x: x.month)
    df_m['day'] = pd.to_datetime(df_m['release_date']).apply(lambda x: x.day)
    be,bn = bin_edges(df_m,'revenue')
    df_m['revenue_level'] = df_m['revenue'].apply(apply_levels)
    df_m['revenue_level2'] = pd.qcut(df_m['revenue'],q=3,labels=['Low','Medium','High'])
    dfyear= df_m.year.unique()
    dfyear= np.sort(dfyear)
    # before 1930s
    b1930s =dfyear[:45]
    
    #  decade of 1930
    y1930s =dfyear[45:55]
    
    #  decade of 1940
    y1940s =dfyear[55:65]
    
    #  decade of 1950
    y1950s =dfyear[65:75]
    
    # decade of 1960s
    y1960s =dfyear[75:85]
    
    # decade of 1970s
    y1970s =dfyear[85:95]
    
    # decade of 1980s
    y1980s =dfyear[95:105]
    
    # decade of 1990s
    y1990s = dfyear[105:115]
    
    # decade of 2000
    y2000s = dfyear[115:125]
    
    # decade of 2010/ till now
    y2010s = dfyear[125:]
    
    
    times = [b1930s,y1930s,y1940s,y1950s,y1960s, y1970s, y1980s, y1990s, y2000s,y2010s]
    
    names = ['before1930s','1930s','1940s','1950s','1960s', '1970s', '1980s', '1990s', '2000s','2010s']
    
    df_r3 = pd.DataFrame()
    index = 0
    
    for s in times:
        dfn = df_m[df_m.year.isin(s)] 
        dfn2 = pd.DataFrame({'year' :names[index],'top': find_top(dfn.genres,2)})
        df_r3 = df_r3.append(dfn2)
        index +=1
    df_r3.reset_index(inplace=True)
    df_r3.columns = ['Generes','year','release count']
    d = df_m.copy()
    cols = list(d.columns[16:36])
    cols.extend(['id','revenue'])
    for i in cols:
        d[i] = d[i]*d['revenue']
    df_genre_rev = pd.DataFrame(d[cols].dropna(subset=cols).apply(sum,axis=0).sort_values(ascending=False)[4:14]).reset_index()
    df_genre_rev.columns=['Genres','Total Revenue']
    
    size_4_chart =list(((df_r3['release count'].values)/df_r3['release count'].sum())*1000)

    trace0 = go.Scatter(
        x=df_r3['year'],
        y=df_r3['Generes'],
        mode='markers',
        marker=dict(
            size=size_4_chart,
           
        )
    )
    
    
    data = [trace0]
    plt_t5g_d = py.iplot(data, filename='bubblechart-1')
    
    # Plot the chart
    size_4_chart =list(((df_genre_rev['Total Revenue'][::-1].values)/df_genre_rev['Total Revenue'].sum())*1000)

    trace0 = go.Scatter(
        x=df_genre_rev['Total Revenue'][::-1],
        y=df_genre_rev['Genres'][::-1],
        mode='markers',
        marker=dict(
            size=size_4_chart,
        )
    )

    data = [trace0]
    plt_ = py.iplot(data, filename='bubblechart-size')
       
    #graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return plt_, plt_t5g_d

    #py.iplot(data, filename='bubblechart-size')

#def create_topmoviegenre_revenue(plt_data):
    
    
@register.simple_tag    
def find_top(dataframe_col, num):
    alist = dataframe_col.str.cat(sep='|').split('|')
    new = pd.DataFrame({'top' :alist})
    top = new['top'].value_counts().head(num)
    return top

@register.simple_tag
def find_nexttop(dataframe_col, num):
    alist = dataframe_col.str.cat(sep='|').split('|')
    new = pd.DataFrame({'top' :alist})
    top = new['top'].value_counts()[1:].head(num)
    return top
@register.simple_tag
def find_top_revenuewise(dataframe_col, num):
    alist = dataframe_col.str.cat(sep='|').split('|')
    new = pd.DataFrame({'top' :alist})
    top = new['top'].value_counts().head(num)
    return top



@register.simple_tag    
def bin_edges(dfname ,column_name):
    min_value = dfname[column_name].min()
    first_quantile = dfname[column_name].describe()[4]
    second_quantile = dfname[column_name].describe()[5]
    third_quantile = dfname[column_name].describe()[6]
    max_value = dfname[column_name].max()
    bin_edges = [ min_value, first_quantile, second_quantile, third_quantile, max_value]
    bin_names = [ 'Lowest','Low','Medium', 'High', 'Highest'] 
    return bin_edges,bin_names

@register.simple_tag
def apply_levels(vals):
    if np.isnan(vals):
        return 'NA'
    elif vals ==be[0]:
        return bn[0]
    elif vals <=be[1]:
        return bn[1]
    elif vals <=be[2]:
        return bn[2]
    elif vals <=be[3]:
        return bn[3]
    elif vals >= be[4]:
        return bn[4]
        
@register.simple_tag
def create_keywords_plot(features):
    path_k = 'keywords.csv'
    df_k = pd.read_csv(path_k)
    df_k['keywords'] = df_k['keywords'].apply(lambda x: x.replace("'",'"'))
    df_k['keywords'] = df_k['keywords'].replace('[]',np.nan)
    df_k.dropna(how='any',subset=['keywords'],inplace=True) 
    df_k['keywords'] = df_k['keywords'].apply(json.loads,encoding='utf-8')
    df_k['keywords'] = df_k['keywords'].apply(pipe_flatten_names)
    list_keywords = set()
    for s in df_k['keywords'].str.split('|'):
        list_keywords = set().union(s, list_keywords)
    list_keywords = list(list_keywords)

#def create_top5genres_decades_plot(features):    

