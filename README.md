# Character Relationship Mapping

This is a project to test the capability of natural language processing in the process of character identification from a book series. The project consists of a webscraper, a python script to create the character maps and a second script to create a dashboard so as to visualize the character maps.

## Webscraper (scraper.ipynb)

This notebook functions to scrape the character webpage of the Witcher fandom website. The scraping of is done through the selenium library and runs windowless with the FireFox drivers provided by the Gecko Driver Manager. 

The names of the characters are stored in a pandas dataframe, matched to the books in which they appear. The names are then filtered to find only the first name of the characters and this is stored in a new column to allow more accurate identification. The column containing the books names is also cleaned to ensure that only the name of the book is kept as the webpage formatting does add unnecessary text.

## Relationship map creation


