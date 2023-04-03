from random import randint
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from tqdm import tqdm

from avito.parser_avito import get_avito_info
from db.model import Product, Base, Avito

# from settingss import database_cinfig


# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/product', echo=False)
Session = sessionmaker(bind=engine)

def check_bd():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/product')
    if not database_exists(engine.url):
        create_database(engine.url)
    print(f'База данных {"postgresql+psycopg2://postgres:postgres@localhost/product".split("/")[-1]} созданна : {database_exists(engine.url)}')
    engine.dispose()


def clear():
    Base.metadata.drop_all(engine)
    engine.dispose()


def create_bd():
    check_bd()
    Base.metadata.create_all(engine)
    print('Таблицы созданы, база готова к работе \n')
    engine.dispose()


def add_product(data):
    with Session() as session:
        offer = session.query(Product).filter(Product.name == data['name']).first()
        if not offer:
            product = Product(
                          name=data['name'],
                          min_buy=data['min_buy'],
                          buy_price=data['buy_price'],
                          url=data['url'],
                          )
            session.add(product)
            session.commit()

    engine.dispose()

def add_avito_data():
    with Session() as session:
        offers = session.query(Product).all()
        for offer in tqdm(offers, colour='yellow'):
            if not offer.avito:
                # sleep(randint(2, 4))
                data_avito = get_avito_info(offer.__dict__)

                if data_avito != 'Нет данных/ Ошибка':
                    avito = Avito(
                                  product_id=offer.id,
                                  count_offer=data_avito['count_offer'],
                                  avg_price=data_avito['avg_price'],
                                  avito_url=data_avito['url_avito'],

                                  )
                else:
                    avito = Avito(
                                  product_id=offer.id,
                                  count_offer=0,
                                  avg_price=0,
                                  avito_url='---'

                                  )
                session.add(avito)
                session.commit()
            else:
                continue
    engine.dispose()



if __name__ == '__main__':
    # create_bd()
    add_avito_data()