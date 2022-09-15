import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


data = pd.read_csv('../raw_data/xy_hct_eyes_time2.csv')

#%%
import plotly.express as px
import pandas as pd
data = pd.read_csv('../raw_data/xy_hct_eyes_time2.csv')
fig = px.line(data,y=['L_EYE','R_EYE'])
fig
# %%
