from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    min_buy = Column(Integer)
    buy_price = Column(Integer)
    avito = relationship("Avito")

    def __repr__(self):
        return f' Название : {self.name} \n' \
               f' Мин Закупка : {self.min_buy} \n' \
               f' Цена покупки :  {self.buy_price} \n' \
               f' Ссылка :  {self.url}  \n' \
               f' Авито :  {self.avito}  \n' \
               f'id : {self.id}'


class Avito(Base):
    __tablename__ = 'avito'
    avito_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    count_offer = Column(Integer)
    avg_price = Column(Integer)
    avito_url = Column(String)