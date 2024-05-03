import argparse

# Load module
from utils.load import load_table_file

# variable module
from utils.variable import (
    config, 
    main_path_train_task_1,
    main_path_train_task_2,
    main_path_test_task_1,
    main_path_test_task_2
)

# process module
from utils.process import (
    alsfrs_processing,
    sensor_processing,
    static_processing,
    build_train_predict_pairs,
    merge_sensor,
    impute_sensor_data
)

parser = argparse.ArgumentParser()
parser.add_argument("--train-or-predict", type = str, default = "train")
parser.add_argument("--task-id", type = int, default = 1)
args = parser.parse_args()

def main():

    if args.train_or_predict == "train" and args.task_id == 1:
        main_path = main_path_train_task_1

    elif args.train_or_predict == "train" and args.task_id == 2:
        main_path = main_path_train_task_2

    elif args.train_or_predict == "predict" and args.task_id == 1:
        main_path = main_path_test_task_1

    else: 
        main_path = main_path_test_task_2

    # Step1. Load data
    
    alsfrs_df = load_table_file(
        folder_path = main_path,
        file_name = config[args.train_or_predict]["file_name"]["alsfrs"]
    )
    sensor_df = load_table_file(
        folder_path = main_path,
        file_name = config[args.train_or_predict]["file_name"]["sensor"]
    )
    static_df = load_table_file(
        folder_path = main_path,
        file_name = config["predict"]["file_name"]["static"]
    )

    # Step3. Data preprocessing
    alsfrs_df = alsfrs_processing(
        df = alsfrs_df
    )

    # Step4. Impute missing data
    sensor_df = impute_sensor_data(
        df = sensor_df,
        patient_column_name = config["sensor"]["primary_key"]
    )

    # Step2. Build train-predict pairs
    if args.train_or_predict == "train":
        alsfrs_df = build_train_predict_pairs(
            alsfrs_df = alsfrs_df,
            patient_id_column_name = config["alsfrs"]["primary_key"]
        )

    # Step2. Date merge
    alsfrs_sensor_df = merge_sensor(
        main_df = alsfrs_df,
        sensor_df = sensor_df,
        patient_column_name = "patient_id",
        main_df_start_date_column = config["alsfrs"]["time_feature"][f"{args.train_or_predict}_start"],
        main_df_end_date_column = config["alsfrs"]["time_feature"][f"{args.train_or_predict}_end"], 
        sensor_df_date_column = config["sensor"]["time_feature"]
    )
    alsfrs_sensor_df.to_excel("./test.xlsx", index = None)

    # Step5. Feature engineer for sensor data

    
    # Step6. Questionaire combination


    # Step7. Machine learning 


    return

if __name__ == "__main__":
    main()