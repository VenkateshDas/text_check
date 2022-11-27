'''
This is a script to update the rule database. The rule database is currently present in Google sheets.
The script will compare the rule database in google sheets with the rule database in the local file system.
If there is a difference, the script will update the local rule database with the google sheets rule database.
After making the necessary changes to rules.csv and examples.csv, the script will output in the console to set the GITHUB_OUTPUT environment variable.
This will run the github action to update the rule database in the github repository and create a pull request.
'''

# TODO: Connect to google sheets and download the latest rule database
# TODO: Compare the local rule database with the google sheets rule database. If there are changes then update the local rule database (rules.csv and examples.csv).
 
import pandas as pd

# compare the old_rules_file and new_rules_file. If there are changes then update the old rules file with the new rules file.
def compare_rules(old_rules_file, new_rules_file):
    old_rules = pd.read_csv(old_rules_file)
    new_rules = pd.read_csv(new_rules_file)
    if old_rules.equals(new_rules):
        print("No changes in rules.csv")
    else:
        print("Updating rules.csv")
        old_rules.to_csv(old_rules_file, index=False)

# compare the old_examples_file and new_examples_file. If there are changes then update the old examples file with the new examples file.
def compare_examples(old_examples_file, new_examples_file):
    old_examples = pd.read_csv(old_examples_file)
    new_examples = pd.read_csv(new_examples_file)
    if old_examples.equals(new_examples):
        print("No changes in examples.csv")
    else:
        print("Updating examples.csv")
        old_examples.to_csv(old_examples_file, index=False)

# main function
def main():
    old_rules_file = "/Users/venkateshmurugadas/text_check/text_check/configs/rules.csv"
    new_rules_file = "/Users/venkateshmurugadas/Downloads/new_rules.csv"
    old_examples_file = "examples.csv"
    new_examples_file = "new_examples.csv"
    compare_rules(old_rules_file, new_rules_file)
    # compare_examples(old_examples_file, new_examples_file)
    # print("Set the GITHUB_OUTPUT environment variable to run the github action to update the rule database in the github repository and create a pull request.")