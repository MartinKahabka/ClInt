import argparse
import os
import re

# author: Martin Kahabka

# this file should input the output if "runVariantProm.sh" and return a tsv as described on git
# necessary files
# 1. from output files of "runVariantProm.sh" get
#   1.1 chr/pos of variants
#   1.2 number of patients with variant
#   1.3 ID of patients
# 3. from Q001H_sample_preparations_20230803115337.tsv get
#   3.1 condition (severe/not severe) of patients

# structure
# save ID of each analysed patient
# get condition of each patient with saved ID
# counter number of severe/not severe patients
# counter number of 
# for each output file get
#   ID of patient -> condition of patient
#   for each variant do
#       is variant already saved? -> create new dict entry
#       increase correlating counter
#       save ID to correlation array
# iterate over variants and fill number of patients where variant was not found (see number severe/not severe patients)
# save file in described format (see git)

# gets a string and a regex pattern that describes the unique ID of the patient
def extract_id(name, pattern) -> str:
    id = re.search(pattern, name).group()
    return id


parser = argparse.ArgumentParser(description="Process input directory")
parser.add_argument("-i", "--input_dir", help="Path to the input directory of the filtered vcfs")
parser.add_argument("-p", "--patient_info", help="File with general information of patients")
args = parser.parse_args()

### informationAndData/output_promoter/
# get parameters
input_path = args.input_dir
info_file_path = args.patient_info

# get IDs of patients
print("--- READ IN LAB IDS OF PATIENTS FOR PROMTER VCF FILES ---")
counter_pat = 0
id_and_condition = {}
for file in os.listdir(input_path):
    counter_pat += 1
    pattern = r"FO\d*x\d*"
    patient_ID = extract_id(file, pattern)
    id_and_condition[patient_ID] = ""

print("--- SUCCESSFUL: number of files: " + str(counter_pat))
## 
# read conditions from Q001H_sample_preparations_20230803115337.tsv
# extract lab_ID from patients
print("--- READ IN CONDITIONS OF PATIENTS ---")
counter_severe = 0
counter_not_severe = 0
with open(info_file_path, 'r') as info_file:
    for line in info_file:
        content = line.split("\t")
        # check for header line
        lab_id = content[2]
        condition = content[15]
        # check if lab id correlates to patient
        if lab_id != "Lab ID" and lab_id in id_and_condition:
            id_and_condition[lab_id] = condition
            # check type of condition
            if condition == "COVID severe":
                counter_severe += 1
            else:
                counter_not_severe += 1
print("--- SUCCESFUL: number of severe/not severe patients: " + str(counter_severe) + "/" + str(counter_not_severe))

