"""
Run the example data.
"""
import pandas as pd

from utils.log import log, write_to_log, set_attrs_name, print_dataframe_columns
from utils.clean import remove_one_hot_encoding, rename_values

if __name__ == '__main__':
    write_to_log(
        'Example data cleaning',
        heading=True
    )

    write_to_log(
        'Import raw data.',
        step_heading=True
    )
    dir_in = './input/'
    file_in = 'example_data.csv'
    name_raw_data = 'raw data'
    df_raw = log(
        pd.read_csv,
        [f'{dir_in}{file_in}']
    )
    # Rename this DataFrame for the log:
    df_raw = log(
        set_attrs_name,
        [df_raw, name_raw_data]
        )

    write_to_log(
        'Set up cleaned output DataFrame.',
        step_heading=True
    )
    df_clean = pd.DataFrame()

    # Rename this DataFrame for the log:
    name_cleaned_data = 'cleaned data'
    df_clean = log(
        set_attrs_name,
        [df_clean, name_cleaned_data]
        )

    df_clean['patient_id'] = df_raw['patient_id']
    df_clean['treated'] = df_raw['treated']

    write_to_log(
        'Process',
        heading=True
    )
    write_to_log(
        'Age: combine multiple columns.',
        step_heading=True
        )
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
    clean_series_age = log(
        set_attrs_name,
        [clean_series_age, 'age_combined_columns']
        )

    write_to_log(
        'Age: change bands to average values.',
        step_heading=True
        )
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
    # Write the contents of the cleaned dataframe:
    write_to_log(
        'Update cleaned dataframe.',
        step_heading=True
        )
    print_dataframe_columns(df_clean)

    write_to_log(
        'Sex: change M/F to 1/0.',
        step_heading=True
        )
    df_clean['sex'] = log(
        rename_values,
        [df_raw['S1Gender'], {'M': 1, 'F': 0}]
        )
    # Write the contents of the cleaned dataframe:
    write_to_log(
        'Update cleaned dataframe.',
        step_heading=True
        )
    print_dataframe_columns(df_clean)

    write_to_log(
        'Arrival times: change bands to start values.',
        step_heading=True
        )
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
    # Write the contents of the cleaned dataframe:
    write_to_log(
        'Update cleaned dataframe.',
        step_heading=True
        )
    print_dataframe_columns(df_clean)

    write_to_log(
        'Result',
        heading=True
    )
    # Write the contents of the dataframe:
    write_to_log('Contents of cleaned dataframe.',
        step_heading=True)
    print_dataframe_columns(df_clean)
    # Save output to file.
    dir_out = './output/'
    file_out = 'data_cleaned.csv'
    df_clean.to_csv(f'{dir_out}{file_out}', index=False)
    write_to_log(
        'Save cleaned dataframe to file.',
        step_heading=True
        )
    write_to_log(f'  {dir_out}{file_out}')

