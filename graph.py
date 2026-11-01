import pandas as pd
import plotly.graph_objects as go
import os
import random
import numpy as np

def rgb_to_hex(rgb):
    r, g, b = map(int, rgb.split(","))
    return f"#{r:02x}{g:02x}{b:02x}"

countries=pd.read_csv("Countries.csv")

flags=['ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bl', 'bm', 'bn', 'bo', 'bq', 'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm','cn', 'co', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gb-eng','gb-nir', 'gb-sct', 'gb-wls', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no','np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'xk', 'ye', 'yt', 'za', 'zm', 'zw']

table = pd.read_csv("flagrgb.csv")
table["rgb"]=table["r"].astype(str)+","+table["g"].astype(str)+","+table["b"].astype(str)
table.loc[table["rgb"]=="0,0,0", "r"] = 1
table.loc[table["rgb"]=="0,0,0", "g"] = 1
table.loc[table["rgb"]=="0,0,0", "b"] = 1
table["rgb"]=table["rgb"].apply(rgb_to_hex)
table["%"]=table["%"]*100
table=pd.merge(table,countries,on="ISO")



flag=random.choice(flags)

flag=flag.upper()
table = table.loc[table["ISO"] == flag]

table.loc[table["%"]<1, "%"] = 2
table=table.sort_values(by='%',ascending=False)

fig = go.Figure()



fig.add_trace(go.Scatterternary(
    a=table["r"],
    b=table["g"],
    c=table["b"],
    mode="markers+lines",
    hovertext=table["Country"],


    marker=dict(
        color=table["rgb"],
        size=table["%"]*3,
        opacity=1),
    line=dict(color="lightgray"),
    text=table["Country"],
    textposition="middle center"))

fig.update_ternaries(
    aaxis_title="Red",
    baxis_title="Green",
    caxis_title="Blue")


fig.write_html("flag.html")
fig.show()  
