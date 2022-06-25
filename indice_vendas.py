from sidrapy import get_table
from user_config import *
from index import Index
import datetime
import json


def main():

    period = get_period()
    retail, ext_retail, industry, services = get_data(period)

    print("Varejo:")
    print(retail)
    print("Varejo ampliado")
    print(ext_retail)
    print("Indústria")
    print(industry)
    print("Serviços")
    print(services)

# Returns period string going from chosen start date to current month
def get_period():
    
    today = datetime.date.today()
    start_date = datetime.date.fromisoformat(START_DATE)
    return f"{start_date.year}{start_date.month:02d}-{today.year}{today.month:02d}"


# Gets the data form the API and returns lists with dates and values
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
        ibge_territorial_code="1",
        variable="11707",
        header="n",
        format="list",
        period=period,
        classifications={"11046": "56735"}
    )

    industry = get_table(
        table_code="8159",
        territorial_level="1",
        ibge_territorial_code="1",
        variable="11600",
        header="n",
        format="list",
        period=period,
        classifications={"544": "129314"}
    )

    services = get_table(
        table_code="8161",
        territorial_level="1",
        ibge_territorial_code="1",
        variable="11622",
        header="n",
        format="list",
        period=period,
        classifications={"11046": "56725"}
    )


    return api_to_list(retail), api_to_list(ext_retail), api_to_list(industry), api_to_list(services)
    

# Gets api data and returns it as a list of dicts
def api_to_list(list: list):
    
    out_list = []

    for i in range(len(list)):
        out_list.append({"date": list[i]["D2C"], "value": list[i]["V"]})

    return out_list


if __name__ == '__main__':
    main()

    