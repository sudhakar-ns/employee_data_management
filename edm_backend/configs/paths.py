
google_input_field = {
    "path": "name",
    "value": "q",
    "type": "input",
    "name": "Google Input Field"
}

google_search_btn = {
    "path": "name",
    "value": "btnK",
    "type": "btn",
    "name": "Google Search Button"
}

search_field = {
    "path": "id",
    "value": "search",
    "type": "input",
    "name": "Search Field"
}


""" humane website """
username_field = {
    "path": "id",
    "value": ""
}

password_field = {
    "path": "id",
    "value": ""
}

login_button = {
    "path": "id",
    "value": "loginButon"
}

download_link = lambda link_txt: {
    "path": "xpath",
    "value": f"//div[@class='name-data icon img-txt']//a[@class='name-text']/span[contains(text(), '{link_txt}')]"
}