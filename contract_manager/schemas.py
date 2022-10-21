from datetime import date
from typing import Optional

from pydantic import BaseModel


class Bank(BaseModel):
    name: str
    account: str
    correspondent_account: str
    bic: str


class Company(BaseModel):
    name: str
    name_short: str
    fio_rod: str
    adress: str
    ogrn: str
    inn: str
    bank: Bank


class SelfEmployed(BaseModel):
    ident: Optional[int]
    fio: str
    fio_short: str
    pasport: str
    adress: str
    phone: str
    vid_oplati: str
    balance: int
    bank: Bank


class Service(BaseModel):
    name: str
    descriptions: list[str]


class Contract(BaseModel):
    id_company: int
    id_selfemployed: int
    id_sevice: int
    additional_service_desc: Optional[list[str]] = []
    ammount: int
    contract_date: Optional[date]


class ContractInfo(BaseModel):
    ident: int
    selfemployed_name: str
    sevice_name: str
    amount: int
    contract_num: str
    contract_date: date
    is_check: bool
    is_signed: bool


class SelfEmployerInfo(BaseModel):
    ident: int
    fio_short: str


class ServiceInfo(BaseModel):
    ident: int
    name: str


class Page(BaseModel):
    contracts: list[ContractInfo]
    selfemployers: list[SelfEmployerInfo]
    serices: list[ServiceInfo]


class CheckIn(BaseModel):
    png: bytes
    ident_contract: int


class SignContact(BaseModel):
    pdf: bytes
    ident_contract: int
