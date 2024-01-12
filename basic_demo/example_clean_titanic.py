"""
Clean the Titanic data.

Keep a log of the methods used and save it to file.
"""
import pandas as pd
import logging

from utils.log import log_heading, log_step, log_text, \
    log_dataframe_columns, set_attrs_name
import utils.clean as clean


if __name__ == '__main__':
    # #######################
    # ##### USER INPUTS #####
    # #######################

    # Input file directory and name:
    dir_in = './input/'
    file_in = 'titanic.csv'

    # Output file directory and name:
    dir_out = './output/'
    file_out = 'titanic_cleaned.csv'

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
            filename='example_clean_titanic.log',
            encoding='utf-8',
            level=logging.DEBUG,
            filemode='w'  # Overwrite the existing file
            )
    else:
        # Don't set up logging.
        # Any function here named "log_"... won't do anything useful.
        pass

    log_heading('Titanic data cleaning')
    log_step('Import raw data.')
    df_raw = clean.load_data(f'{dir_in}{file_in}')
    # Rename this DataFrame for the log:
    df_raw = set_attrs_name(df_raw, 'raw data')

    log_step('Check for missing data.')
    series_missing_raw = clean.check_for_missing_data(df_raw)

    log_step('Set up cleaned output DataFrame.')
    df_clean = pd.DataFrame()
    # Rename this DataFrame for the log:
    df_clean = set_attrs_name(df_clean, 'cleaned data')

    log_step('Update cleaned dataframe.')
    columns_to_keep = [
        'PassengerId',
        'Survived',
        'Pclass',
        'Age',
        'SibSp',
        'Parch',
        'Fare'
    ]
    for col in columns_to_keep:
        df_clean[col] = df_raw[col]
    log_dataframe_columns(df_clean)

    log_heading('Process Titanic data')

    log_step('Sex: change male/female to 1/0.')
    clean_series_sex = clean.rename_values(
        df_raw['Sex'], {'male': 1, 'female': 0})

    log_step('Update cleaned dataframe.')
    df_clean['Male'] = clean_series_sex
    log_dataframe_columns(df_clean)

    log_step('Age: impute missing values with median.')
    age, imputed = clean.impute_missing_with_median(df_raw['Age'])

    log_step('Update cleaned dataframe.')
    df_clean['Age'] = age
    df_clean['AgeImputed'] = imputed
    log_dataframe_columns(df_clean)

    log_step('Embarked: impute missing values with label.')
    embarked, imputed = clean.impute_missing_with_missing_label(
        df_raw['Embarked'], label='missing')

    log_step('Embarked: one-hot-encode.')
    clean_df_embarked = clean.apply_one_hot_encoding(
        embarked, prefix='Embarked')

    log_step('Update cleaned dataframe.')
    df_clean = pd.concat([df_clean, clean_df_embarked], axis=1)
    df_clean['EmbarkedImputed'] = imputed
    log_dataframe_columns(df_clean)

    log_step('Cabin: split multiple entries.')
    clean_df_cabin = clean.split_strings_to_columns_by_delimiter(
        df_raw['Cabin'], delimiter=' ')
    log_text('Only keep the first cabin entry.')
    clean_series_cabin = clean_df_cabin[clean_df_cabin.columns[0]]
    print(clean_df_cabin)

    log_step('Cabin: split letters and numbers.')
    clean_df_cabin = clean.split_strings_to_columns_by_index(
        clean_series_cabin, split_index=1)
    clean_df_cabin.columns = ['CabinLetter', 'CabinNumber']

    log_step('Cabin letter: impute missing values.')
    cabin_l, cabin_l_imputed = clean.impute_missing_with_missing_label(
        clean_df_cabin['CabinLetter'], label='missing')

    log_step('Cabin number: impute missing values.')
    cabin_n, cabin_n_imputed = clean.impute_missing_with_missing_label(
        clean_df_cabin['CabinNumber'], label=0)

    log_step('Cabin letter: one-hot-encode.')
    clean_df_cabin_l = clean.apply_one_hot_encoding(
        cabin_l, prefix='CabinLetter')

    log_step('Update cleaned dataframe.')
    df_clean = pd.concat([df_clean, clean_df_cabin_l], axis=1)
    df_clean['CabinLetterImputed'] = cabin_l_imputed
    df_clean['CabinNumber'] = cabin_n
    df_clean['CabinNumberImputed'] = cabin_n_imputed
    log_dataframe_columns(df_clean)

    log_heading('Result')
    log_step('Contents of cleaned dataframe.')
    log_dataframe_columns(df_clean)

    log_step('Save cleaned dataframe to file.')
    df_clean.to_csv(f'{dir_out}{file_out}', index=False)
    log_text(f'{dir_out}{file_out}')
