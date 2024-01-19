"""
Clean the Titanic data.

Keep a log of the methods used and save it to file.
"""
import pandas as pd
import logging

from utils.log import log_heading, log_step, log_text, \
    log_dataframe_contents, log_dataframe_stats


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
    log_file_name = 'example_clean_titanic_test.log'

    # #########################
    # ##### START OF CODE #####
    # #########################
    if create_log_file:
        # Set up a log file. Name the logger so that later
        # we can check whether it exists.
        logging.getLogger('pipeline')
        logging.basicConfig(
            filename=log_file_name,
            encoding='utf-8',
            level=logging.DEBUG,
            filemode='w'  # Overwrite the existing file
            )
        import utils.clean_log as clean
    else:
        # Don't set up logging.
        # Any function here named "log_"... won't do anything useful.
        import utils.clean as clean

    log_heading(f'{file_in} data cleaning')
    df_raw = clean.load_data(f'{dir_in}{file_in}')

    series_missing_raw = clean.check_for_missing_data(df_raw)

    """ TO DO """
    # TO DO - steps to check which columns are missing data,
    # which columns have which data types,

    # log_step('Check current data types and ranges.')
    # print(df_raw.info(verbose=True, show_counts=True, memory_usage=False))
    # print(df_raw.dtypes)

    # print(df_raw.describe())

    # # Guess whether this column can be simplified by seeing
    # # how many unique values it has.
    # for column in df_raw.columns:
    #     print(df_raw[column].unique())

    # if series_missing_raw.sum() > 0:
    # TO DO - imputation or deleting steps.
    # Best placed after the cleaning?
    # Don't want to impute weird strings or crazy out-of-range values.
    # print('Sort out missing data')
    # print(series_missing_raw)

    log_step('Set up cleaned output DataFrame.')
    df_clean = pd.DataFrame()
    # Rename this DataFrame for the log:
    df_clean = clean.set_attrs_name(df_clean, 'cleaned data')

    columns_to_keep = [
        'PassengerId',
        'Survived',
        'Pclass',
        'SibSp',
        'Parch',
        'Fare'
    ]
    df_clean = clean.add_to_dataframe(df_clean, df_raw[columns_to_keep])

    log_heading('Process data')

    series = clean.rename_values(
        df_raw['Sex'],
        {'male': True, 'female': False}
        )
    df_clean = clean.add_to_dataframe(df_clean, series)

    series, imputed = clean.impute_missing_with_median(df_raw['Age'])
    df_clean = clean.add_to_dataframe(df_clean, series, imputed)

    series, imputed = clean.impute_missing_with_label(
        df_raw['Embarked'],
        label='missing'
        )
    df = clean.apply_one_hot_encoding(series)
    df_clean = clean.add_to_dataframe(df_clean, df, imputed)

    df = clean.split_strings_to_columns_by_delimiter(
        df_raw['Cabin'],
        delimiter=' '
        )
    # Only keep the first column:
    series = df[df.columns[0]]
    df = clean.split_strings_to_columns_by_index(
        series,
        split_index=1
        )
    df.columns = ['CabinLetter', 'CabinNumber']
    # Store copies of these to prevent overwriting them:
    series_cabinletter = df[df.columns[0]]
    series_cabinnumber = df[df.columns[1]]

    series, imputed = clean.impute_missing_with_label(
        series_cabinletter,
        label='missing'
        )
    df = clean.apply_one_hot_encoding(series)
    df_clean = clean.add_to_dataframe(
        df_clean,
        df,
        imputed,
        )

    series, imputed = clean.impute_missing_with_label(
        series_cabinnumber,
        label=0
        )
    df_clean = clean.add_to_dataframe(
        df_clean,
        series,
        imputed
        )

    log_heading('Result')
    df_clean = df_clean.convert_dtypes()
    log_step('Contents of cleaned dataframe.')
    log_dataframe_contents(df_clean)
    log_dataframe_stats(df_clean)  # only runs for numerical columns

    log_step('Save cleaned dataframe to file.')
    df_clean.to_csv(f'{dir_out}{file_out}', index=False)
    log_text(f'{dir_out}{file_out}')
