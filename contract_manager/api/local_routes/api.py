import os
import secrets

from contract_manager import db_tools, schemas
from contract_manager.api import service
from fastapi import APIRouter, Depends, File, HTTPException, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
security = HTTPBasic()

username = os.environ.get('API_USERNAME') or 'api'
password = os.environ.get('API_PASSWORD') or 'pass'


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )
    return credentials.username


@router.post('/make-contract')
def make_contract(
    contract: schemas.Contract,
    _: str = Depends(get_current_username)
):
    service.make_contract(contract)


@router.post('/make-contracts')
def make_contracts(
    contract: schemas.Contract,
    _: str = Depends(get_current_username)
):
    service.make_contracts(contract)


@router.post('/make-company')
def make_company(
    company: schemas.Company,
    _: str = Depends(get_current_username)
):
    db_tools.update_company(company)


@router.post('/make-selfemployed')
def make_selfemployed(
    selfemployed: schemas.SelfEmployed,
    _: str = Depends(get_current_username)
):
    db_tools.update_selfemployed(selfemployed)


@router.post('/add-service')
def add_service(
    service: schemas.Service,
    _: str = Depends(get_current_username)
):
    db_tools.add_service(service)


@router.post('/get-contract')
def get_contract(
    ident: int,
    _: str = Depends(get_current_username)
):
    name, contract = db_tools.get_contract(ident)
    return Response(
        content=contract,
        media_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename={name}.pdf'
        }
    )


@router.post('/get-check')
def get_check(
    ident: int,
    _: str = Depends(get_current_username)
):
    name, check = db_tools.get_check(ident)
    return Response(
        content=check,
        media_type='image/png',
        headers={
            'Content-Disposition': f'attachment; filename={name}_check.png'
        }
    )


@router.post('/get-signed-contract')
def get_signed_contract(
    ident: int,
    _: str = Depends(get_current_username)
):
    name, contract = db_tools.get_signed_contract(ident)
    return Response(
        content=contract,
        media_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename={name}_signed.pdf'
        }
    )


@router.post('/get-page')
def get_page(
    _: str = Depends(get_current_username)
):
    return db_tools.get_page()


@router.post('/add-check')
def add_check(
    check_in: schemas.CheckIn,
    _: str = Depends(get_current_username)
):
    return db_tools.add_check(check_in)


@router.post('/add-signed-contract')
def add_signed_contract(
    ident_contract: int,
    signed_contract: bytes = File(),
    _: str = Depends(get_current_username)
):
    signed_contract_in = schemas.SignContact(
        pdf=signed_contract,
        ident_contract=ident_contract,
    )
    return db_tools.add_signed_contract(signed_contract_in)
