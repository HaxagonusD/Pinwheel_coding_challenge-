import requests
from bs4 import BeautifulSoup


# response = requests.get('https://httpbin.org/ip')

# print('Your IP is {0}'.format(response.json()['origin']))

# this needs search
# you give a fucntion some parameters and you get back some html
baseurl = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"


# Takes in the the name of one form as a string
# Returns the search results as a string of html
def search_one_tax_form(tax_form_name):
    response = requests.get(
        baseurl,
        {
            "value": tax_form_name,
            "criteria": "formNumber",
            "submitSearch": "Find",
            "indexOfFirstRow": 0,
            "sortColumn": "sortOrder",
            "resultsPerPage": 25,
            "isDescending": "false",
        },
    )
    return response.text


# Then it needs a parser
# you get some html and you get back some useful objects
def parse_one_tax_form_search_data(tax_form_search_data):
    soup = BeautifulSoup(tax_form_search_data, "html.parser")
   
    form_objects = []
    table_rows_list = soup.find_all("tr", class_=True)
    print(table_rows_list)
    print(len(table_rows_list))
    


form_w2_data = search_one_tax_form("form w2")
parse_one_tax_form_search_data(form_w2_data)


# then given some useful objects
# you either have a function that gives spits out json in some format based on the object
# or you download a bunch of files to some directory based of the object
