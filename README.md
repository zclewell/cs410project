# CS410 Final Project
The goal of this project was to develop a new search tool for UIUC's cs website [cs.illinois.edu](https://cs.illinois.edu/). In order to achieve this goal we developed a cli search tool, a web interface to use that search tool, as well as a script that crawls the site.

## Installation:
  Required programs: Python, pip
  Required packages: metapy, scrapy
  To install and run this software you must first download Python/pip. Once that is complete you can install the required packages (metapy   for indexing and scrapy for web crawling.
  
  ## Use:
  ### Command Line interface
  In order to use the cli search tool you need to navigate to the 'data' directory of this project and run the 'run_query' python script.
  This command take 3 arguments:
  
  * **Search Type:** User must enter: 'all', 'courses', 'news', or 'profile' as the second argument of their query. Each section returns results only from these sections of the website.
    
  * **Number of results:** User must enter an integer as the third argument of their query. The algoritm will return no more results than this value (if there are not many good matches the program may return less than this amount)
  
  * **Query:** The last argument is the query the user would like to search for. If you would like to include more than a single word in your query you must wrap the entire query in quotation marks.
  
  **Example:**
  python run_query.py news 3 "Lawrence Angrave"
  This command will output the 3 best results in the news section of cs.illinois.edu for the query "Lawrence Angrave"

