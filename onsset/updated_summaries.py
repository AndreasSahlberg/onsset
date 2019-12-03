"""
This script produces the summary analysis required to provide input data for the OSeMOSYS soft-link
"""

SET_TOTAL_ENERGY_PER_CELL = "TotalEnergyPerCell"
SET_ELEC_FINAL_CODE = "FinalElecCode"
SET_ELEC_CURRENT = 'ElecStart'
SET_POP = 'Pop'
SET_NEW_CONNECTIONS = 'NewConnections'
SET_NEW_CAPACITY = 'NewCapacity'
SET_INVESTMENT_COST = 'InvestmentCost'

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
# from runner import *

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

messagebox.showinfo('OnSSET', 'Open the csv file with results data')
result_csv_path = filedialog.askopenfilename()
df_in = pd.read_csv(result_csv_path)

elements = ["1.Population", "2.New_Connections", "3.Capacity", "4.Investment", "5. Demand", "6. Transmission summaries", "7. Distribution summaries"]
techs = ["Grid", "SA_Diesel", "MG_Diesel", "MG_PV", "MG_Wind", "MG_Hydro", "SA_PV_1", "SA_PV_2", "SA_PV_3", "SA_PV_4", "SA_PV_5"]
years = [2025, 2030, 2070]
tech_codes = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]


for year in years:
    df_in.loc[(df_in[SET_ELEC_FINAL_CODE + '{}'.format(year)] == 3) & (df_in['PVType' + '{}'.format(year)] == 1), SET_ELEC_FINAL_CODE + '{}'.format(year)] = 8
    df_in.loc[(df_in[SET_ELEC_FINAL_CODE + '{}'.format(year)] == 3) & (df_in['PVType' + '{}'.format(year)] == 2), SET_ELEC_FINAL_CODE + '{}'.format(year)] = 9
    df_in.loc[(df_in[SET_ELEC_FINAL_CODE + '{}'.format(year)] == 3) & (df_in['PVType' + '{}'.format(year)] == 3), SET_ELEC_FINAL_CODE + '{}'.format(year)] = 10
    df_in.loc[(df_in[SET_ELEC_FINAL_CODE + '{}'.format(year)] == 3) & (df_in['PVType' + '{}'.format(year)] == 4), SET_ELEC_FINAL_CODE + '{}'.format(year)] = 11
    df_in.loc[(df_in[SET_ELEC_FINAL_CODE + '{}'.format(year)] == 3) & (df_in['PVType' + '{}'.format(year)] == 5), SET_ELEC_FINAL_CODE + '{}'.format(year)] = 12

df_electrified = df_in.loc[df_in[SET_ELEC_CURRENT] == 1]
df_unelectrified = df_in.loc[df_in[SET_ELEC_CURRENT] == 0]

sumtechs = []
for element in elements:
    for tech in techs:
        sumtechs.append(element + "_" + tech)

total_rows = len(sumtechs)

electrified_sumtechs = pd.DataFrame(columns=years)
unelectrified_sumtechs = pd.DataFrame(columns=years)

for row in range(0, total_rows):
    electrified_sumtechs.loc[sumtechs[row]] = 0
    unelectrified_sumtechs.loc[sumtechs[row]] = 0

i = 0

# Adding pop summary (Million ppl
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_POP + "{}".format(year)])/1000000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_POP + "{}".format(year)])/1000000
    i += 1

# Adding connections summary (Million ppl)
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_NEW_CONNECTIONS + "{}".format(year)])/1000000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_NEW_CONNECTIONS + "{}".format(year)])/1000000
    i += 1

# Adding capacity summaries (MW)
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_NEW_CAPACITY + "{}".format(year)])/1000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_NEW_CAPACITY + "{}".format(year)])/1000
    i += 1

# Adding investment summaries (Million USD)
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_INVESTMENT_COST + "{}".format(year)])/1000000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_INVESTMENT_COST + "{}".format(year)])/1000000
    i += 1

# Adding demand summaries (GWh)
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_TOTAL_ENERGY_PER_CELL + "{}".format(year)])/1000000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_TOTAL_ENERGY_PER_CELL + "{}".format(year)])/1000000
    i += 1

print('hi')