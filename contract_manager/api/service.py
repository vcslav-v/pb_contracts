import os
import shutil

from markdown import markdown
from xhtml2pdf import pisa

from contract_manager import db_tools, schemas
from datetime import datetime, date, timedelta
from random import randint


def make_contract(contract: schemas.Contract):
    company = db_tools.get_company(contract.id_company)
    selfemployed = db_tools.get_selfemployed(contract.id_selfemployed)
    service = db_tools.get_service(contract.id_sevice)
    next_contract_num = db_tools.get_next_contract_num()

    contract_date = contract.contract_date if contract.contract_date else datetime.now().date()
    contract_num = f"{contract_date.strftime('%Y%m%d')}/{next_contract_num}"
    format_data = {
        'company_name': company.name,
        'company_name_short': company.name_short,
        'company_fio_rod': company.fio_rod,
        'company_adress': company.adress,
        'company_OGRN': company.ogrn,
        'company_INN': company.inn,
        'company_bank_account': company.bank.account,
        'company_bank_name': company.bank.name,
        'company_bank_cs': company.bank.correspondent_account,
        'company_bank_bic': company.bank.bic,
        'fio': selfemployed.fio,
        'fio_short': selfemployed.fio_short,
        'pasport': selfemployed.pasport,
        'adress': selfemployed.adress,
        'phone': selfemployed.phone,
        'bank_account': selfemployed.bank.account,
        'bank_name': selfemployed.bank.name,
        'bank_cs': selfemployed.bank.correspondent_account,
        'bank_bic': selfemployed.bank.bic,
        'uslugi_short': service.name,
        'uslugi_long': ''.join(
            [f'\n - {desc}' for desc in service.descriptions + contract.additional_service_desc]
        ),
        'sum_num': contract.ammount,
        'vid_oplati': selfemployed.vid_oplati,
        'num_dogovor': contract_num,
        'date': contract_date.strftime('%d.%m.%Y')
    }

    with open(os.path.join('contract_manager', 'templates', 'template.md'), 'r') as template:
        md_template = template.read()
        md_contract = md_template.format(**format_data)
        html = markdown(md_contract)
    with open(os.path.join('contract_manager', 'templates', 'for_pdf.css'), 'r') as css_file:
        html = f'<style type="text/css">{css_file.read()}</style> {html}'

    temp_directory = str(int(datetime.now().timestamp()))
    temp_file_path = os.path.join(temp_directory, 'out.pdf')
    os.mkdir(temp_directory)
    with open(temp_file_path, 'wb') as out_pdf:
        pisa.CreatePDF(html, dest=out_pdf)
    db_tools.make_contract(temp_file_path, contract, contract_date, contract_num)
    shutil.rmtree(temp_directory)


def make_contracts(contract: schemas.Contract):
    start_contract_date = contract.contract_date if contract.contract_date else date.today()
    contract_pay = start_contract_date + timedelta(randint(20, 25))
    contract_date = contract_pay - timedelta(randint(5, 7))
    amount_contracts = randint(2, 3)
    all_amount = contract.ammount
    part_amount = all_amount / amount_contracts
    money_noise = (randint(-20, 20) / 100)
    contract_sum = int((part_amount + part_amount * money_noise) / 100) * 100
    contracts_sum = contract_sum
    gaps = [(contract_date, contract_pay, contract_sum)]
    for _ in range(amount_contracts-2):
        money_noise = (randint(-10, 10) / 100)
        contract_sum = int((part_amount + part_amount * money_noise) / 100) * 100
        contracts_sum += contract_sum

        next_contract_date, _, _ = gaps[-1]
        contract_pay = next_contract_date - timedelta(randint(1,3))
        contract_date = contract_pay - timedelta(randint(7, 10))

        gaps.append((contract_date, contract_pay, contract_sum))

    contract_sum = all_amount - contracts_sum
    next_contract_date, _, _ = gaps[-1]
    contract_pay = next_contract_date - timedelta(randint(2, 5))
    contract_date = contract_pay - timedelta(randint(7, 10))

    gaps.append((contract_date, contract_pay, contract_sum))

    for gap in gaps:
        new_contract = contract.copy()
        contract_date, contract_pay, contract_sum = gap
        new_contract.contract_date = contract_date
        new_contract.ammount = contract_sum
        make_contract(new_contract)
