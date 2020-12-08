# webscraper-CyberSecurityNews
A personal project to create a web scraper for cyber security news that exports the data to a csv file.

## Installation
This project is based on python, please ensure the version is at least 3.8.0 32 bit to ensure there are no complications.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following modules.

```bash
pip install pandas
pip install requests
pip install lxml
```

## Project Status
The main functionalities of the script is done but some other ideas I have are the below.

### Improvements to still be made
1. Better Error Handling
2. Search/Emphasize on specific key words
3. Automate running and sending the file in the morning

### Reflections
1. Not easily scalable but is fine for small list of websites. 
If need speed and/or large list of sites to scrape the module Scrapy is probably a better idea.

2. Can easily be broken if the xpath selector is changed.
