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
    search_results = []
    without_whitespace = ''
    index = 0
    how_many_per_page = 25
   
    while(len(without_whitespace) == 0):
        #get the html from the website 
        response = requests.get(
            baseurl,
            {
                "value": tax_form_name,
                "criteria": "formNumber",
                "submitSearch": "Find",
                "indexOfFirstRow": index,
                "sortColumn": "sortOrder",
                "resultsPerPage": how_many_per_page,
                "isDescending": "false",
            },
        )
        #append the html string into an array to be parsed later 
        search_results.append(response.text)
        #determine whether or not  we can get more results 
        #white space at the last element of pagination bottom div means that there is more results to get 
        soup = BeautifulSoup(response.text, "html.parser")
        pagination_bottom = soup.find("div", class_="paginationBottom")
        last_element = pagination_bottom.contents[len(pagination_bottom.contents)-1]
        pattern = re.compile(r'\s+')
        without_whitespace = re.sub(pattern, '', last_element)

        #go to the next page 
        index += how_many_per_page
    return search_results
    


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

#maps html into a useful form_object
def parse_all_search_results(results_array):
    parsed_results = []

    for results in results_array:
        parsed_results.append(parse_one_tax_form_search_data(results))
    
    flattened_parsed_results = [item for sublist in parsed_results for item in sublist ]
    return flattened_parsed_results


def filter_data_by_tax_form(parsed_data, tax_form_name):
    def is_exact_tax_form_name(data):
        return True if data["form_number"] == tax_form_name else False 
    
    filtered_data = filter(is_exact_tax_form_name, parsed_data)
    for tax_form in filtered_data:
        print(tax_form)
    




form_w2_data = search_one_tax_form("Form W-2")

parsed_data = parse_all_search_results(form_w2_data)
filter_data_by_tax_form(parsed_data, "Form W-2")



# then given some useful objects
# you either have a function that gives spits out json in some format based on the object
# or you download a bunch of files to some directory based of the object


#TODO
#Get all the information on every page by searching, and parsing, and filtering 
#The above is based on either what page you are on or how many entries are left in the table 

#After that I need to be able to download into a certain directory. shouldn't be that hard. I just need path and a pdf downloader library 

# then I need to be able to get the min and max data for one  for one form
#so that I can do it for multiple forms. 

#After that I need to make it all worth with the commandline 