# Defines the modules

from onsset import *
import pandas as pd
from openpyxl import load_workbook

def calibration(specs_path, csv_path, specs_path_calib, calibrated_csv_path):


    specs = pd.read_excel(specs_path, index_col=0)
    SpecsData = pd.read_excel(specs_path, sheet_name='SpecsData')
    settlements_in_csv = csv_path
    settlements_out_csv = calibrated_csv_path

    onsseter = SettlementProcessor(settlements_in_csv)

    num_people_per_hh_rural = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
    num_people_per_hh_urban = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])

    # RUN_PARAM: these are the annual household electricity targets
    tier_1 = 38.7  # 38.7 refers to kWh/household/year. It is the mean value between Tier 1 and Tier 2
    tier_2 = 219
    tier_3 = 803
    tier_4 = 2117
    tier_5 = 2993

    onsseter.prepare_wtf_tier_columns(num_people_per_hh_rural, num_people_per_hh_urban,
                                      tier_1, tier_2, tier_3, tier_4, tier_5)
    onsseter.condition_df()
    onsseter.grid_penalties()
    onsseter.calc_wind_cfs()

    pop_actual = SpecsData.loc[0, SPE_POP]
    pop_future_high = SpecsData.loc[0, SPE_POP_FUTURE + 'High']
    pop_future_low = SpecsData.loc[0, SPE_POP_FUTURE + 'Low']
    urban_current = SpecsData.loc[0, SPE_URBAN]
    urban_future = SpecsData.loc[0, SPE_URBAN_FUTURE]
    start_year = int(SpecsData.loc[0, SPE_START_YEAR])
    end_year = int(SpecsData.loc[0, SPE_END_YEAR])

    intermediate_year = 2025
    elec_actual = SpecsData.loc[0, SPE_ELEC]
    elec_actual_urban = SpecsData.loc[0, SPE_ELEC_URBAN]
    elec_actual_rural = SpecsData.loc[0, SPE_ELEC_RURAL]
    pop_tot = SpecsData.loc[0, SPE_POP]

    urban_modelled = onsseter.calibrate_pop_and_urban(pop_actual, pop_future_high, pop_future_low, urban_current,
                                                      urban_future, start_year, end_year, intermediate_year)

    elec_modelled, rural_elec_ratio, urban_elec_ratio = \
        onsseter.elec_current_and_future(elec_actual, elec_actual_urban, elec_actual_rural, pop_tot, start_year)

    SpecsData.loc[0, SPE_URBAN_MODELLED] = urban_modelled
    SpecsData.loc[0, SPE_ELEC_MODELLED] = elec_modelled
    SpecsData.loc[0, 'rural_elec_ratio_modelled'] = rural_elec_ratio
    SpecsData.loc[0, 'urban_elec_ratio_modelled'] = urban_elec_ratio

    book = load_workbook(specs_path)
    writer = pd.ExcelWriter(specs_path_calib, engine='openpyxl')
    writer.book = book
    # RUN_PARAM: Here the calibrated "specs" data are copied to a new tab called "SpecsDataCalib". This is what will later on be used to feed the model
    SpecsData.to_excel(writer, sheet_name='SpecsDataCalib', index=False)
    writer.save()
    writer.close()

    logging.info('Calibration finished. Results are transferred to the csv file')
    onsseter.df.to_csv(settlements_out_csv, index=False)

def scenario(specs_path, calibrated_csv_path, results_folder, summary_folder):


    ScenarioInfo = pd.read_excel(specs_path, sheet_name='ScenarioInfo')
    Scenarios = ScenarioInfo['Scenario']
    ScenarioParameters = pd.read_excel(specs_path, sheet_name='ScenarioParameters')
    SpecsData = pd.read_excel(specs_path, sheet_name='SpecsDataCalib')
    print(SpecsData.loc[0, SPE_COUNTRY])

    for scenario in Scenarios:
        print('Scenario: ' + str(scenario + 1))
        countryID = SpecsData.iloc[0]['CountryCode']

        popIndex = ScenarioInfo.iloc[scenario]['Population_Growth']
        tierIndex = ScenarioInfo.iloc[scenario]['Target_electricity_consumption_level']
        fiveyearIndex = ScenarioInfo.iloc[scenario]['Electrification_target_5_years']
        gridIndex = ScenarioInfo.iloc[scenario]['Grid_electricity_generation_cost']
        pvIndex = ScenarioInfo.iloc[scenario]['PV_cost_adjust']
        dieselIndex = ScenarioInfo.iloc[scenario]['Diesel_price']
        productiveIndex = ScenarioInfo.iloc[scenario]['Productive_uses_demand']
        prioIndex = ScenarioInfo.iloc[scenario]['Prioritization_algorithm']

        end_year_pop = ScenarioParameters.iloc[popIndex]['PopEndYear']
        rural_tier = ScenarioParameters.iloc[tierIndex]['RuralTargetTier']
        urban_tier = ScenarioParameters.iloc[tierIndex]['UrbanTargetTier']
        grid_price = ScenarioParameters.iloc[gridIndex]['GridGenerationCost']
        diesel_price = ScenarioParameters.iloc[dieselIndex]['DieselPrice']
        productive_demand = ScenarioParameters.iloc[productiveIndex]['ProductiveDemand']
        prioritization = ScenarioParameters.iloc[prioIndex]['PrioritizationAlgorithm']

        auto_intensification_2025 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2025']
        auto_intensification_2030 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2030']
        auto_intensification_2040 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2040']
        auto_intensification_2050 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2050']
        auto_intensification_2060 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2060']
        auto_intensification_2070 = ScenarioParameters.iloc[prioIndex]['AutoIntensificationKM2070']

        annual_new_grid_connections_limit_2025 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2025'] * 1000
        annual_new_grid_connections_limit_2030 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2030'] * 1000
        annual_new_grid_connections_limit_2040 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2040'] * 1000
        annual_new_grid_connections_limit_2050 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2050'] * 1000
        annual_new_grid_connections_limit_2060 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2060'] * 1000
        annual_new_grid_connections_limit_2070 = ScenarioParameters.iloc[fiveyearIndex]['GridConnectionsLimitThousands2070'] * 1000

        annual_grid_cap_gen_limit_2025 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2025'] * 1000
        annual_grid_cap_gen_limit_2030 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2030'] * 1000
        annual_grid_cap_gen_limit_2040 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2040'] * 1000
        annual_grid_cap_gen_limit_2050 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2050'] * 1000
        annual_grid_cap_gen_limit_2060 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2060'] * 1000
        annual_grid_cap_gen_limit_2070 = SpecsData.loc[0, 'NewGridGenerationCapacityAnnualLimitMW2070'] * 1000

        settlements_in_csv = calibrated_csv_path
        settlements_out_csv = os.path.join(results_folder,
                                           '{}-1-{}_{}_{}_{}_{}_{}.csv'.format(countryID, popIndex, tierIndex,
                                                                                     fiveyearIndex, gridIndex, pvIndex,
                                                                                     prioIndex))
        summary_csv = os.path.join(summary_folder,
                                   '{}-1-{}_{}_{}_{}_{}_{}_summary.csv'.format(countryID, popIndex, tierIndex,
                                                                                     fiveyearIndex, gridIndex, pvIndex,
                                                                                     prioIndex))

        onsseter = SettlementProcessor(settlements_in_csv)

        start_year = SpecsData.iloc[0][SPE_START_YEAR]
        end_year = SpecsData.iloc[0][SPE_END_YEAR]

        existing_grid_cost_ratio = SpecsData.iloc[0][SPE_EXISTING_GRID_COST_RATIO]
        num_people_per_hh_rural = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_RURAL])
        num_people_per_hh_urban = float(SpecsData.iloc[0][SPE_NUM_PEOPLE_PER_HH_URBAN])
        max_grid_extension_dist = float(SpecsData.iloc[0][SPE_MAX_GRID_EXTENSION_DIST])
        urban_elec_ratio = float(SpecsData.iloc[0]['rural_elec_ratio_modelled'])
        rural_elec_ratio = float(SpecsData.iloc[0]['urban_elec_ratio_modelled'])

        # annual_new_grid_connections_limit = SpecsData.loc[0, 'NewGridConnectionsAnnualLimitThousands']*1000
        pv_no = 1
        diesel_no = 1

        # RUN_PARAM: Fill in general and technology specific parameters (e.g. discount rate, losses etc.)
        Technology.set_default_values(base_year=start_year,
                                      start_year=start_year,
                                      end_year=end_year,
                                      discount_rate=0.10)

        grid_calc = Technology(om_of_td_lines=0.02,
                               distribution_losses=0.122,
                               connection_cost_per_hh=125,
                               base_to_peak_load_ratio=0.8,
                               capacity_factor=1,
                               tech_life=30,
                               grid_capacity_investment=float(SpecsData.iloc[0][SPE_GRID_CAPACITY_INVESTMENT]),
                               grid_penalty_ratio=1,
                               grid_price=grid_price)

        mg_hydro_calc = Technology(om_of_td_lines=0.02,
                                   distribution_losses=0.05,
                                   connection_cost_per_hh=100,
                                   base_to_peak_load_ratio=0.85,
                                   capacity_factor=0.5,
                                   tech_life=30,
                                   capital_cost=3000,
                                   om_costs=0.03)

        mg_wind_calc = Technology(om_of_td_lines=0.02,
                                  distribution_losses=0.05,
                                  connection_cost_per_hh=100,
                                  base_to_peak_load_ratio=0.85,
                                  capital_cost=3750,
                                  om_costs=0.02,
                                  tech_life=20)

        mg_pv_calc = Technology(om_of_td_lines=0.02,
                                distribution_losses=0.05,
                                connection_cost_per_hh=100,
                                base_to_peak_load_ratio=0.85,
                                tech_life=20,
                                om_costs=0.015,
                                capital_cost=2950)

        sa_pv_calc = Technology(base_to_peak_load_ratio=0.9,
                                tech_life=15,
                                om_costs=0.02,
                                capital_cost={0.020: 9620,
                                              0.050: 8780,
                                              0.100: 6380,
                                              1: 4470,
                                              5: 6950},
                                standalone=True)

        mg_diesel_calc = Technology(om_of_td_lines=0.02,
                                    distribution_losses=0.05,
                                    connection_cost_per_hh=100,
                                    base_to_peak_load_ratio=0.85,
                                    capacity_factor=0.7,
                                    tech_life=15,
                                    om_costs=0.1,
                                    capital_cost=721)

        sa_diesel_calc = Technology(base_to_peak_load_ratio=0.9,
                                    capacity_factor=0.5,
                                    tech_life=10,
                                    om_costs=0.1,
                                    capital_cost=938,
                                    standalone=True)


        sa_diesel_cost = {'diesel_price': diesel_price,
                          'efficiency': 0.28,
                          'diesel_truck_consumption': 14,
                          'diesel_truck_volume': 300}


        mg_diesel_cost = {'diesel_price':diesel_price,
                          'efficiency': 0.33,
                          'diesel_truck_consumption': 33.7,
                          'diesel_truck_volume': 15000}


        # RUN_PARAM: One shall define here the years of analysis (excluding start year) together with access targets per interval and timestep duration
        yearsofanalysis = [2025, 2030, 2040, 2050, 2060, 2070]
        #yearsofanalysis = [2025, 2030, 2070]
        eleclimits = {2025: 1, 2030: 1, 2040: 1, 2050: 1, 2060: 1, 2070: 1}
        #eleclimits = {2025: 1, 2030: 1, 2070: 1}
        time_steps = {2025: 7, 2030: 5, 2040: 10, 2050: 10, 2060: 10, 2070: 10}
        # time_steps = {2025: 7, 2030: 5, 2070: 40}

        elements = ["1.Population", "2.New_Connections", "3.Capacity", "4.Investment"]
        techs = ["Grid", "SA_Diesel", "SA_PV", "MG_Diesel", "MG_PV", "MG_Wind", "MG_Hydro", "MG_Hybrid"]
        time_step_number = {2025: 0, 2030: 1, 2040: 2, 2050: 3, 2060: 4, 2070: 5}

        sumtechs = []

        for element in elements:
            for tech in techs:
                sumtechs.append(element + "_" + tech)

        sumtechs.append('Min_cluster_pop_2030')
        sumtechs.append('Max_cluster_pop_2030')
        sumtechs.append('Min_cluster_area')
        sumtechs.append('Max_cluster_area')
        sumtechs.append('Min_existing_grid_dist')
        sumtechs.append('Max_existing_grid_dist')
        sumtechs.append('Min_road_dist')
        sumtechs.append('Max_road_dist')
        sumtechs.append('Min_investment_capita_cost')
        sumtechs.append('Max_investment_capita_cost')

        total_rows = len(sumtechs)

        df_summary = pd.DataFrame(columns=yearsofanalysis)

        for row in range(0, total_rows):
            df_summary.loc[sumtechs[row]] = "Nan"

        onsseter.current_mv_line_dist()

        for year in yearsofanalysis:
            eleclimit = eleclimits[year]
            time_step = time_steps[year]
            time_step_no = time_step_number[year]

            end_year = year # 2070
            start_year = year - time_step

            #grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit
            #grid_connect_limit = time_step * annual_new_grid_connections_limit
            if year == 2025:
                auto_intensification = auto_intensification_2025
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2025
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2025
            elif year == 2030:
                auto_intensification = auto_intensification_2030
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2030
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2030
            elif year == 2040:
                auto_intensification = auto_intensification_2040
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2040
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2040
            elif year == 2050:
                auto_intensification = auto_intensification_2050
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2050
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2050
            elif year == 2060:
                auto_intensification = auto_intensification_2060
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2060
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2060
            elif year == 2070:
                auto_intensification = auto_intensification_2070
                grid_connect_limit = time_step * annual_new_grid_connections_limit_2070
                grid_cap_gen_limit = time_step * annual_grid_cap_gen_limit_2070

            onsseter.set_scenario_variables(year, num_people_per_hh_rural, num_people_per_hh_urban, time_step,
                                            start_year, urban_tier, rural_tier,
                                            end_year_pop, productive_demand)

            onsseter.diesel_cost_columns(sa_diesel_cost, mg_diesel_cost, year)

            onsseter.calculate_off_grid_lcoes(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
                                              sa_diesel_calc, year, start_year, end_year, time_step)

            onsseter.pre_electrification(grid_price, year, time_step, start_year)

            onsseter.df[SET_LCOE_GRID + "{}".format(year)], onsseter.df[SET_MIN_GRID_DIST + "{}".format(year)], onsseter.df[
                SET_ELEC_ORDER + "{}".format(year)], onsseter.df[SET_MV_CONNECT_DIST] = onsseter.elec_extension(grid_calc,
                                                                                                        max_grid_extension_dist,
                                                                                                        year,
                                                                                                        start_year,
                                                                                                        end_year,
                                                                                                        time_step,
                                                                                                        grid_cap_gen_limit,
                                                                                                        grid_connect_limit,
                                                                                                        auto_intensification=auto_intensification,
                                                                                                        prioritization=prioritization)

            # onsseter.elec_extension(grid_calc, max_grid_extension_dist, year, start_year, end_year, time_step,
            #                   grid_cap_gen_limit, grid_connect_limit, auto_intensification, prioritization)

            onsseter.results_columns(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
                                     sa_diesel_calc, grid_calc, year)

            onsseter.calculate_investments(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
                                           sa_diesel_calc, grid_calc, year, end_year, time_step)

            onsseter.apply_limitations(eleclimit, year, time_step, prioritization, auto_intensification)

            onsseter.final_decision(year)

            onsseter.calculate_new_capacity(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
                                            sa_diesel_calc, grid_calc, year, time_step)

            onsseter.pv_system_type(year, sa_pv_calc)

            onsseter.time_step_remaining_cap(mg_hydro_calc, mg_wind_calc, mg_pv_calc, sa_pv_calc, mg_diesel_calc,
                                    sa_diesel_calc, grid_calc, year, start_year, time_step_no)

            onsseter.calc_summaries(df_summary, sumtechs, year)

        onsseter.df['FinalElecCode' + str(year)] = onsseter.df['FinalElecCode' + str(year)].astype(int)

        for i in range(len(onsseter.df.columns)):
            if onsseter.df.iloc[:, i].dtype == 'float64':
                onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='float')
            elif onsseter.df.iloc[:, i].dtype == 'int64':
                onsseter.df.iloc[:, i] = pd.to_numeric(onsseter.df.iloc[:, i], downcast='signed')

        df_summary.to_csv(summary_csv, index=sumtechs)
        onsseter.df.to_csv(settlements_out_csv, index=False)
