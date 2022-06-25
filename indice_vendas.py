from sidrapy import get_table
from user_config import *
from index import Index
import datetime
import json


def main():

    period = get_period()
    indices = get_data(period)


# Returns period string going from chosen start date to current month
def get_period():
    
    today = datetime.date.today()
    start_date = datetime.date.fromisoformat(START_DATE)
    return f"{start_date.year}{start_date.month:02d}-{today.year}{today.month:02d}"


# Gets the data form the API and returns a list of objects from the Index class
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

    retail = api_to_list(retail) 
    ext_retail = api_to_list(ext_retail) 
    industry = api_to_list(industry) 
    services = api_to_list(services)

    indices = []

    # Possible problem if not all series are up to date
    for i in range(len(retail)):

        indices.append(Index(retail[i]["date"], retail[i]["value"], ext_retail[i]["value"], industry[i]["value"], services[i]["value"]))
    
    return indices

# Gets api data and returns it as a list of dicts
def api_to_list(list: list):
    
    out_list = []

    for i in range(len(list)):
        out_list.append({"date": list[i]["D2C"], "value": list[i]["V"]})

    return out_list


if __name__ == '__main__':
    main()

    