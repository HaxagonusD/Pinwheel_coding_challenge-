# Pinwheel coding Challenge - Julian Quezada

This is a tool to get info about IRS tax forms. This tool can also download these tax forms

Python Version:  Python 3.8.5
--------------
Usage: 

python3 main.py [command] [arguments, ...]

Commands available:

    --form [Form name] [Form name] [Form name] ... [destination file]
        This command will write json to the specified file
        The json will tell you what years each of the forms specified was available from the IRS

    --download [Form name] [Min Year] [Max Year]
        This command will download all forms of the specifed name between min year and max year into  ./downloaded_forms/[Form name]-[Year].pdf
    --help
        Displays this help message 

Feedback: This is a great challange because it tackles a lot of areas taht you want to test developers on. 
    - How they problem solve
    - Time compelxity  
    - Their knowledge of the language and its libraries 
    - Error handling etc

A little background: 
    - Python is not my main language right now so if you see something that's not python standard or could be done in a more "Python way" excuse my JavaScript and Node.js
    - I didn't do a lot of error handling for this since I'm already late turning this in because I didn't see the email until a week after it was sent. I think most errors should handle themselves. Like if there is an empty object in the JSON it's proably because that exact name of the form doesn't exist on the website (I didn't handle that )
    - 
