#!/usr/bin/python
import pandas as pd
import feedparser
import requests
import tempfile
import os.path
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_days(date_str):
    """
    Check if the article was published today.
    Attempts to parse the date string and compare it with today's date.
    """
    try:
        # Try to parse the date in the common RSS format
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            # Try to parse the date in another common format if the first attempt fails
            date_obj = datetime.strptime(date_str, "%d %b %Y %H:%M:%S %z")
        except ValueError:
            return False
    # Compare the article's publication date with today's date
    published_date = date_obj.date()
    today_date = datetime.now(date_obj.tzinfo).date()
    return published_date == today_date


def format_date(date_str):
    """
    Convert the date string into a more readable format (e.g., "Month Day, Year").
    """
    try:
        # Attempt to parse the date in the first common format
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except ValueError:
        try:
            # If the first attempt fails, try another format
            date_obj = datetime.strptime(date_str, "%d %b %Y %H:%M:%S %z")
        except ValueError:
            return date_str
    # Return the formatted date string
    return date_obj.strftime("%B %d, %Y")


def strip_html_tags(text):
    """
    Remove any HTML tags from the provided text to clean up the content.
    """
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def scrape_rss(url):
    """
    Scrape and parse an RSS feed from the provided URL.
    Extract relevant information if the article was published today.
    """
    feed = feedparser.parse(url)
    entries_data = []

    if feed.bozo:
        # Handle errors if the feed could not be parsed correctly
        print("Error parsing feed:", feed.bozo_exception)
        return

    for entry in feed.entries:
        # Check if the article was published or updated today
        if is_published_days(entry.published) or is_published_days(entry.get('updated', '')):
            summary = strip_html_tags(entry.summary)
            # Collect the title, cleaned summary, link, and formatted date
            entries_data.append([entry.title, summary, entry.link, format_date(entry.published)])
    # Return the feed title and the collected data entries
    return feed.feed.title, entries_data


def parse_fbi_cyber_news(url):
    """
    Scrape the FBI cyber news website for the latest articles.
    """
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    doc = BeautifulSoup(response.text, "html.parser")
    entries_data = []

    if response.status_code == 200:
        # Extract titles, links, and publication dates for the articles
        titles = [title.text.strip() for title in doc.select('ul.dt-tagged.filter-listing h3.title')[:5]]
        links = [link['href'] for link in doc.select('ul.dt-tagged.filter-listing h3.title a')[:5]]
        dates_published = [date.text.strip() for date in doc.select('ul.dt-tagged.filter-listing p.pat-moment.date')]

        # Define the date range for filtering articles
        today = datetime.now().date()
        date_threshold = today - timedelta(days=0)

        for title, link, date_published in zip(titles, links, dates_published):
            # Check if the article was published within the desired date range
            if lxml_published_days(date_published.strip(), date_threshold, today):
                entries_data.append([title, None, link, date_published])
        # Return the feed title and the collected data entries
        return "FBI Cyber News", entries_data
    else:
        print("Failed to retrieve the page:", response.status_code)


def parse_scmagazine(url):
    """
    Scrape a malformed RSS feed from SCMagazine.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        entries_data = []

        # Get today's date
        today = datetime.now().date()

        # Extract entries from the malformed RSS feed
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
        # Return the feed title and the collected data entries
        return soup.find("title").text, entries_data
    else:
        print("Failed to retrieve the feed:", response.status_code)


def lxml_published_days(date_str, start_date, end_date):
    """
    Check if the article was published within the specified date range.
    """
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        return False
    published_date = date_obj.date()
    return start_date <= published_date <= end_date


# List of RSS feed URLs to scrape
Feed_urls = [
    "https://www.wired.com/feed/category/security/latest/rss",
    "https://sdtimes.com/feed/",
    "https://cyware.com/allnews/feed",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/"
]

# Pair URLs with their respective parsing functions
url_parse_function_pairs = [
    ("https://www.scmagazine.com/feed/topic/patchconfiguration-management", parse_scmagazine),
    ("https://www.scmagazine.com/feed/topic/phishing", parse_scmagazine),
    ("https://www.fbi.gov/investigate/cyber/news", parse_fbi_cyber_news)
]

# Get the system's temporary directory and create a file path for the output
file_path = tempfile.gettempdir()
file_name = f"{datetime.today().strftime('%A_%B_%d_%Y')}.html"
complete_path = os.path.join(file_path, file_name)

# Open the output file for writing the results
with open(complete_path, "w", encoding="utf-8") as file:
    for url, parse_func in url_parse_function_pairs:
        # Parse the FBI and SCMagazine feeds
        feed_title, entries_data = parse_func(url)
        if entries_data:
            # Write the feed title and entries to the HTML file
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            df = pd.DataFrame(entries_data, columns=["Title", "Summary", "Link", "Published"])
            df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Link</a>')
            df['Published'] = df['Published'].apply(lambda x: f'<span style="font-size: smaller;">{x}</span>')
            file.write(df.to_html(index=False, justify='center', escape=False))
            file.write("<br><br>\n")
        else:
            # Handle cases where no entries were found or the feed couldn't be retrieved
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title}</u></h3></div>\n")
            file.write(f"No entries found or failed to retrieve the feed from {url}.\n")

    for url in Feed_urls:
        # Parse general RSS feeds
        result = scrape_rss(url)
        feed_title2, entries_data2 = result
        if entries_data2:
            # Write the feed title and entries to the HTML file
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title2}</u></h3></div>\n")
            df = pd.DataFrame(entries_data2, columns=["Title", "Summary", "Link", "Published"])
            df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Link</a>')
            df['Published'] = df['Published'].apply(lambda x: f'<span style="font-size: smaller;">{x}</span>')
            file.write(df.to_html(index=False, justify='center', escape=False))
            file.write("<br><br>\n")
        else:
            # Handle cases where no entries were found or the feed couldn't be retrieved
            file.write(f"<div style='text-align: center;'><h3><u>{feed_title2}</u></h3></div>\n")
            file.write(f"No entries found or failed to retrieve the feed from {url}.\n")

# Output the path to the generated HTML file
print(complete_path)
