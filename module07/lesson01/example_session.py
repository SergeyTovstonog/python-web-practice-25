"""
SQLAlchemy session
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///:memory:', echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'))
    person = relationship(Person)


'''
Як об'єкт, що зв'язує стан бази та опис бази, в Python коді виступає Base, саме цей клас відповідає за "магію" 
синхронізації таблиць у базі даних та їх опису в Python класах Person та Address.
'''

Base.metadata.create_all(engine)
Base.metadata.bind = engine

if __name__ == '__main__':

    '''
    ORM підхід виразніший. Наприклад, додавання нових записів до таблиці – це просто створення нових об'єктів класів Person 
    та Address:
    '''

    new_person = Person(fullname="Michail")
    new_person_jane = Person(fullname="Jane Doe")
    session.add(new_person)
    session.add(new_person_jane)
    '''Зверніть увагу, щоб зміни набули чинності, були записані до бази, обов'язково потрібно виконати commit.'''

    # session.commit()

    new_address = Address(post_code='36065', street_name='Mazepa', person=new_person)
    session.add(new_address)
    session.commit()

    '''Щоб отримати дані з бази, можна скористатися методом query:'''
    print('Знайти користувача')
    person = session.query(Person).filter(Person.fullname == 'Jane Doe').one()
    print(person.id, person.fullname)
    print('Знайти адреси з користувачами')
    addresses = session.query(Address).join(Address.person).all()
    # addresses = session.query(Address).all()
    for address in addresses:
        print(
            f"id: {address.id}, code: {address.post_code}, street: {address.street_name}, owner: {address.person.fullname}")
