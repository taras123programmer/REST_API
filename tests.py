import requests

book = {'id':5,'title':'Book 1', 'author':'Author 1', 'text':'Text 1'}

response = requests.get('http://localhost:8000/book/')
print(response.json())

response = requests.post("http://localhost:8000/book/", json=book)
print(response.status_code)

response = requests.delete('http://localhost:8000/book/1')
print(response.status_code)

response = requests.get('http://localhost:8000/book/')
print(response.json())


