from fastapi import FastAPI
from pydantic import BaseModel
import redis

class User(BaseModel):
    id: int
    name: str
    last_name: str
    age: int
    email: str
    profession: str
    specialization: str

app = FastAPI()

# Configuração do Redis
redis_host = '127.0.0.1'
redis_port = 6379       
r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

# Função para criar um novo usuário
@app.post("/users")
async def create_user(user: User):
    # Gerando ID único para o usuário (pode ser um número sequencial)
    user_id = r.incr("user_id_counter")
    user.id = user_id
    # Armazenenando o usuário no Redis usando uma chave única
    r.hmset(f"user:{user_id}", user.dict())
    return user

# Lista de todos os usuários
@app.get("/users")
async def get_users():
    # Recuperação de todas as chaves de usuários
    user_keys = r.keys("user:*")
    # Recuperação dos dados de cada usuário e transformando em objetos User
    users = [User(**r.hgetall(user_key)) for user_key in user_keys]
    return users

# Buscando usuário específico pelo id
@app.get("/users/{id}")
async def get_user(id: int):
    # Verificação da chave do usuário se existe no Redis
    if r.exists(f"user:{id}"):
        # Recuperação dos dados de cada usuário e transformando em objetos User
        user_data = r.hgetall(f"user:{id}")
        return User(**user_data)
    return None

# Função para atualizar as informações do usuário
@app.put("/users/{id}")
async def update_user(id: int, user: User):
    # Verificando se a chave do usuário existe no Redis
    if r.exists(f"user:{id}"):
        # Atualizando os dados
        r.hmset(f"user:{id}", user.dict())
        return user
    return None

# Função para excluir um usuário
@app.delete("/users/{id}")
async def delete_user(id: int):
    # Verificando se a chave do usuário existe no Redis
    if r.exists(f"user:{id}"):
        # Excluindo o usuário
        r.delete(f"user:{id}")
        return "Usuário excluído com sucesso!"
    return "Usuário não encontrado!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
