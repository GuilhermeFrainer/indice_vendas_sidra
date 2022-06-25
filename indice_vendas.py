from heapq import merge
from numpy import indices, number
from sidrapy import get_table
from user_config import *
from index import Index
import datetime
import xlsxwriter
import json


# Global variables
merge_format = None
indices_length = None
date_format = None


def main():

    period = get_period()
    indices = get_data(period)

    workbook, worksheet = list_to_workbook(indices)
    write_formulas(workbook, worksheet)
    make_chart(workbook, indices)

    workbook.close()


def make_chart(workbook : xlsxwriter.Workbook, indices : list[Index]):
    
    global indices_length

    chart_start = chart_start_finder(indices)
    chartsheet = workbook.add_chartsheet('Gráfico')
    chart = workbook.add_chart({'type': 'line'})

    chart.add_series({
        'name': 'Varejo',
        'categories': f'=Dados!$A${6 + chart_start}:$A${5 + indices_length}',
        'values': f'=Dados!$G${6 + chart_start}:$G${5 + indices_length}',
        'line': {'color': '#c00000'}
    })

    chart.add_series({
        'name': 'Varejo ampliado',
        'categories': f'=Dados!$A${6 + chart_start}:$A${5 + indices_length}',
        'values': f'=Dados!$H${6 + chart_start}:$H${5 + indices_length}',
        'line': {'color': '#4472c4'}
    })

    chart.add_series({
        'name': 'Indústria',
        'categories': f'=Dados!$A${6 + chart_start}:$A${5 + indices_length}',
        'values': f'=Dados!$I${6 + chart_start}:$I${5 + indices_length}',
        'line': {'color': '#70ad47'}
    })

    chart.add_series({
        'name': 'Serviços',
        'categories': f'=Dados!$A${6 + chart_start}:$A${5 + indices_length}',
        'values': f'=Dados!$J${6 + chart_start}:$J${5 + indices_length}',
        'line': {'color': '#ffc000'}
    })

    chart.add_series({
        'categories': f'=Dados!$A${6 + chart_start}:$A${5 + indices_length}',
        'values': f'=Dados!$K${6 + chart_start}:$K${5 + indices_length}',
        'line': {'color': 'black'}
    })

    chart.set_x_axis(x_axis_config)
    chart.set_y_axis(y_axis_config)
    chart.set_legend(legend_config)

    chartsheet.set_chart(chart)

# Returns position of chart start date
def chart_start_finder(indices : list[Index]):
    
    global indices_length

    dates = []
    for i in range(indices_length):
        dates.append(indices[i].date)

    chart_start = CHART_START_DATE
    chart_start = datetime.date.fromisoformat(chart_start)

    for i in range(len(dates)):
        if dates[i] == chart_start:
            return i


def write_formulas(workbook : xlsxwriter.Workbook, worksheet : xlsxwriter.Workbook.worksheet_class):
    
    global merge_format

    number_format = workbook.add_format({'num_format': '##0.0'})
    
    # Writes headers
    worksheet.merge_range('G1:J1', 'Valores de correção a partir de 2018', merge_format)
    worksheet.merge_range('G4:J4', 'Corrigidos', merge_format)

    worksheet.write('G5', 'Varejo')
    worksheet.write('H5', 'Varejo ampliado')
    worksheet.write('I5', 'Indústria')
    worksheet.write('J5', 'Serviços')
    worksheet.write('K5', 100)

    # Writes values to adjust to
    worksheet.write_formula('G2', f'=LARGE(B6:B{5 + indices_length},1)', number_format)
    worksheet.write_formula('H2', f'=LARGE(C6:C{5 + indices_length},1)', number_format)
    worksheet.write_formula('I2', f'=LARGE(D6:D{5 + indices_length},1)', number_format)
    worksheet.write_formula('J2', f'=LARGE(E6:E{5 + indices_length},1)', number_format)

    # Writes months of the values above
    worksheet.write_formula('G3', f'=INDEX($A6:$A{indices_length + 5},MATCH(G2,B6:B{indices_length + 5},0))', date_format)
    worksheet.write_formula('H3', f'=INDEX($A6:$A{indices_length + 5},MATCH(H2,C6:C{indices_length + 5},0))', date_format)
    worksheet.write_formula('I3', f'=INDEX($A6:$A{indices_length + 5},MATCH(I2,D6:D{indices_length + 5},0))', date_format)
    worksheet.write_formula('J3', f'=INDEX($A6:$A{indices_length + 5},MATCH(J2,E6:E{indices_length + 5},0))', date_format)

    # Actually writes formulas
    for i in range(indices_length):
        worksheet.write_formula(f'G{6 + i}', f'=B{6 + i}*100/G$2', number_format)
        worksheet.write_formula(f'H{6 + i}', f'=C{6 + i}*100/H$2', number_format)
        worksheet.write_formula(f'I{6 + i}', f'=D{6 + i}*100/I$2', number_format)
        worksheet.write_formula(f'J{6 + i}', f'=E{6 + i}*100/J$2', number_format)
        worksheet.write(f'K{6 + i}', 100)


# Takes the data and puts it into an Excel file. Returns workbook and worksheet
def list_to_workbook(indices : list[Index]):
    
    global indices_length
    global date_format

    workbook = xlsxwriter.Workbook('índices_de_vendas_py.xlsx')
    worksheet = workbook.add_worksheet('Dados')

    global merge_format 
    merge_format = workbook.add_format({'align': 'center'})

    worksheet.write('A5', 'Mês')
    worksheet.write('B5', 'Varejo')
    worksheet.write('C5', 'Varejo ampliado')
    worksheet.write('D5', 'Indústria')
    worksheet.write('E5', 'Serviços')

    worksheet.merge_range('B4:E4', 'Inalterados', merge_format)

    # Writes the data into the worksheet
    date_format = workbook.add_format({'num_format': 'mmm-yy'})
    
    indices_length = len(indices)

    for i in range(indices_length):
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

    # Determines the longest series
    lengths = [len(retail), len(ext_retail), len(industry), len(services)]
    longest = 0

    for i in range(len(lengths)):

        if lengths[i] > longest:
            longest = lengths[i]

    indices = []

    for i in range(longest):

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

    