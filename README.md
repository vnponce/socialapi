# socialapi
Social API exercise  created with FastAPI

Implements: 
- Models with pydantic
- Routes with APIRouter from fastapi

## First steps
- Install dependencies from `requirement` file


```console
$ pip install -r requirements.txt
```

## Start project
python -m uvicorn main:app --reload 

Go to http://127.0.0.1:8000/docs


## Tests
The project was developed considering the most coverage possible implementing TDD.
```
$ pytest
```



