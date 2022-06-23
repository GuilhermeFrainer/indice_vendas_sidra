from sidrapy import get_table
from user_config import *
import datetime
import json


def main():

    period = get_period()

    #print(json.dumps(varejo, indent=4))


# Returns period string going from chosen start date to current month
def get_period():
    
    today = datetime.date.today()
    start_date = datetime.date.fromisoformat(START_DATE)
    return f"{start_date.year}{start_date.month}-{today.year}{today.month}"


def get_data(period : str):
    
    retail = get_table(
        table_code="8185", 
        territorial_level="1",
        ibge_territorial_code="1",
        variable="11707",
        header="n",
        format="list",
        period=period,
        classifications={"11046": "56734"},
    )

    ext_retail = get_table(
        table_code="8186",
        territorial_level="1",
        ibge_territorial_code="1"
    )

    industry = get_table(
        table_code="8159",
        territorial_level="1",
        ibge_territorial_code="1"
    )

    services = get_table(
        table_code="8161",
        territorial_level="1",
        ibge_territorial_code="1"
    )

    
if __name__ == '__main__':
    main()

    