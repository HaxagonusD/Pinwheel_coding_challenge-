import requests
from bs4 import BeautifulSoup
import re


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
    # print(table_rows_list[0].contents[1].contents[1].string)
    for table_row in table_rows_list:
        form_objects.append(
            {
                "form_number": re.sub(
                    "\s+", " ", table_row.contents[1].contents[1].string
                ).strip(),
                "form_title": re.sub("\s+", " ", table_row.contents[3].string).strip(),
                "year": re.sub("\s+", " ", table_row.contents[5].string).strip(),
            }
        )
    return form_objects

def filter_data_by_tax_form(parsed_data, tax_form_name):
    def is_exact_tax_form_name(data):
        return True if data["form_number"] == tax_form_name else False 
    
    filtered_data = filter(is_exact_tax_form_name, parsed_data)
    for tax_form in filtered_data:
        print(tax_form)
    
   


    


form_w2_data = search_one_tax_form("form w2")
parsed_data = parse_one_tax_form_search_data(form_w2_data)
filter_data_by_tax_form(parsed_data, "Form W-2")


# then given some useful objects
# you either have a function that gives spits out json in some format based on the object
# or you download a bunch of files to some directory based of the object


#TODO
#Get all the information on every page by searching, and parsing, and filtering 
#The above is based on either what apge youa re on or how many entries are left in the table 

#After that I need to be able to download into a certain directory. shouldn't be that hard. I just need path and a pdf downloader library 

# then I need to be able to get the min and max data for one  for one form
#so that I can do it for multiple forms. 

#After that I need to make it all worth with the commandline 