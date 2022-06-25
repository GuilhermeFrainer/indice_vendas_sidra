from heapq import merge
from sidrapy import get_table
from user_config import *
from index import Index
import datetime
import xlsxwriter
import json


def main():

    period = get_period()
    indices = get_data(period)

    workbook, worksheet = list_to_workbook(indices)

    workbook.close()


# Takes the data and puts it into an Excel file. Returns workbook and worksheet
def list_to_workbook(indices : list[Index]):
    
    workbook = xlsxwriter.Workbook('Índices de vendas.xlsx')
    worksheet = workbook.add_worksheet('Dados')

    # Writes headers for unadjusted data
    merge_format = workbook.add_format({'align': 'center'})
    
    worksheet.write('A5', 'Mês')
    worksheet.write('B5', 'Varejo')
    worksheet.write('C5', 'Varejo ampliado')
    worksheet.write('D5', 'Indústria')
    worksheet.write('E5', 'Serviços')

    worksheet.merge_range('B4:E4', 'Inalterados', merge_format)

    # Writes the data into the worksheet
    date_format = workbook.add_format({'num_format': 'mmm-yy'})
    
    for i in range(len(indices)):
        worksheet.write_datetime(f'A{6 + i}', indices[i].date, date_format)
        worksheet.write(f'B{6 + i}', indices[i].retail)
        worksheet.write(f'C{6 + i}', indices[i].ext_retail)
        worksheet.write(f'D{6 + i}', indices[i].industry)
        worksheet.write(f'E{6 + i}', indices[i].services)

    return workbook, worksheet

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
        classifications={"11046": "56736"}
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
        classifications={"11046": "56726"}
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
        out_list.append({"date": list[i]["D2C"], "value": float(list[i]["V"])})

    return out_list


if __name__ == '__main__':
    main()

    