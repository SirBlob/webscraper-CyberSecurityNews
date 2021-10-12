
import pandas as pd
import requests
import lxml.html
from datetime import datetime
from urllib.parse import urljoin

pd.set_option('display.max_colwidth', 50)
pd.set_option("display.expand_frame_repr", False)

#Urls
phishing = "https://www.scmagazine.com/topic/phishing"
patch_management = "https://www.scmagazine.com/topic/patch-management/"
ransomware = "https://www.scmagazine.com/ransomware"
software_dev = "https://sdtimes.com/"
cyware = "https://cyware.com/cyber-security-news-articles"
threatpost = "https://threatpost.com/"
hacker_news = "https://thehackernews.com/"
exfiltration = "https://www.bleepingcomputer.com/tag/data-exfiltration/"
podcast = "https://www.itworldcanada.com/podcasts#cyber-security-today"
fbi_flash = "https://www.fbi.gov/investigate/cyber/news"

urls = [
    ## Phishing
    phishing,

    ## Patch Management
    patch_management,
    
    ## Ransomware
    ransomware, #! Weird site is broken for now

    ## SDLC
    software_dev,

    ## General CyberSec News
    cyware,
    threatpost,
    hacker_news,
    fbi_flash,

    ## Exfiltration
    exfiltration,

    ## CyberSec Podcast
    podcast
]

#Converts each link in list to each own with different text
def add_htmllink(x):
    #htmllink = [f"<a href={htmllink} target='_blank'>Link</a>" for htmllink in x]
    htmllink = [f"<a href={htmllink} target='_blank'><button>Link</button></a>" for htmllink in x]
    return htmllink

#Style Source Title
def style_source(y):
    source_title = f"<h1 style='color:add8e6;font-size:20px;text-align:center;text-decoration: underline;'>{y}</h1>"
    return source_title

## General CyberSec News
#To parse multiple sites but to note !# each site might have their own special way
for p in urls:
    page = requests.get(p, headers={'User-Agent': 'Mozilla/5.0'})
    doc = lxml.html.fromstring(page.text) #Change page.content to page.text fixed the encoding problem
    #If checks the variable p for which website to scrape

    #Phishing
    if p == phishing:
        p_title = doc.xpath('//h5[@class="ContentTeaser_title__3Gv3Q"]/text()')[:3] #limits to 3 posts
        p_descrip = doc.xpath('//div/div[@class="ContentTeaser_summary__34nbw"]/p/text()')[:3]
        p_links = doc.xpath('//a[@class="ContentTeaser_titleLink__30KhQ"]/@href')[:3]
        
        p_titlesplit = [p_title.strip() for p_title in p_title] #if brackets added remove split
        p_linkhtml = ['https://www.scmagazine.com' + p_links if p_links.startswith('/') else p_links for p_links in p_links]

        ph = pd.DataFrame({
            "Title": p_titlesplit,
            "Description": p_descrip,
            "Link": add_htmllink(p_linkhtml) #will probably need a for loop for each link
        })

        phrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Phishing - SCMagazine"),
            "Link": " "
        }, index = [0])

        ph = pd.concat([phrow, ph]).reset_index(drop = True) 

    #Patch Management
    elif p == patch_management:
        pm_title = doc.xpath('//h5[@class="ContentTeaser_title__3Gv3Q"]/text()')[:3]
        pm_descrip = doc.xpath('//div/div[@class="ContentTeaser_summary__34nbw"]/p/text()')[:3]
        pm_links = doc.xpath('//a[@class="ContentTeaser_titleLink__30KhQ"]/@href')[:3]
        
        pm_titlesplit = [pm_title.strip() for pm_title in pm_title] #if brackets added remove split
        pm_linkhtml = ['https://www.scmagazine.com' + pm_links if pm_links.startswith('/') else pm_links for pm_links in pm_links]

        pm = pd.DataFrame({
            "Title": pm_titlesplit,
            "Description": pm_descrip,
            "Link": add_htmllink(pm_linkhtml)
        })

        pmrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Patch Management - SCMagazine"),
            "Link": " "
        }, index = [0])

        pm = pd.concat([pmrow, pm]).reset_index(drop = True)

    #Ransomware
    elif p == ransomware:
        rm_title = doc.xpath('//h5[@class="ContentTeaser_title__3Gv3Q"]/text()')[:3]
        rm_descrip = doc.xpath('//div/div[@class="ContentTeaser_summary__34nbw"]/p/text()')[:3]
        rm_links = doc.xpath('//a[@class="ContentTeaser_titleLink__30KhQ"]/@href')[:3]
        
        rm_titlesplit = [rm_title.strip() for rm_title in rm_title] #if brackets added remove split
        rm_linkhtml = ['https://www.scmagazine.com' + rm_links if rm_links.startswith('/') else rm_links for rm_links in rm_links]
        
        rm = pd.DataFrame({
            "Title": rm_titlesplit,
            "Description": rm_descrip,
            "Link": add_htmllink(rm_linkhtml)
        })

        rmrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Ransomeware - SCMagazine"),
            "Link": " "
        }, index = [0])

        rm = pd.concat([rmrow, rm]).reset_index(drop = True) 

    #SDLC
    elif p == software_dev:
        sdlc_title = doc.xpath('//div[@class="col-lg-8 col-md-7 col-sm-9 col-xs-12"]/h4//text()')[:3]
        sdlc_descrip = doc.xpath('//div[@class="col-lg-8 col-md-7 col-sm-9 col-xs-12"]/p//text()')[:3]
        sdlc_links = doc.xpath('//div[@class="col-lg-8 col-md-7 col-sm-9 col-xs-12"]/h4//@href')[:3] #! Broken
        
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
        
    #CyberSec News
    elif p == cyware:
        title = doc.xpath('//h1[@class="cy-card__title m-0 cursor-pointer pb-3"]/text()')[:5]
        descrip = doc.xpath('//div[@class="cy-card__description"]/text()')[:5]
        links = doc.xpath('//div[@class="cy-panel__body"]/a[not(contains(@href,"alerts"))]/@href')[:5]

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

#ThreatPost
    elif p == threatpost:
        title2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/text()')[:5]
        descrip2 = doc.xpath('//div[@class="c-border-layout"]//p/text()')[:5]
        links2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/@href')[:5]

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

#HackerNews
    elif p == hacker_news:
        title3 = doc.xpath('//div[@class="clear home-post-box cf"]//h2[@class="home-title"]/text()')[:3]
        descrip3 = doc.xpath('//div[@class="clear home-post-box cf"]//div[@class="home-desc"]/text()')[:3] 
        links3 = doc.xpath('//a[@class="story-link"]/@href')[:3]

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

#FBINews
    elif p == fbi_flash:
        fbi_title = doc.xpath('//ul[@class="dt-tagged filter-listing"]//h3[@class="title"]//text()')[:5]
        fbi_descrip = None
        fbi_links = doc.xpath('//ul[@class="dt-tagged filter-listing"]//h3[@class="title"]//@href')[:5]

        fbi_news = pd.DataFrame({
            "Title": fbi_title,
            "Description": fbi_descrip,
            "Link": add_htmllink(fbi_links)
        })

        fbi_row = pd.DataFrame({
            "Title": " ",
            "Description": style_source("FBI News"),
            "Link": " "
        }, index = [0])

        fbi_news = pd.concat([fbi_row, fbi_news]).reset_index(drop = True) 

#Exfiltration
    elif p == exfiltration:
        exfil_title = doc.xpath('//div[@class="bc_latest_news_text"]//h4//text()')[:3]
        exfil_descrip = doc.xpath('//div[@class="bc_latest_news_text"]//p//text()')[:3] 
        exfil_links = doc.xpath('//div[@class="bc_latest_news_text"]//h4//@href')[:3]

        exfil = pd.DataFrame({
            "Title": exfil_title,
            "Description": exfil_descrip,
            "Link": add_htmllink(exfil_links)
        })

        exfilrow = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Exfiltration News"),
            "Link": " "
        }, index = [0])

        exfil = pd.concat([exfilrow, exfil]).reset_index(drop = True) 

#Podcast
    elif p == podcast:
        podcast_title = doc.xpath('//div[@class="wp-block-column"]//h3//text()')[:3]
        podcast_descrip = None
        podcast_links = doc.xpath('//div[@class="wp-block-column"]//@href')[:3]

        pod = pd.DataFrame({
            "Title": podcast_title,
            "Description": podcast_descrip,
            "Link": add_htmllink(podcast_links)
        })

        podcast_row = pd.DataFrame({
            "Title": " ",
            "Description": style_source("Cybersecurity Podcasts"),
            "Link": " "
        }, index = [0])

        pod = pd.concat([podcast_row, pod]).reset_index(drop = True) 

    else:
        print(f"Something went wrong with {p}")

list_df = [pm, rm, sdlc, gc, gc2, gc3, fbi_news, exfil, pod]
final = ph.append(list_df, ignore_index = True) #append all the dataframes together

print(f"Good Morning!\nToday is {datetime.today().strftime('%A, %B %d %Y')} see below for the latest cybersecurity news.")
print("Feel free to provide feedback or improvement requests.\nHave a nice day.")

final['Title'] = [f'<b>{x}</b>' for x in final['Title']] #Bolds the title column
finalstyle = final.style.set_properties(**{'background-color': '272727', 'color': 'white'}).hide_index()
finalstyler = finalstyle.render()
with open(f"{datetime.today().strftime('%A, %B %d %Y')}.html", "w", encoding="utf-8") as text_file:
    text_file.write(finalstyler)
