import pandas as pd
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def is_published_days(date_str): # For checking for articles published today
    try:
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%d %b %Y %H:%M:%S %z")
        except ValueError:
            return False
    published_date = date_obj.date()
    today_date = datetime.now(date_obj.tzinfo).date()
    return published_date == today_date

def format_date(date_str): # For correct date format
    try:
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%d %b %Y %H:%M:%S %z")
        except ValueError:
            return date_str
    return date_obj.strftime("%B %d, %Y")

def strip_html_tags(text): # For cleaning up random html tags
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def scrape_rss(url): # For scraping comptaible RSS Feeds
    feed = feedparser.parse(url)
    entries_data = []

    if feed.bozo:
        print("Error parsing feed:", feed.bozo_exception)
        return
    
    for entry in feed.entries:
        if is_published_days(entry.published) or is_published_days(entry.get('updated', '')):
            summary = strip_html_tags(entry.summary)
            entries_data.append([entry.title, summary, entry.link, format_date(entry.published)])
    return feed.feed.title, entries_data

def parse_fbi_cyber_news(url): # For scraping the FBI cyber website
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    doc = BeautifulSoup(response.text, "html.parser")
    entries_data = []

    if response.status_code == 200:
        titles = [title.text.strip() for title in doc.select('ul.dt-tagged.filter-listing h3.title')[:5]]
        links = [link['href'] for link in doc.select('ul.dt-tagged.filter-listing h3.title a')[:5]]
        dates_published = [date.text.strip() for date in doc.select('ul.dt-tagged.filter-listing p.pat-moment.date')]
        
        today = datetime.now().date()
        date_threshold = today - timedelta(days=0)

        for title, link, date_published in zip(titles, links, dates_published):
            if lxml_published_days(date_published.strip(), date_threshold, today):
                entries_data.append([title, None, link, date_published])
        return "FBI Cyber News", entries_data
    else:
        print("Failed to retrieve the page:", response.status_code)

def parse_scmagazine(url): # For scraping a malformed rss feed
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        entries_data = []

        today = datetime.now().date()

        entries = soup.select("entry")
        for entry in entries:
            updated = entry.find("updated").text.split("T")[0]
            updated_date = datetime.strptime(updated, "%Y-%m-%d").date()

            if updated_date == today:
                title = entry.find("title").text
                published = entry.find("published").text
                summary = entry.find("summary").text
                link = entry.find("link", {"rel": "alternate"})["href"]

                if summary:
                    summary = strip_html_tags(summary).strip()

                formatted_date = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S%z").strftime("%B %d, %Y")
                entries_data.append([title, summary, link, formatted_date])
        return soup.find("title").text, entries_data
    else:
        print("Failed to retrieve the feed:", response.status_code)

def lxml_published_days(date_str, start_date, end_date): # For checking for articles published today
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        return False
    published_date = date_obj.date()
    return start_date <= published_date <= end_date

Feed_urls = [
    "https://www.wired.com/feed/category/security/latest/rss",
    "https://sdtimes.com/feed/",
    "https://cyware.com/allnews/feed",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/"
]

url_parse_function_pairs = [
    ("https://www.scmagazine.com/feed/topic/patchconfiguration-management", parse_scmagazine),
    ("https://www.scmagazine.com/feed/topic/phishing", parse_scmagazine),
    ("https://www.fbi.gov/investigate/cyber/news", parse_fbi_cyber_news)
]

output_file = "parsed_tables_pandas.html"

with open(output_file, "w", encoding="utf-8") as file:
    for url, parse_func in url_parse_function_pairs:
        feed_title, entries_data = parse_func(url)
        if entries_data:
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            df = pd.DataFrame(entries_data, columns=["Title", "Summary", "Link", "Published"])
            df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Link</a>')
            df['Published'] = df['Published'].apply(lambda x: f'<span style="font-size: smaller;">{x}</span>')
            file.write(df.to_html(index=False, justify='center', escape=False))
            file.write("<br><br>\n")
        else:
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            file.write(f"No entries found or failed to retrieve the feed from {url}.\n")

    for url in Feed_urls:
        feed_title, entries_data = scrape_rss(url)
        if entries_data:
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            df = pd.DataFrame(entries_data, columns=["Title", "Summary", "Link", "Published"])
            df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Link</a>')
            df['Published'] = df['Published'].apply(lambda x: f'<span style="font-size: smaller;">{x}</span>')
            file.write(df.to_html(index=False, justify='center', escape=False))
            file.write("<br><br>\n")
        else:
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            file.write(f"No entries found or failed to retrieve the feed from {url}.\n")

print(f"HTML tables have been written to {output_file}.")
