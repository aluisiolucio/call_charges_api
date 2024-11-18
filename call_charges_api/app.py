from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from call_charges_api.api.v1.routes import call_record, phone_bill

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['POST', 'GET', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*'],
)


app.include_router(call_record.router)
app.include_router(phone_bill.router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': '/'}
