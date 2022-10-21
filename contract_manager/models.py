from sqlalchemy import Column, Date, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Company(Base):
    '''Company.'''

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(LargeBinary)
    name_short = Column(LargeBinary)
    fio_rod = Column(LargeBinary)
    adress = Column(LargeBinary)
    ogrn = Column(LargeBinary)
    inn = Column(LargeBinary)
    bank_id = Column(Integer, ForeignKey('banks.id'))
    bank = relationship('Bank', back_populates='company')
    contracts = relationship('Contract', back_populates='company')


class Bank(Base):
    '''Bank.'''

    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    name = Column(LargeBinary)
    account = Column(LargeBinary)
    correspondent_account = Column(LargeBinary)
    bic = Column(LargeBinary)
    company = relationship('Company', uselist=False, back_populates='bank')
    self_employed = relationship('SelfEmployed', uselist=False, back_populates='bank')


class SelfEmployed(Base):
    '''Self employed.'''

    __tablename__ = 'self_employeds'

    id = Column(Integer, primary_key=True)
    fio = Column(LargeBinary)
    fio_short = Column(LargeBinary)
    pasport = Column(LargeBinary)
    adress = Column(LargeBinary)
    phone = Column(LargeBinary)
    vid_oplati = Column(LargeBinary)
    balance = Column(Integer, default=0)
    bank_id = Column(Integer, ForeignKey('banks.id'))
    bank = relationship('Bank', back_populates='self_employed')
    contracts = relationship('Contract', back_populates='contractor')


class Service(Base):
    '''Service.'''

    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(LargeBinary)
    descriptions = relationship('ServiceDescription')
    contracts = relationship('Contract', back_populates='service')


class ServiceDescription(Base):
    '''Service description.'''

    __tablename__ = 'service_descriptions'

    id = Column(Integer, primary_key=True)
    description = Column(LargeBinary)
    service_id = Column(Integer, ForeignKey('services.id'))


class Contract(Base):
    '''Contract.'''

    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True)
    num = Column(LargeBinary)
    date = Column(Date)
    amount = Column(Integer)
    service_id = Column(Integer, ForeignKey('services.id'))
    service = relationship('Service', back_populates='contracts')
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='contracts')
    contractor_id = Column(Integer, ForeignKey('self_employeds.id'))
    contractor = relationship('SelfEmployed', back_populates='contracts')
    pdf = Column(LargeBinary)
    signed = Column(LargeBinary)
    check = Column(LargeBinary)
