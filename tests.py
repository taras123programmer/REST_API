import requests

response = requests.get(f"http://localhost:5000/token?username=taras&password=123")
tokens = response.json()
token = tokens['access_token']

book = {'title':'Book 10', 'author':'Author 10', 'text':'Text 10'}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get('http://localhost:5000/book/', headers=headers)

print(response.json())

response = requests.post("http://localhost:5000/book/", json=book, headers=headers)
print(response.status_code)
print(response.text)

id = input()
print(id)
response = requests.delete('http://localhost:5000/book/'+id, headers=headers)
print(response.status_code)

response = requests.get('http://localhost:5000/book/', headers=headers)
print(response.json())


