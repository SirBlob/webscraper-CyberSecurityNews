import pandas  as pd
import requests
import lxml.html

#Links that are used
url = [
    "https://cyware.com/cyber-security-news-articles",
    "https://threatpost.com/",
    "https://thehackernews.com/",
    "https://www.securitymagazine.com/topics/2236-cyber-security-news",
    "https://www.bobbythings.com"
]
df = []
df2 = []
df3 = []
df4 = []

#To parse multiple sites but to note !# each site might have their own special way
for p in url:
    page = requests.get(p)
    doc = lxml.html.fromstring(page.content)
    #If checks the variable p for which website to scrape
    if p == "https://cyware.com/cyber-security-news-articles":
        title = doc.xpath('//h1[@class="cy-card__title m-0 cursor-pointer pb-3"]/text()')
        descrip = doc.xpath('//div[@class="cy-card__description"]/text()')
        links = doc.xpath('//div[@class="cy-panel__body"]//a/@href')

        #Cleaning up the data
        titlesplit = [title.lstrip().rstrip().split(",") for title in title] #removes the new line and spaces from left and right and splits it by the ,
        descripsplit = [descrip.lstrip().rstrip().split(",") for descrip in descrip] #removes the new line and spaces from left and right and splits it by the ,

        nodupelink = list(set(links)) #remove dupelicate links
        linkclean = [word for word in nodupelink if "alert" not in word] #removes links that have the word alert
        linkssplit = [linkclean.split(',') for linkclean in linkclean] #splits it by the comma

        #Create a dataframe for the data
        df = pd.DataFrame({
            "Title": titlesplit,
            "Description": descripsplit,
            "Link": linkssplit
        })
        #Remove the brackets due to list type
        df["Title"] = df["Title"].str.join(', ')
        df["Description"] = df["Description"].str.join(', ')
        df["Link"] = df["Link"].str.join(', ')

        Siterow = pd.DataFrame({
            "Title": "Cyware",
            "Description": " ",
            "Link": " "
        }, index = [0])
        df = pd.concat([Siterow, df]).reset_index(drop = True) #Adds Siterow row to the top of the dataframe

    elif p == "https://threatpost.com/":
        title2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/text()') #selects only the text part 
        descrip2 = doc.xpath('//div[@class="c-border-layout"]//p/text()') 
        links2 = doc.xpath('//div[@class="c-border-layout"]//h2[@class="c-card__title"]//a/@href') #selects only the link part

        df2 = pd.DataFrame({
            "Title": title2,
            "Description": descrip2,
            "Link": links2
        })

        Siterow2 = pd.DataFrame({
            "Title": "Threatpost",
            "Description": " ",
            "Link": " "
        }, index = [0])
    
        df2 = pd.concat([Siterow2, df2]).reset_index(drop = True) 

    elif p == "https://thehackernews.com/":
        title3 = doc.xpath('//div[@class="clear home-post-box cf"]//h2[@class="home-title"]/text()') #selects only the text part 
        descrip3 = doc.xpath('//div[@class="clear home-post-box cf"]//div[@class="home-desc"]/text()') 
        links3 = doc.xpath('//a[@class="story-link"]/@href') #selects only the link part

        df3 = pd.DataFrame({
            "Title": title3,
            "Description": descrip3,
            "Link": links3
        })

        Siterow3 = pd.DataFrame({
            "Title": "Hacker News",
            "Description": " ",
            "Link": " "
        }, index = [0])

        df3 = pd.concat([Siterow3, df3]).reset_index(drop = True) 

    elif p == "https://www.securitymagazine.com/topics/2236-cyber-security-news": #For somer reason results in an empty dataframe
        title4 = doc.xpath('//h2[@class="headline article-summary__headline"]//a/text()') #selects only the text part 
        descrip4 = doc.xpath('//div[@class="abstract article-summary__teaser"]/text() |//div[@class="abstract article-summary__teaser"]/p/text()') #BROKEN need to fix 
        links4 = doc.xpath('//h2[@class="headline article-summary__headline"]//a/@href') #selects only the link part

        df4 = pd.DataFrame({
            "Title": title4,
            "Description": descrip4,
            "Link": links4
        })

        Siterow4 = pd.DataFrame({
            "Title": "Security Magazine",
            "Description": " ",
            "Link": " "
        }, index = [0])

        df4 = pd.concat([Siterow4, df4]).reset_index(drop = True)
    else:
        print(f"Something went wrong with {p}")

finaldf = df.append([df2, df3, df4]) #append all the dataframes together
#finaldf

#To Convert/Export the DataFrame into a CSV File
finaldf.to_csv('Summary.csv', index = False, header=True)