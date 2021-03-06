# CS410 Final Project
The goal of this project was to develop a new search tool for UIUC's cs website [cs.illinois.edu](https://cs.illinois.edu/) that supported categorical search tools. In order to achieve this goal we developed a cli search tool, a web interface to use that search tool, as well as a script that crawls the site.

## Overview:
  We first crawl all pages at cs.illinois.edu using our web crawler. The crawler generates a csv file with information about all of the pages hosted on cs.illinois.edu. We then run our prep script in order to generate .dat files for each of the categories we supported. Leveraging the structure of the website we were able to sort pages based on the path of their url. For example, all of the instructor and staff profile pages begin with: 'cs.illinois.edu/directory'. We created a .toml file for each of the search categories we supported. These individual config tiles allowed us to separate the .dat files as well as create separate index directories. We then implemented a ranking function and a script that would accept a config file and return results. We wrapped this ranking script in both a Command Line Interface as well as a web interface. 

## Installation:
  Required programs: Python, pip  
  Required packages: metapy, scrapy, pytoml, tqdm  
  To install and run this software, you must first download Python/pip. Once that is complete, you can install the required packages (metapy for indexing and scrapy for web crawling).
  
  ## Use:
  ### Command Line interface
  In order to use the cli search tool, you need to navigate to the 'data' directory of this project and run the 'run_query' python script.
  This command take 3 arguments:
  
  * **Search Type:** User must enter: 'all', 'courses', 'news', or 'profile' as the second argument of their query. Each section returns results only from these sections of the website.
    
  * **Number of results:** User must enter an integer as the third argument of their query. The algorithm will return no more results than this value (if there are not many good matches, the program may return less than this amount)
  
  * **Query:** The last argument is the query the user would like to search for. If you would like to include more than a single word in your query, you must wrap the entire query in quotation marks.
  
  **Example:**
  
  ```python run_query.py news 3 "Lawrence Angrave"```
  
  This command will output the top 3 results in the news section of cs.illinois.edu for the query "Lawrence Angrave"
  
  **NOTE**
  The command line interface was written in python 2.7 and has some issues running in python3
  
  
  ### Web Server
  
  The setup instructions for the web server can be found in the web folder. Please setup before running the command below.
  
  Our web server was written using Flask and can be run locally using:
  
  ```python web/search_server.py```
  
  The address of the server will be printed in the terminial after the user runs this command.
  
  The web server simply uses the function we wrote for the cli and presents the information in a more user-freiendly manner. It was built using [Flask](http://flask.pocoo.org/) and [coffeescript](http://coffeescript.org/)
  
  ### Web Crawler

To run the web crawler and generate new data that the search tool you can run:

```scrapy runspider spider.py -o data.csv -t csv```

This will generate a new csv file containing the url, title, and html of every page hosted on cs.illinois.edu. In order to update the search script, you must replace the .dat file for each search category in the data folder using prep.py.

The crawler starts by going to cs.illinois.edu, dynamically loading the page with Selenium, and retrieving all the links on the page. All the text content on the page is retrieved and written to a csv file. The crawler then recursively repeats this process for all the pages that the links lead to that begine with cs.illinois.edu.

This crawler is based off of [scrapy](https://scrapy.org/)

## Contributions of Team Members

Sergey developed the initial web crawler and put the initial search functionality in place. He later improved the crawler to load pages dynamically, which allows useful searches on pages such as staff directory profiles, which have almost exclusively dynamic content.

Zach developed the script that converted the .csv files to .dat files and implemented the underlying search functions for the web server and the cli.

Arun implemented the frontend and backend for the web interface by setting up the web server and incorporating the underlying search functions into the query processor. JSON requests were used to obtain the specified filter option and user query.
