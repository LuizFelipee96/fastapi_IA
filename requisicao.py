import requests
import json

# Dados do usuário em um formato dicionário
user_data = {
    "id": 1,
    "name": "Regina",
    "last_name": "Menezes",
    "age": 70,
    "email": "reginamenezes@hotmail.com",
    "profession": "Dentista",
    "specialization": "Pesquisadora"
}

# URL da API
url = "http://localhost:8000/users/"

# Solicitação POST para criar o usuário
response = requests.post(url, json=user_data)

# Resposta da solicitação
if response.status_code == 200:
    print("Usuário criado com sucesso.")
else:
    print("Erro ao criar usuário. Status code:", response.status_code)
    






