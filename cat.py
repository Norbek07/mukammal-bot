import requests

def get_cat_image():
    url = "https://cataas.com/cat/says/hello?fontSize=1"

    response = requests.get(url)
    
    if response.status_code == 200:
        pishak =  response.content
        
        return pishak
    return False
