import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import sys
import json


# this needs search
# you give a function some parameters and you get back some html
baseurl = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"


# Takes in the the name of one form as a string
# Returns the search results as a list of html strings 
def search_one_tax_form(tax_form_name):
    search_results = []
    without_whitespace = ""
    index = 0
    how_many_per_page = 25

    while len(without_whitespace) == 0:
        # get the html from the website
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
        # append the html string into an array to be parsed later
        search_results.append(response.text)
        # determine whether or not  we can get more results
        # white space at the last element of pagination bottom div means that there is more results to get
        soup = BeautifulSoup(response.text, "html.parser")
        pagination_bottom = soup.find("div", class_="paginationBottom")
        last_element = pagination_bottom.contents[len(pagination_bottom.contents) - 1]
        pattern = re.compile(r"\s+")
        without_whitespace = re.sub(pattern, "", last_element)

        # go to the next page
        index += how_many_per_page
    return search_results


# Then it needs a parser
# you get some html and you get back some useful objects
def parse_one_tax_form_search_data(tax_form_search_data):
    soup = BeautifulSoup(tax_form_search_data, "html.parser")

    form_objects = []
    table_rows_list = soup.find_all("tr", class_=True)

    for table_row in table_rows_list:
        form_objects.append(
            {
                "form_number": re.sub(
                    "\s+", " ", table_row.contents[1].contents[1].string
                ).strip(),
                "form_title": re.sub("\s+", " ", table_row.contents[3].string).strip(),
                "year": re.sub("\s+", " ", table_row.contents[5].string).strip(),
                "link": table_row.contents[1].contents[1]["href"],
            }
        )
    return form_objects


# maps html into a useful form_object
def parse_all_search_results(results_array):
    parsed_results = []

    for results in results_array:
        parsed_results.append(parse_one_tax_form_search_data(results))
    #flatten all the forms_objects into one big array 
    flattened_parsed_results = [item for sublist in parsed_results for item in sublist]
    return flattened_parsed_results

# give me back only the forms whose names match exactly
def filter_data_by_tax_form(parsed_data, tax_form_name):
    def is_exact_tax_form_name(data):
        return True if data["form_number"] == tax_form_name else False

    filtered_data = filter(is_exact_tax_form_name, parsed_data)
    return list(filtered_data)


# create a dictionary with form info. will be turned into JSON later 
def get_min_max_years(list_of_form_names):
    min_max_year_results = []

    for form_name in list_of_form_names:

        form_data = search_one_tax_form(form_name)
        parsed_data = parse_all_search_results(form_data)
        filtered_data = filter_data_by_tax_form(parsed_data, form_name)
        min_year = int(filtered_data[0]["year"])
        max_year = int(filtered_data[0]["year"])

        for form in filtered_data:
            if int(form["year"]) > max_year:
                max_year = int(form["year"])
            elif int(form["year"]) < min_year:
                min_year = int(form["year"])
        data_to_push = {
            "form_number": filtered_data[0]["form_number"],
            "form_title": filtered_data[0]["form_title"],
            "min_year": min_year,
            "max_year": max_year,
        }

        min_max_year_results.append(data_to_push)
        return min_max_year_results

#  writes to ./downlaoded_forms all the forms that can be found between specifed years
def download_forms(form_name, min_year, max_year):
    html = search_one_tax_form(form_name)
    form_objects = parse_all_search_results(html)
    filtered_form_objects = filter_data_by_tax_form(form_objects, form_name)
    # ight error handling
    if min_year > max_year:
        print("Minimum year is greater than maximum year")
        return 0

    for form_object in filtered_form_objects:
        year = int(form_object["year"])
        if year >= min_year and year <= max_year:
            file = Path(
                "downloaded_forms/" + form_name + " - " + form_object["year"] + ".pdf"
            )
            response = requests.get(form_object["link"])
            file.write_bytes(response.content)


# start the command line interface
command = sys.argv[1]
arguements = sys.argv[2:]

if command == "--forms":
    results = get_min_max_years(arguements[:-1])
    file = Path(arguements[len(arguements) - 1])
    file.write_text(json.dumps(results))
    print("Your results are in " + arguements[len(arguements) - 1])
elif command == "--download":
    download_forms(arguements[0], int(arguements[1]), int(arguements[2]))
    print("Your forms should be in ./downloaded_forms")
elif command == "--help":
    print("This is a tool to get info about IRS tax forms. This tool can also download these tax forms")
    print("--------------")
    print("Usage: ")
    print("")
    print("python3 main.py [command] [arguments, ...]")
    print("")
    print("Commands available:")
    print("    --form [Form name] [Form name] [Form name] ... [destination file]")
    print("        This command will write json to the specified file")
    print(
        "        The json will tell you what years each of the forms specified was available from the IRS"
    )
    print("")
    print("    --download [Form name] [Min Year] [Max Year]")
    print(
        "        This command will download all forms of the specifed name between min year and max year into  ./downloaded_forms/[Form name]-[Year].pdf"
    )
    print("    --help")
    print("        Displays this help message ")


