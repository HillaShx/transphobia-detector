import param
import panel as pn
import pandas as pd
import numpy as np

class Dashboard(param.Parameterized):
    df = param.DataFrame()
    # df = pd.read_csv('frontend/tweets.csv')
    # search = param.String(default="", doc="A string")
    users = []
    username = param.ObjectSelector(default=None, objects=users)

    def __init__(self, **params):
        super().__init__(**params)
        self.df = pd.read_csv('frontend/tweets.csv')

    @param.depends('df')
    def get_users(self):
        self.users = set(self.df['username'])
        return self.users

    @param.depends('username', watch=True)
    def view_df(self):
        # df_widget = pn.widgets.DataFrame(self.df, name='DataFrame', show_index=False)
        # return df_widget
        filtered_df = self.df.query('username=="username"')
        return pn.widgets.DataFrame(filtered_df, name='DataFrame', show_index=False)

dash = Dashboard(name='Dashboard')
# pn.Row(dash.param, dash.view_df).show()

vanilla = pn.template.VanillaTemplate(title='Vanilla Template')
vanilla.sidebar.append(dash.param)
vanilla.main.append(dash.view_df)
vanilla.show()
