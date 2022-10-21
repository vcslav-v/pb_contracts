import os
from datetime import datetime

import requests
from cryptography.fernet import Fernet

from contract_manager import db, models, schemas

cipher_key = os.environ.get('SECRET', '')
cipher_key = cipher_key.encode()


def update_company(company: schemas.Company) -> int:
    bank_id = update_bank(company.bank)
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_bank = session.query(models.Bank).filter_by(id=bank_id).first()
        db_company = session.query(models.Company).filter_by(inn=cipher.encrypt(company.inn.encode())).first()
        if not db_company:
            db_company = models.Company(
                name=cipher.encrypt(company.name.encode()),
                name_short=cipher.encrypt(company.name_short.encode()),
                fio_rod=cipher.encrypt(company.fio_rod.encode()),
                adress=cipher.encrypt(company.adress.encode()),
                ogrn=cipher.encrypt(company.ogrn.encode()),
                inn=cipher.encrypt(company.inn.encode()),
                bank=db_bank,
            )
            session.add(db_company)
        else:
            db_company.name = cipher.encrypt(company.name.encode()),
            db_company.name_short = cipher.encrypt(company.name_short.encode())
            db_company.fio_rod = cipher.encrypt(company.fio_rod.encode())
            db_company.adress = cipher.encrypt(company.adress.encode())
            db_company.ogrn = cipher.encrypt(company.ogrn.encode())
            db_company.inn = cipher.encrypt(company.inn.encode())
            db_company.bank = db_bank
        session.commit()
        db_company_id = db_company.id
    return db_company_id


def update_bank(bank: schemas.Bank) -> int:
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_bank = session.query(models.Bank).filter_by(
            bic=cipher.encrypt(bank.bic.encode()),
            account=cipher.encrypt(bank.account.encode()),
        ).first()
        if not db_bank:
            db_bank = models.Bank(
                name=cipher.encrypt(bank.name.encode()),
                account=cipher.encrypt(bank.account.encode()),
                correspondent_account=cipher.encrypt(bank.correspondent_account.encode()),
                bic=cipher.encrypt(bank.bic.encode())
            )
            session.add(db_bank)
        else:
            db_bank.name = cipher.encrypt(bank.name.encode())
            db_bank.correspondent_account = cipher.encrypt(bank.correspondent_account.encode())
        session.commit()
        db_bank_id = db_bank.id
    return db_bank_id


def update_selfemployed(selfemployed: schemas.SelfEmployed) -> int:
    bank_id = update_bank(selfemployed.bank)
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_bank = session.query(models.Bank).filter_by(id=bank_id).first()
        if selfemployed.ident:
            db_selfemployed = session.query(
                models.SelfEmployed
            ).filter_by(id=selfemployed.ident).first()
            db_selfemployed.fio = cipher.encrypt(selfemployed.fio.encode())
            db_selfemployed.fio_short = cipher.encrypt(selfemployed.fio_short.encode())
            db_selfemployed.pasport = cipher.encrypt(selfemployed.pasport.encode())
            db_selfemployed.adress = cipher.encrypt(selfemployed.adress.encode())
            db_selfemployed.phone = cipher.encrypt(selfemployed.phone.encode())
            db_selfemployed.vid_oplati = cipher.encrypt(selfemployed.vid_oplati.encode())
            db_selfemployed.bank = db_bank
        else:
            db_selfemployed = models.SelfEmployed(
                fio=cipher.encrypt(selfemployed.fio.encode()),
                fio_short=cipher.encrypt(selfemployed.fio_short.encode()),
                pasport=cipher.encrypt(selfemployed.pasport.encode()),
                adress=cipher.encrypt(selfemployed.adress.encode()),
                phone=cipher.encrypt(selfemployed.phone.encode()),
                vid_oplati=cipher.encrypt(selfemployed.vid_oplati.encode()),
                bank=db_bank,
            )
            session.add(db_selfemployed)
        session.commit()
        db_selfemployed_id = db_selfemployed.id
    return db_selfemployed_id


def add_service(service: schemas.Service):
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        new_service = models.Service(
            name=cipher.encrypt(service.name.encode()),
        )
        for description in service.descriptions:
            new_description = models.ServiceDescription(description=cipher.encrypt(description.encode()))
            new_service.descriptions.append(new_description)
        session.add(new_service)
        session.add(new_description)
        session.commit()


def get_company(ident: int) -> schemas.Company:
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_company = session.query(models.Company).filter_by(id=ident).first()
        company_bank = schemas.Bank(
            name=cipher.decrypt(db_company.bank.name).decode(),
            account=cipher.decrypt(db_company.bank.account).decode(),
            correspondent_account=cipher.decrypt(db_company.bank.correspondent_account).decode(),
            bic=cipher.decrypt(db_company.bank.bic).decode(),
        )
        company = schemas.Company(
            name=cipher.decrypt(db_company.name).decode(),
            name_short=cipher.decrypt(db_company.name_short).decode(),
            fio_rod=cipher.decrypt(db_company.fio_rod).decode(),
            adress=cipher.decrypt(db_company.adress).decode(),
            ogrn=cipher.decrypt(db_company.ogrn).decode(),
            inn=cipher.decrypt(db_company.inn).decode(),
            bank=company_bank,
        )
        return company


def get_selfemployed(ident: int) -> schemas.SelfEmployed:
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_selfemployed = session.query(models.SelfEmployed).filter_by(id=ident).first()
        selfemployed_bank = schemas.Bank(
            name=cipher.decrypt(db_selfemployed.bank.name).decode(),
            account=cipher.decrypt(db_selfemployed.bank.account).decode(),
            correspondent_account=cipher.decrypt(db_selfemployed.bank.correspondent_account).decode(),
            bic=cipher.decrypt(db_selfemployed.bank.bic).decode(),
        )
        selfemployed = schemas.SelfEmployed(
            fio=cipher.decrypt(db_selfemployed.fio).decode(),
            fio_short=cipher.decrypt(db_selfemployed.fio_short).decode(),
            pasport=cipher.decrypt(db_selfemployed.pasport).decode(),
            adress=cipher.decrypt(db_selfemployed.adress).decode(),
            phone=cipher.decrypt(db_selfemployed.phone).decode(),
            vid_oplati=cipher.decrypt(db_selfemployed.vid_oplati).decode(),
            balance=db_selfemployed.balance,
            bank=selfemployed_bank,
        )
        return selfemployed


def get_service(ident: int) -> schemas.Service:
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_service = session.query(models.Service).filter_by(id=ident).first()
        service = schemas.Service(
            name=cipher.decrypt(db_service.name).decode(),
            descriptions=[cipher.decrypt(desc.description).decode() for desc in db_service.descriptions]
        )
        return service


def get_next_contract_num() -> int:
    with db.SessionLocal() as session:
        db_contracts_count = session.query(
            models.Contract
        ).filter_by(date=datetime.now().date()).count()
    return db_contracts_count + 1


def make_contract(
    temp_file_path: str,
    contract: schemas.Contract,
    contract_date: str,
    contract_num: str,
):
    cipher = Fernet(cipher_key)
    new_contract = models.Contract(
        num=cipher.encrypt(contract_num.encode()),
        date=contract_date,
        amount=contract.ammount,
        service_id=contract.id_sevice,
        company_id=contract.id_company,
        contractor_id=contract.id_selfemployed,
    )
    with open(temp_file_path, 'rb') as out_pdf:
        new_contract.pdf = cipher.encrypt(out_pdf.read())
    with db.SessionLocal() as session:
        session.add(new_contract)
        session.commit()


def get_contract(ident: int) -> tuple[str, bytes]:
    with db.SessionLocal() as session:
        db_contract = session.query(models.Contract).filter_by(id=ident).first()
        if not db_contract:
            return ('error', b'')
        cipher = Fernet(cipher_key)
        pdf_contract = cipher.decrypt(db_contract.pdf)
        num_contract = cipher.decrypt(db_contract.num).decode()
    return (num_contract, pdf_contract)


def get_check(ident: int) -> tuple[str, bytes]:
    with db.SessionLocal() as session:
        db_contract = session.query(models.Contract).filter_by(id=ident).first()
        if not db_contract:
            return ('error', b'')
        cipher = Fernet(cipher_key)
        png_check = cipher.decrypt(db_contract.check)
        num_contract = cipher.decrypt(db_contract.num).decode()
    return (num_contract, png_check)


def get_signed_contract(ident: int) -> tuple[str, bytes]:
    with db.SessionLocal() as session:
        db_contract = session.query(models.Contract).filter_by(id=ident).first()
        if not db_contract:
            return ('error', b'')
        cipher = Fernet(cipher_key)
        pdf_contract = cipher.decrypt(db_contract.signed)
        num_contract = cipher.decrypt(db_contract.num).decode()
    return (num_contract, pdf_contract)


def get_page() -> schemas.Page:
    with db.SessionLocal() as session:
        cipher = Fernet(cipher_key)
        db_contracts = session.query(models.Contract).all()
        contracts = []
        for db_contract in db_contracts:
            if db_contract.check and db_contract.signed:
                continue
            contracts.append(
                schemas.ContractInfo(
                    ident=db_contract.id,
                    selfemployed_name=cipher.decrypt(db_contract.contractor.fio_short).decode(),
                    sevice_name=cipher.decrypt(db_contract.service.name).decode(),
                    amount=db_contract.amount,
                    contract_num=cipher.decrypt(db_contract.num).decode(),
                    contract_date=db_contract.date,
                    is_check=True if db_contract.check else False,
                    is_signed=True if db_contract.signed else False,
                )
            )

        db_selfemployers = session.query(models.SelfEmployed).all()
        selfemployers = []
        for db_selfemployer in db_selfemployers:
            selfemployers.append(
                schemas.SelfEmployerInfo(
                    ident=db_selfemployer.id,
                    fio_short=cipher.decrypt(db_selfemployer.fio_short).decode(),
                )
            )

        db_sevices = session.query(models.Service).all()
        sevices = []
        for db_sevice in db_sevices:
            sevices.append(
                schemas.ServiceInfo(
                    ident=db_sevice.id,
                    name=cipher.decrypt(db_sevice.name).decode(),
                )
            )

    result = schemas.Page(
        contracts=contracts,
        selfemployers=selfemployers,
        serices=sevices,
    )
    return result


def add_check(check_in: schemas.CheckIn):
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_contract = session.query(models.Contract).filter_by(id=check_in.ident_contract).first()
        db_contract.check = cipher.encrypt(check_in.png)
        session.commit()


def add_signed_contract(signed_contact: schemas.SignContact):
    cipher = Fernet(cipher_key)
    with db.SessionLocal() as session:
        db_contract = session.query(models.Contract).filter_by(id=signed_contact.ident_contract).first()
        db_contract.signed = cipher.encrypt(signed_contact.pdf)
        session.commit()
