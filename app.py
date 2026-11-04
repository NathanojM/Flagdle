import pandas as pd
import plotly.graph_objects as go
import random
import numpy as np
import urllib.request
from PIL import Image
from IPython.display import display
from difflib import SequenceMatcher
from operator import itemgetter

table = pd.read_csv("flagtable.csv")
table["rgb"]=table["r"].astype(str)+","+table["g"].astype(str)+","+table["b"].astype(str) #concatenate rgb fields

table.loc[table["rgb"]=="0,0,0", "r"] = 1 #0,0,0=black, but it doesn't show up unless it's shifted to 1,1,1
table.loc[table["rgb"]=="0,0,0", "g"] = 1
table.loc[table["rgb"]=="0,0,0", "b"] = 1

def rgb_to_hex(rgb): #convert RGB to hex for filling points
    r, g, b = map(int, rgb.split(","))
    return f"#{r:02x}{g:02x}{b:02x}"

table["rgb"]=table["rgb"].apply(rgb_to_hex)
allcountries=table
table = table.loc[table["Country"] == str(random.choice(table["Country"]))] #pick a random country
table = table.loc[table["%"]>= 0.1] #filter out tiny pixel values from the PNG compression
table.loc[table["%"]<=1, ["%"]] = 3 #make tiny colours more visible by making anything less than 1% 3%
table=table.sort_values(by='%',ascending=False) #put smaller points over larger ones for visibility

fig = go.Figure()
fig.add_trace(go.Scatterternary(
    a=table["r"],b=table["g"], c=table["b"], #r g and b axes
    mode="markers+lines", #lines to join points together - makes tiny ones easier to see
    #hovertext=table["Country"], #show country name on hover

    marker=dict(color=table["rgb"],size=table["%"]/100,opacity=1),
    line=dict(color="lightgray"),text="",textposition="middle center"))

fig.update_ternaries(aaxis_title="Red",baxis_title="Green",caxis_title="Blue") #axis titles
fig.update_layout(width=1000, height=1000) # make chart bigger
fig.show()
for x in table["Country"]:
    c=x.upper() #make country names uppercase

countries=[] #get list of country names to match against
for i in allcountries["Country"]:
        countries.append(i.upper())



guesses=0
while guesses<6:
    guess=input("\nEnter guess here: ") #enter guess
    guess=guess.upper() #make guess uppercase

    if guess not in countries: #reject if country not in list
        print("\nNot a valid country")
        matches=[]
        for country in countries: #look for countries with similar names
            res = SequenceMatcher(None, guess.upper(), country.upper()).ratio()
            match=({"country":country,"res":res})
            if match not in matches:
                matches.append(match)
        matches = sorted(matches, key=itemgetter('res'), reverse=True) #sort list of countries by similarity
        print("Did you mean?")
        matches=matches[:3] #choose top 3 most similar countries
        for m in matches: #print top 3
            print(m["country"])

    elif guess ==c: #if guess is correct
        guesses+=1
        print(f"Correct! You guessed the flag in {guesses} guesses.")

        break

    else: #if guess is wrong
        guesses+=1


for x in table["ISO"]:
    iso=x.lower() #flagpedia filenames are lowercase iso.png
    urllib.request.urlretrieve(f'https://flagcdn.com/h240/{iso}.png', "flagpic.png") #get picture of flag
    display(Image.open("flagpic.png")) #show picture
    break
for x in table["Country"]:
    print(f"\nAnswer: {x}")
    break
