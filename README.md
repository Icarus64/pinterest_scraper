The main.py is a simple python script that takes a user input which it then searches on pinterest as a query parameter and saves the loaded links to json as output data.

Pinterest uses lazy loading feature for their content loading, so this script tries to use the headless browser of pyppeteer to scroll through the web page a certain number of times as defined by the user during runtime and then extracts the loaded content.

please install the required libraries from requirements.txt before running the script via the command below.

pip install -r requirements.txt

