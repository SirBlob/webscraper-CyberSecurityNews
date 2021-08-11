# To Do
# 
# Fix up variables to be more descriptive
# find a way to check if empty dataframe and skip it if it is

import pandas as pd
import requests
import lxml.html
from datetime import datetime
from urllib.parse import urljoin

pd.set_option('display.max_colwidth', 50)
pd.set_option("display.expand_frame_repr", False)

urls = [
    ## Phishing
    "https://www.scmagazine.com/home/security-news/phishing/",

    ## Path Management
    "https://www.scmagazine.com/home/patch-management/",
    
    ## Ransomware
    "https://www.scmagazine.com/home/security-news/ransomware/",

    ## SDLC
    "https://appdevelopermagazine.com/search/sdlc",

    ## General CyberSec News
    "https://cyware.com/cyber-security-news-articles",
    "https://threatpost.com/",
    "https://thehackernews.com/"
]

#Converts each link in list to each own with different text
def add_htmllink(x):
    #htmllink = [f"<a href={htmllink} target='_blank'>Link</a>" for htmllink in x]
    htmllink = [f"<a href={htmllink} target='_blank'><button>Link</button></a>" for htmllink in x]
    return htmllink

#Style Source Title
def style_source(y):
    source_title = f"<h1 style='color:white;font-size:20px;text-align:center;text-decoration: underline;'>{y}</h1>"
    return source_title

## General CyberSec News
#To parse multiple sites but to note !# each site might have their own special way
for p in urls:
    page = requests.get(p, headers={'User-Agent': 'Mozilla/5.0'})
    doc = lxml.html.fromstring(page.text) #Change page.content to page.text fixed the encoding problem
    #If checks the variable p for which website to scrape

    #Phishing
    if p == "https://www.scmagazine.com/home/security-news/phishing/":
        p_title = doc.xpath('//h3[@class="title"]//a/text()')
        p_descrip = doc.xpath('//div/div[@class="content"]/p/text()')
        p_links = doc.xpath('//h3[@class="title"]//a/@href')
        
        p_titlesplit = [p_title.strip() for p_title in p_title] #if brackets added remove split
        
        ph = pd.DataFrame({
            "Title": p_titlesplit,
            "Description": p_descrip,
            "Link": add_htmllink(p_links) #will probably need a for loop for each link
        })

        phrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Phishing - SCMagazine"),
            "Link": " "
        }, index = [0])

        ph = pd.concat([phrow, ph]).reset_index(drop = True) 

    #Patch Management
    elif p == "https://www.scmagazine.com/home/patch-management/":
        pm_title = doc.xpath('//h3[@class="title"]//a/text()')
        pm_descrip = doc.xpath('//div/div[@class="content"]/p/text()')
        pm_links = doc.xpath('//h3[@class="title"]//a/@href')
        
        pm_titlesplit = [pm_title.strip() for pm_title in pm_title] #if brackets added remove split
        
        pm = pd.DataFrame({
            "Title": pm_titlesplit,
            "Description": pm_descrip,
            "Link": add_htmllink(pm_links)
        })

        pmrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Patch Management - SCMagazine"),
            "Link": " "
        }, index = [0])

        pm = pd.concat([pmrow, pm]).reset_index(drop = True)

    #Ransomware
    elif p == "https://www.scmagazine.com/home/security-news/ransomware/":
        rm_title = doc.xpath('//h3[@class="title"]//a/text()')
        rm_descrip = doc.xpath('//div/div[@class="content"]/p/text()')
        rm_links = doc.xpath('//h3[@class="title"]//a/@href')
        
        rm_titlesplit = [rm_title.strip() for rm_title in rm_title] #if brackets added remove split
        
        rm = pd.DataFrame({
            "Title": rm_titlesplit,
            "Description": rm_descrip,
            "Link": add_htmllink(rm_links)
        })

        rmrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Ransomeware - SCMagazine"),
            "Link": " "
        }, index = [0])

        rm = pd.concat([rmrow, rm]).reset_index(drop = True) 

    #SDLC
    elif p == "https://appdevelopermagazine.com/search/sdlc":
        
        if datetime.today().strftime("%B") not in doc.xpath('/html/body/div[2]/div/div/section/div/div/div[1]/div/text()'):
            continue
        sdlc_title = doc.xpath('//div[@id="content"]//span[@class="newstitle"]//text()')
        sdlc_descrip = doc.xpath('//div[@id="content"]//p//text()')
        sdlc_links = doc.xpath('//div[@class="profile-inner-wrapper typography-text clearfix"]/a/@href')
        
        sdlc_titlesplit = [sdlc_title.strip() for sdlc_title in sdlc_title] #if brackets added remove split
        
        sdlc = pd.DataFrame({
            "Title": sdlc_titlesplit,
            "Description": sdlc_descrip,
            "Link": add_htmllink(sdlc_links)
        })

        sdlc_row = pd.DataFrame({
            "Title": " ",
            "Description": style_source("SDLC"),
            "Link": " "
        }, index = [0])

        sdlc = pd.concat([sdlc_row, sdlc]).reset_index(drop = True) 
        
    elif p == "https://cyware.com/cyber-security-news-articles":
        title = doc.xpath('//h1[@class="cy-card__title m-0 cursor-pointer pb-3"]/text()')
        descrip = doc.xpath('//div[@class="cy-card__description"]/text()')
        links = doc.xpath('//div[@class="cy-panel__body"]/a[not(contains(@href,"alerts"))]/@href')

        #Cleaning up the data
        titlestrip = [title.lstrip().rstrip() for title in title] #removes the new line and spaces from left and right
        descripstrip = [descrip.lstrip().rstrip() for descrip in descrip] #removes the new line and spaces from left and right

        linkhtml = ['https://cyware.com' + links if links.startswith('/') else links for links in links] #If it starts with a / add https://cyware.com/, broken links
        
        #Create a dataframe for the data
        gc = pd.DataFrame({
            "Title": titlestrip,
            "Description": descripstrip,
            "Link": add_htmllink(linkhtml)
        })

        Siterow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Cyware"),
            "Link": " "
        }, index = [0])
        gc = pd.concat([Siterow, gc]).reset_index(drop = True) 

    elif p == "https://threatpost.com/":
        title2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/text()')
        descrip2 = doc.xpath('//div[@class="c-border-layout"]//p/text()') 
        links2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/@href')

        gc2 = pd.DataFrame({
            "Title": title2,
            "Description": descrip2,
            "Link": add_htmllink(links2)
        })

        Siterow2 = pd.DataFrame({
            "Title": "",
            "Description": style_source("Threatpost"),
            "Link": " "
        }, index = [0])
    
        gc2 = pd.concat([Siterow2, gc2]).reset_index(drop = True) 

    elif p == "https://thehackernews.com/":
        title3 = doc.xpath('//div[@class="clear home-post-box cf"]//h2[@class="home-title"]/text()')
        descrip3 = doc.xpath('//div[@class="clear home-post-box cf"]//div[@class="home-desc"]/text()') 
        links3 = doc.xpath('//a[@class="story-link"]/@href')

        gc3 = pd.DataFrame({
            "Title": title3,
            "Description": descrip3,
            "Link": add_htmllink(links3)
        })

        Siterow3 = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Hacker News"),
            "Link": " "
        }, index = [0])

        gc3 = pd.concat([Siterow3, gc3]).reset_index(drop = True) 
        
    else:
        print(f"Something went wrong with {p}")

list_df = [pm, rm, sdlc, gc, gc2, gc3]
final = ph.append(list_df, ignore_index = True) #append all the dataframes together

print(f"Good Morning!\nToday is {datetime.today().strftime('%A, %B %d %Y')} see below for the latest cybersecurity news.")
print("Feel free to provide feedback or improvement requests.\nHave a nice day.")

finalstyle = final.style.set_properties(**{'background-color': '107896', 'color': 'white'}).hide_index()
finalstyler = finalstyle.render()
with open(f"{datetime.today().strftime('%A, %B %d %Y')}styler.html", "w", encoding="utf-8") as text_file:
    text_file.write(finalstyler)
