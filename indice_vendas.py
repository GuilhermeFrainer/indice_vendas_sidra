from sidrapy import get_table


def main():
    varejo = get_table(
        table_code="8185", 
        territorial_level="1",
        ibge_territorial_code="1",
        variable="11707",
        header="n",
        format="list",
        period="202204"
    )
    print(varejo)


if __name__ == '__main__':
    main()

    