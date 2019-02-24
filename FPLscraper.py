import time
from selenium import webdriver
import pandas as pd

import re
num=re.compile(r'\d+')
skip=int(input('Enter gameweek to start from: ')) 


output=pd.DataFrame()

browser = webdriver.Firefox()
browser.get('https://fantasy.premierleague.com/a/leagues/standings/45810/classic')
time.sleep(3)
teams = browser.find_elements_by_css_selector("a[class='ismjs-link']")
print("Teams identified:", len(teams))

for i in range(len(teams)):
    scores=[0]
    teamname=teams[i].text.splitlines()[1]
    print("Extracting team: ", teamname)
    teams[i].click()


    #gameweek history
    time.sleep(1.25)
    browser.find_element_by_css_selector("a[class='ismjs-link ism-link ism-link--more']").click()
    
    #gameweeks
    time.sleep(1.25)
    gws = browser.find_elements_by_css_selector("a[class='ismjs-show-event ismjs-link']")
    j=0
    skipper=skip
    length=len(gws)
    if teamname=='anirudh menon':
        skipper-=3
        if skip<=3:
            for i in range(3-skip):
                scores.append(0)

    while j<length:
        if j+1>=skipper:
            gws[j].click()
            time.sleep(1.25)


            #extracting digits of score
            score = int(num.match(browser.find_element_by_css_selector("div[class='ism-scoreboard__panel__value ism-scoreboard__panel__value--lrg']").text).group())
            print("GW",j+1,": ", score)
            

            #checking for transfer cost
            try:    
                tcost = int(num.match(browser.find_element_by_css_selector("span[class='ism-scoreboard-points__tf-cost']").text[2:]).group())
                print('Transfer cost detected: ', tcost)
                score-=tcost
                print("New score: ", score)
            except Exception as e:
                pass
            finally:
                
                scores.append(score)


            
            browser.back()
            time.sleep(1.25)
            gws = browser.find_elements_by_css_selector("a[class='ismjs-show-event ismjs-link']")
        j+=1

    print(scores)
    output[teamname]=scores

    #return to main
    browser.get('https://fantasy.premierleague.com/a/leagues/standings/45810/classic')
    time.sleep(3)
    teams = browser.find_elements_by_css_selector("a[class='ismjs-link']")



output.T.to_csv("data.csv", index=True)
