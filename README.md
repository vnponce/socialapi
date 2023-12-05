# socialapi
>Social API exercise created with FastAPI

<img width="1135" alt="Captura de pantalla 2023-12-05 a la(s) 12 13 14 a m" src="https://github.com/vnponce/socialapi/assets/11002279/0bb4971c-c954-4331-b9d8-b878ac496bdb">

## API Features:
- Register User
- Hash Password
- Create Post
- List Posts
- Create Comment in a Post by a User
- Like a post by a User (Many-to-Many Relationship)

## Tech Features: 
- Project based on Test Driven Development
- Create JWT Token
- Validate JWT Token
- Protect create Post and Comments for non-logged users
- Models with pydantic
- Routes with APIRouter from fastapi
- SQLite as db


## First steps
- Install dependencies from `requirement` file


```console
$ pip install -r requirements.txt
```

## Start project
```
python -m uvicorn main:app --reload 
```

>Go to http://127.0.0.1:8000/docs


## Tests
The project was developed considering the most coverage possible implementing TDD.
```
$ pytest
```


