# socialapi
>Social API exercise created with FastAPI

![Captura de pantalla 2023-12-05 a la(s) 12.08.32 a.m..png](..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fs7%2F7jbv65r518g78j3nc658bpmm0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_ycRsmE%2FCaptura%20de%20pantalla%202023-12-05%20a%20la%28s%29%2012.08.32%E2%80%AFa.m..png)

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


