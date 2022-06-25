# Stores user preferences


START_DATE = "2012-01-01"

# Chart preferences
CHART_START_DATE = "2018-01-01"

x_axis_config = {
    'num_font': {
        'name': 'Calibri',
        'size': 12,
        'rotation': -45 
        },
    'date_axis': True,
    'label_position': 'low',
    'major_unit': 2,
    'major_unit_type': 'months'
}

y_axis_config = {
    'num_font': {'name': 'Calibri', 'size': 12},
    'min': 60,
    'max': 100,
    'major_unit': 5,
    'major_gridlines': {'visible': False}
}

legend_config = {
    'position': 'bottom',
    'font': {'name': 'Calibri', 'size': 12},
    'delete_series': [4]
}