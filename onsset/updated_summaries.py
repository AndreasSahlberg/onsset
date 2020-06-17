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
SET_TRANSMISSION_INV = 'TransmissionInvestmentCost'
SET_GHI = 'GHI'
SET_WINDCF = 'WindCF'

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

messagebox.showinfo('OnSSET', 'Open the csv file with results data')
result_csv_path = filedialog.askopenfilename()

messagebox.showinfo('OnSSET', 'Browse to SUMMARIES folder and name the scenario to save outputs')
summary_folder = filedialog.askdirectory()

df_in = pd.read_csv(result_csv_path)
df_in['PVType2018'] = 1
df_in['NewConnections2018'] = 0
df_in['NewCapacity2018'] = 0
df_in['InvestmentCost2018'] = 0
df_in['TransmissionInvestmentCost2018'] = 0
df_in['TotalEnergyPerCell2018'] = df_in['ElecPopCalib'] * df_in['ResidentialDemandTierCustom2018'] * df_in[SET_ELEC_CURRENT]

elements = ["1.Population", "2.New_Connections", "3.Capacity", "4.Investment", "5. Demand", "6. Transmission summaries", "7. Distribution summaries", "8. Capacity factor"]
techs = ["Grid", "MG_Diesel", "MG_PV", "MG_Wind", "MG_Hydro", "SA_PV_1", "SA_PV_2", "SA_PV_3", "SA_PV_4", "SA_PV_5"]
years = [2018, 2025, 2030, 2040, 2050, 2060, 2070]
tech_codes = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]

grid_power_plants_capital_cost = {2025: 663,
                                  2030: 373,
                                  2040: 3067,
                                  2050: 982,
                                  2060: 1583,
                                  2070: 1352}

mg_diesel_capital_cost = {2025: 721,
                          2030: 721,
                          2040: 721,
                          2050: 721,
                          2060: 721,
                          2070: 721}

mg_pv_capital_cost = {2025: 2829,
                      2030: 2540,
                      2040: 2252,
                      2050: 1977,
                      2060: 1703,
                      2070: 1428}

mg_wind_capital_cost = {2025: 4356,
                        2030: 4285,
                        2040: 4213,
                        2050: 4117,
                        2060: 4021,
                        2070: 3926}

mg_hydro_capital_cost = {2025: 3000,
                         2030: 3000,
                         2040: 3000,
                         2050: 3000,
                         2060: 3000,
                         2070: 3000}

sa_pv_capital_cost_1 = {2025: 9067,
                        2030: 8143,
                        2040: 7218,
                        2050: 6338,
                        2060: 5458,
                        2070: 4577}
### Stand-alone PV capital cost (USD/kW) for household systems between 21-50 W
sa_pv_capital_cost_2 = {2025: 8487,
                        2030: 7621,
                        2040: 6756,
                        2050: 5932,
                        2060: 5108,
                        2070: 4285}
### Stand-alone PV capital cost (USD/kW) for household systems between 51-100 W
sa_pv_capital_cost_3 = {2025: 6165,
                        2030: 5537,
                        2040: 4908,
                        2050: 4310,
                        2060: 3711,
                        2070: 3113}
### Stand-alone PV capital cost (USD/kW) for household systems between 101-1000 W
sa_pv_capital_cost_4 = {2025: 4316,
                        2030: 3876,
                        2040: 3436,
                        2050: 3017,
                        2060: 2598,
                        2070: 2179}
### Stand-alone PV capital cost (USD/kW) for household systems over 1 kW
sa_pv_capital_cost_5 = {2025: 6710,
                        2030: 6026,
                        2040: 5342,
                        2050: 4690,
                        2060: 4039,
                        2070: 3387}

tech_costs = {1: grid_power_plants_capital_cost, 4: mg_diesel_capital_cost, 5: mg_pv_capital_cost, 6: mg_wind_capital_cost, 7: mg_hydro_capital_cost,
              8: sa_pv_capital_cost_1, 9: sa_pv_capital_cost_2, 10: sa_pv_capital_cost_3, 11: sa_pv_capital_cost_4, 12: sa_pv_capital_cost_5}

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
combined_sumtechs = pd.DataFrame(columns=years)

for row in range(0, total_rows):
    electrified_sumtechs.loc[sumtechs[row]] = 0
    unelectrified_sumtechs.loc[sumtechs[row]] = 0
    combined_sumtechs.loc[sumtechs[row]] = 0

i = 0

# Adding pop summary (Million ppl
for code in tech_codes:
    for year in years:
        electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_POP + "{}".format(year)])/1000000
        unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_POP + "{}".format(year)])/1000000
        combined_sumtechs[year][sumtechs[i]] = sum(df_in.loc[df_in[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_POP + "{}".format(year)]) / 1000000
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

# Adding transmission summaries (Million USD)
for code in tech_codes:
    for year in years:
        if code == 1:
            electrified_sumtechs[year][sumtechs[i]] = sum(df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code, SET_TRANSMISSION_INV + "{}".format(year)]) / 1000000
            unelectrified_sumtechs[year][sumtechs[i]] = sum(df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code, SET_TRANSMISSION_INV + "{}".format(year)])/1000000
    i += 1

# Adding distribution summaries (USD/kW)
for code in tech_codes:
    for year in years:
        if electrified_sumtechs[year][sumtechs[i-40]] > 0:
            electrified_sumtechs[year][sumtechs[i]] = (electrified_sumtechs[year][sumtechs[i-30]]*1000000 -
                                                       electrified_sumtechs[year][sumtechs[i-10]]*1000000 -
                                                       electrified_sumtechs[year][sumtechs[i-40]]*1000 * tech_costs[code][year])/(electrified_sumtechs[year][sumtechs[i-40]]*1000)
        if unelectrified_sumtechs[year][sumtechs[i-40]] > 0:
            unelectrified_sumtechs[year][sumtechs[i]] = (unelectrified_sumtechs[year][sumtechs[i-30]]*1000000 -
                                                       unelectrified_sumtechs[year][sumtechs[i-10]]*1000000 -
                                                       unelectrified_sumtechs[year][sumtechs[i-40]]*1000 * tech_costs[code][year])/(unelectrified_sumtechs[year][sumtechs[i-40]]*1000)
    i += 1

for code in tech_codes:
    for year in years:
        if code == 5 or code > 7:
            if electrified_sumtechs[year][sumtechs[i-40]] > 0:
                electrified_sumtechs[year][sumtechs[i]] = df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_GHI].mean()/8760
            if unelectrified_sumtechs[year][sumtechs[i - 40]] > 0:
                unelectrified_sumtechs[year][sumtechs[i]] = df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_GHI].mean() / 8760
        elif code == 6:
            if electrified_sumtechs[year][sumtechs[i - 40]] > 0:
                electrified_sumtechs[year][sumtechs[i]] = df_electrified.loc[df_electrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_WINDCF].mean()
            if unelectrified_sumtechs[year][sumtechs[i - 40]] > 0:
                unelectrified_sumtechs[year][sumtechs[i]] = df_unelectrified.loc[df_unelectrified[SET_ELEC_FINAL_CODE + "{}".format(year)] == code][SET_WINDCF].mean()
    i += 1

all_sumtechs = electrified_sumtechs + unelectrified_sumtechs

unelectrified_path = os.path.join(summary_folder, 'Unelectrified_Summary.csv')
electrified_path = os.path.join(summary_folder, 'Electrified_summary.csv')
combined_path = os.path.join(summary_folder, 'Combined_summary.csv')

unelectrified_sumtechs.to_csv(unelectrified_path, index=sumtechs)
electrified_sumtechs.to_csv(electrified_path, index=sumtechs)
all_sumtechs.to_csv(combined_path, index=sumtechs)