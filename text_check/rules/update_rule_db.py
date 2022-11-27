'''
This is a script to update the rule database. The rule database is currently present in Google sheets.
The script will compare the rule database in google sheets with the rule database in the local file system.
If there is a difference, the script will update the local rule database with the google sheets rule database.
After making the necessary changes to rules.csv and examples.csv, the script will output in the console to set the GITHUB_OUTPUT environment variable.
This will run the github action to update the rule database in the github repository and create a pull request.
'''

# TODO: Compare the local rule database with the google sheets rule database. If there are changes then update the local rule database (rules.csv and examples.csv).
 
import pandas as pd
import os


def download_from_google_sheets(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    return df


# Assumption: Every column must have a value. If there is no value, then the column must be empty. They will be be dropped.
def update_df(old_df, new_df, file_name):
    new_df.dropna(inplace=True, axis=1, how='all')
    if old_df.equals(new_df):
        print(f"No changes in the provided file: {file_name}")
        is_updated = False
    else:
        print(f"Updating the file: {file_name}")
        new_df.to_csv(file_name, index=False)
        is_updated = True
    return is_updated


# main function
def main():
    sheet_id = "13Jyq9lvFnMWNbwExruqlfiFsKaFHqm0aGUcUw3_FNgs"
    rules_sheet_name = "rules_v4"
    examples_sheet_name = "rule_examples_v2"
    new_rules_df = download_from_google_sheets(sheet_id, rules_sheet_name)
    new_examples_df = download_from_google_sheets(sheet_id, examples_sheet_name)
    old_rules_df = pd.read_csv("text_check/configs/rules.csv")
    old_examples_df = pd.read_csv("text_check/configs/examples.csv")
    # compare rules df
    is_rules_updated = update_df(old_rules_df, new_rules_df, "text_check/configs/rules.csv")
    # compare examples df
    is_examples_updated = update_df(old_examples_df, new_examples_df, "text_check/configs/examples.csv")

    if is_rules_updated or is_examples_updated:
        files_changed = True
    else:
        files_changed = False
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        print(f'files_changed={files_changed}', file=f)


if __name__ == "__main__":
    main()
    

