"""
Run the example data.
"""
import pandas as pd
import logging

from utils.log import log, log_heading, log_step, log_text, set_attrs_name, log_dataframe_columns
from utils.clean import load_data, remove_one_hot_encoding, rename_values

if __name__ == '__main__':

    create_log_file = True
    if create_log_file:
        # Name the logger so that later we can check whether
        # it exists:
        logger = logging.getLogger('pipeline')
        logging.basicConfig(
            filename='example2.log',
            encoding='utf-8',
            level=logging.DEBUG,
            filemode='w'  # Overwrite the existing file
            )
    else:
        # Don't set up logging.
        pass

    log_heading('Example data cleaning')
    log_step('Import raw data.')

    dir_in = './input/'
    file_in = 'example_data.csv'
    name_raw_data = 'raw data'
    df_raw = load_data(f'{dir_in}{file_in}')
    # Rename this DataFrame for the log:
    # df_raw = log(
    #     set_attrs_name,
    #     [df_raw, name_raw_data]
    #     )
    df_raw = set_attrs_name(df_raw, name_raw_data)
    # log(set_attrs_name, [df_raw, name_raw_data])

    log_step('Set up cleaned output DataFrame.')
    df_clean = pd.DataFrame()

    # Rename this DataFrame for the log:
    name_cleaned_data = 'cleaned data'
    # df_clean = log(
    #     set_attrs_name,
    #     [df_clean, name_cleaned_data]
    #     )
    df_clean = set_attrs_name(df_clean, name_cleaned_data)

    df_clean['patient_id'] = df_raw['patient_id']
    df_clean['treated'] = df_raw['treated']

    log_heading('Process')
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
    clean_series_age = log(
        remove_one_hot_encoding,
        [df_raw, columns_age]
        )
    # clean_series_age = log(
    #     set_attrs_name,
    #     [clean_series_age, 'age_combined_columns']
    #     )
    clean_series_age = set_attrs_name(clean_series_age, 'age_combined_columns')

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
    clean_series_age = log(
        rename_values,
        [clean_series_age, dict_map_age]
        )
    df_clean['age'] = clean_series_age
    log_step('Update cleaned dataframe.')
    log_dataframe_columns(df_clean)

    log_step('Sex: change M/F to 1/0.')
    df_clean['sex'] = log(
        rename_values,
        [df_raw['S1Gender'], {'M': 1, 'F': 0}]
        )
    log_step('Update cleaned dataframe.')
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
    df_clean['FirstArrivalTime'] = log(
        rename_values,
        [df_raw['FirstArrivalTime'], dict_map_arrival]
        )
    log_step('Update cleaned dataframe.')
    log_dataframe_columns(df_clean)

    log_heading('Result')
    log_step('Contents of cleaned dataframe.')
    log_dataframe_columns(df_clean)

    # Save output to file.
    dir_out = './output/'
    file_out = 'data_cleaned.csv'
    df_clean.to_csv(f'{dir_out}{file_out}', index=False)
    log_step('Save cleaned dataframe to file.')
    log_text(f'{dir_out}{file_out}')
