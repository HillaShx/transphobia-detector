import param
import panel as pn
import pandas as pd
import numpy as np
import datetime
from io import BytesIO

vanilla = pn.template.VanillaTemplate(title='Vanilla Template')

# SIDEBAR

values = (datetime.datetime(2023, 1, 1), datetime.datetime(2023, 1, 1))
datetime_range_picker = pn.widgets.DatetimeRangePicker(name='Date Range Picker', value=values, enable_time=False)

vanilla.sidebar.append(datetime_range_picker)

text_input = pn.widgets.TextInput(name='Search', placeholder='Type something here...')

vanilla.sidebar.append(text_input)

multi_select = pn.widgets.MultiSelect(name='Select User', options=['adhayladim', 'blah', 'scum'], size=8)

vanilla.sidebar.append(multi_select)

def get_csv():
    return BytesIO(df.to_csv().encode())

file_download_csv = pn.widgets.FileDownload(filename="data.csv", callback=get_csv, button_type="primary")
vanilla.sidebar.append(file_download_csv)

# MAIN

# df = pd.DataFrame({'TimeStamp': ['10:00', '20:11', '13:13'], 'UserName': ['adhayladim', 'blah', 'scum'], 'Tweet': ['A', 'B', 'C'], 'Link': ['A', 'B', 'C']}, index=[1, 2, 3])
df = pd.read_csv('frontend/tweets.csv')

df_widget = pn.widgets.DataFrame(df, name='DataFrame', show_index=False)

vanilla.main.append(df_widget)

vanilla.show()