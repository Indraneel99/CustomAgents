import requests

response = requests.post("http://localhost:8000/invoke",
                         json = {'input' : {'input':'what is the sum of 2 and 3'}})

print(response.json()['output']['output'])