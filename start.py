from db.ORM import add_avito_data
from trend_opt.parser import get_trend_opt
from avito.parser_avito import get_parse_avito, test_ip
import pandas

from utils import get_my_ip, from_sql_to_exel


def to_exel():
    pandas.read_json("files/offers.json").to_excel("files/output.xlsx")


if __name__ == '__main__':
    # get_my_ip()
    get_trend_opt()
    add_avito_data()
    from_sql_to_exel()


