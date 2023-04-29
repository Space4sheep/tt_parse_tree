# tt_parse_tree
API for paraphrasing syntax trees. Created in python with Django and using the NLTK library.
# Instructions for local deployment of the project.
1 - Copy the repository to your local storage \
2 - Create a local environment and install the packages defined in the requairements.txt file. (pip install -r requirements.txt) \
3 - Before starting the server, go to the django-project directory and run the command  -python manage.py migrate \
4 - To start the server, enter the command -python manage.py runserver
# An example of an API request:
http://127.0.0.1:8000/paraphrase?tree=(S%20(NP%20(NP%20(DT%20The)%20(JJ%20charming)%20(NNP%20Gothic)%20(NNP%20Quarter)%20)%20(,%20,)%20(CC%20or)%20(NP%20(NNP%20Barri)%20(NNP%20G%C3%B2tic)%20)%20)%20(,%20,)%20(VP%20(VBZ%20has)%20(NP%20(NP%20(JJ%20narrow)%20(JJ%20medieval)%20(NNS%20streets)%20)%20(VP%20(VBN%20filled)%20(PP%20(IN%20with)%20(NP%20(NP%20(JJ%20trendy)%20(NNS%20bars)%20)%20(,%20,)%20(NP%20(NNS%20clubs)%20)%20(CC%20and)%20(NP%20(JJ%20Catalan)%20(NNS%20restaurants)%20)%20)%20)%20)%20)%20)%20)&limit=6
-
- path: /paraphrase
- HTTP method: GET
- query parameters: \
------------------------------------------------------------------- \
tree: str (required) - a syntactic tree in the form of a string \
------------------------------------------------------------------- \
limit: int (optional, default: 20) - the maximum number of paraphrased texts that \
---------------------------------------------------------------------
