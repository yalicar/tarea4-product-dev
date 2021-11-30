from starlette.responses import StreamingResponse
import uvicorn
from fastapi import FastAPI
from typing import Dict,Optional
from enum import Enum
from pydantic import BaseModel
from fastapi.responses import UJSONResponse,HTMLResponse
import io
import pandas as pd

app = FastAPI()
class RoleName(str, Enum):
    admin = 'Admin'
    writer = 'Writer'
    reader = 'Reader'

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def root():
    return {"message": "Hello World from Galileo Master!!! Seccion V"}

@app.get("/user/me")
def read_current_user():
    return {"user_id": "The corrent logged user."}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/roles/{role_name}")
def get_role_permissions(role_name: RoleName):
    if role_name == RoleName.ADMIN:
        return {"role_name": role_name, "permissions": "full acces"}
    if role_name == RoleName.write:
        return {"role_name": role_name, "permissions": ["write access"]}
    return {"role_name": role_name, "permissions": ["read access"]}

fake_items_db = [{"item_name": "uno"}, {"item_name": "dos"}, {"item_name": "tres"}]

@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
def read_item_query(item_id:int, query: Optional[str] = None):
    message = {"item_id": item_id}
    if query:
        message["query"] = query
    return message

@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: str, item_id: int,query: Optional[str] = None, describe: bool = False):
    item = {"item_id": item_id, "ouner_id": user_id}
    if query:
        item["query"] = query
    if describe:
        item["description"] = "This is a description for the item"
    
    return item

@app.post("/items/")
def create_item(item: Item):
    return {"message": "The item was succesfully created",
    "item": item.dict()
    }

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item.tax == 0 or item.tax is None:
        item.tax = item.price*0.12
    return {
        "message": "Item {} was updated",
        "item_id": item_id,
        "item": item.dict()
    }

@app.get("itemall",response_class=UJSONResponse)
def read_long_json():
    return [{"item_id": "item"}, {"item_id": "item"}, {"item_id": "item"}]

@app.get("/html",response_class=HTMLResponse)
def read_html():
    return "<html><body>Hello World</body></html>"

@app.get("/csv")
def get_csv():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    stream =io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response

# ---- Tarea usando get suma,resta, multipliacion, division ----
@app.get("/sum")
def sum(a: int, b: int):
    return {"sum": a + b}

@app.get("/resta")
def resta(a: int, b: int):
    return {"resta": a - b}

@app.get("/multiplicacion")
def multiplicacion(a: int, b: int):
    return {"multiplicacion": a * b}

@app.get("/division")
def division(a: int, b: int):
    return {"division": a / b}

# ---- Tarea usando post suma,resta, multipliacion, division ----

@app.post("/sum")
def sum_post(a: int, b: int):
    return {"sum": a + b}

@app.post("/resta")
def resta_post(a: int, b: int):
    return {"resta": a - b}

@app.post("/multiplicacion")
def multiplicacion_post(a: int, b: int):
    return {"multiplicacion": a * b}

@app.post("/division")
def division_post(a: int, b: int):
    return {"division": a / b}
    



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1 )