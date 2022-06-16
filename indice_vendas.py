from sidrapy import get_table


def main():
    varejo = get_table(table_code="8185", territorial_level="1", ibge_territorial_code="all", verify_ssl=False)


if __name__ == '__main__':
    main()

    