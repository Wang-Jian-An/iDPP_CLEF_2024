import os
import yaml
from dotenv import load_dotenv
load_dotenv

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

main_path_train_task_1 = os.getenv("main_path_train_task_1")
main_path_train_task_2 = os.getenv("main_path_train_task_2")
main_path_test_task_1 = os.getenv("main_path_test_task_1")
main_path_test_task_2 = os.getenv("main_path_test_task_2")