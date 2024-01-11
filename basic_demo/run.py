"""
Clean the example data.

Keep a log of the methods used and save it to file.
"""
import pandas as pd
import logging

from utils.log import log_heading, log_step, log_text, \
    log_dataframe_columns, set_attrs_name
from utils.clean import load_data, remove_one_hot_encoding, rename_values

if __name__ == '__main__':
    # #######################
    # ##### USER INPUTS #####
    # #######################

    # Input file directory and name:
    dir_in = './input/'
    file_in = 'example_data.csv'

    # Output file directory and name:
    dir_out = './output/'
    file_out = 'data_cleaned.csv'

    # Whether to save a log file (True) or not (False):
    create_log_file = True

    # #########################
    # ##### START OF CODE #####
    # #########################
    if create_log_file:
        # Set up a log file. Name the logger so that later
        # we can check whether it exists.
        logging.getLogger('pipeline')
        logging.basicConfig(
            filename='example2.log',
            encoding='utf-8',
            level=logging.DEBUG,
            filemode='w'  # Overwrite the existing file
            )
    else:
        # Don't set up logging.
        # Any function here named "log_"... won't do anything useful.
        pass

    log_heading('Example data cleaning')
    log_step('Import raw data.')
    df_raw = load_data(f'{dir_in}{file_in}')
    # Rename this DataFrame for the log:
    df_raw = set_attrs_name(df_raw, 'raw data')

    log_step('Set up cleaned output DataFrame.')
    df_clean = pd.DataFrame()
    # Rename this DataFrame for the log:
    df_clean = set_attrs_name(df_clean, 'cleaned data')

    log_step('Update cleaned dataframe.')
    df_clean['patient_id'] = df_raw['patient_id']
    df_clean['treated'] = df_raw['treated']
    log_dataframe_columns(df_clean)

    log_heading('Process the data')
    log_step('Age: combine multiple columns.')
    columns_age = [
        'AgeUnder40',
        'Age40to44',
        'Age45to49',
        'Age50to54',
        'Age55to59',
        'Age60to64',
        'Age65to69',
        'Age70to74',
        'Age75to79',
        'Age80to84',
        'Age85to89',
        'AgeOver90'
        ]
    clean_series_age = remove_one_hot_encoding(df_raw, columns_age)
    # Rename this Series for the log:
    clean_series_age = set_attrs_name(clean_series_age,
                                      'age_combined_columns')

    log_step('Age: change bands to average values.')
    dict_map_age = {
        'AgeUnder40': 37.5,
        'Age40to44': 42.5,
        'Age45to49': 47.5,
        'Age50to54': 52.5,
        'Age55to59': 57.5,
        'Age60to64': 62.5,
        'Age65to69': 67.5,
        'Age70to74': 72.5,
        'Age75to79': 77.5,
        'Age80to84': 82.5,
        'Age85to89': 87.5,
        'AgeOver90': 92.5
        }
    clean_series_age = rename_values(clean_series_age, dict_map_age)

    log_step('Update cleaned dataframe.')
    df_clean['age'] = clean_series_age
    log_dataframe_columns(df_clean)

    log_step('Sex: change M/F to 1/0.')
    clean_series_sex = rename_values(df_raw['S1Gender'], {'M': 1, 'F': 0})

    log_step('Update cleaned dataframe.')
    df_clean['sex'] = clean_series_sex
    log_dataframe_columns(df_clean)

    log_step('Arrival times: change bands to start values.')
    dict_map_arrival = {
        '0000to3000': 0,
        '0300to0600': 3,
        '0600to0900': 6,
        '0900to1200': 9,
        '1200to1500': 12,
        '1500to1800': 15,
        '1800to2100': 18,
        '2100to2400': 21
        }
    clean_series_firstarrivaltime = rename_values(
        df_raw['FirstArrivalTime'], dict_map_arrival)

    log_step('Update cleaned dataframe.')
    df_clean['FirstArrivalTime'] = clean_series_firstarrivaltime
    log_dataframe_columns(df_clean)

    log_heading('Result')
    log_step('Contents of cleaned dataframe.')
    log_dataframe_columns(df_clean)

    log_step('Save cleaned dataframe to file.')
    df_clean.to_csv(f'{dir_out}{file_out}', index=False)
    log_text(f'{dir_out}{file_out}')
