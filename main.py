from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
from faker import Faker

class User(BaseModel):
    id: int
    username: str 
    password: str
    name: str
    age: int
    email: str

app = FastAPI()
fake = Faker()

users = [
    {'id': 1, 'username': 'user1', 'password': '111aaa', 'name': fake.name(), 'age': 21, 'email': fake.email()},
    {'id': 2, 'username': 'user2', 'password': '222sss', 'name': fake.name(), 'age': 22, 'email': fake.email()},
    {'id': 3, 'username': 'user3', 'password': '333ddd', 'name': fake.name(), 'age': 23, 'email': fake.email()}
]

async def get_user(id: int):
    for user in users:
        if user['id'] == id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

@app.get('/users/{id}', response_model=User)
async def read_user(user: User = Depends(get_user)):
    return user


@app.post('/users/', response_model=User)
async def create_user(user: User):
    users.append(user.dict())
    return user.dict()

@app.put('/users/{id}', response_model=User) 
async def update_user(
    user: User = Depends(get_user), username: str = None, password: str = None, name: str = None, age: int = None, email: str = None
):
    user['username'] = username or user['username']
    user['password'] = password or user['password']
    user['name'] = name or user['name']
    user['age'] = age or user['age']
    user['email'] = email or user['email']
    return user

@app.delete('/users/{id}')
async def delete_user(user: User = Depends(get_user)):
    users.remove(user.dict())
    return status.HTTP_204_NO_CONTENT