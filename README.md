# datWebScrapping
## Requieremnts
- BeautifulSoup
- requests
## Functionallity 
- Manual: the user chooses the value of each filter with a series of questions via CLI
- Automatic: the user defines a Python `list` with the value of each filter beforehand (currently there are two defined)
## Code
It is an object-oriented programming model with three main functions. Each function in the code is briefly explained with input/start data, and output/end data.
### 1. getFilters()
It is responsible for collecting the list of cities and brands available on the site.
### 2. createSearch
It is in charge of collecting the user's query or reading the predefined list, to create the url where the cars that fit a certain criteria are listed.
### 3. getCars()
It is responsible for displaying the list of cars found on each page. The user can scroll down the page by pressing `Enter`.

