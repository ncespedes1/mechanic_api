from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Integer, Float, ForeignKey, Table, Column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)




ticket_mechanics = Table(
    'ticket_mechanics',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'))
)

ticket_parts = Table(
    'ticket_parts',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('inventory_id', Integer, ForeignKey('inventory.id'))
)

class Customers(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False) 
    phone: Mapped[str] = mapped_column(String(360), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', back_populates='customer')


class Mechanics(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(360), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    salary: Mapped[str] = mapped_column(String(360), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', secondary='ticket_mechanics', back_populates='mechanics')

class Service_tickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id'), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    VIN: Mapped[str] = mapped_column(String(360), nullable=False) 
    service_date: Mapped[date] = mapped_column(Date, nullable=False)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    mechanics: Mapped[list['Mechanics']] = relationship('Mechanics', secondary='ticket_mechanics', back_populates='service_tickets')
    inventory: Mapped[list['Inventory']] = relationship('Inventory', secondary='ticket_parts', back_populates='service_tickets')

class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    desc_id: Mapped[int] = mapped_column(Integer, ForeignKey('inventory_descriptions.id'), nullable=False)

    service_tickets: Mapped[list['Service_tickets']] = relationship('Service_tickets', secondary='ticket_parts', back_populates='inventory')
    inventory_description: Mapped['Inventory_descriptions'] = relationship('Inventory_descriptions', back_populates='inventory')


class Inventory_descriptions(Base):
    __tablename__ = 'inventory_descriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    inventory: Mapped[list['Inventory']] = relationship('Inventory', back_populates='inventory_description')
