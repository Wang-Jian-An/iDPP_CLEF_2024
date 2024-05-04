import os
import pandas as pd

def load_table_file(
    folder_path: str,
    file_name: str
):
    
    """
    Load table file. 
    """

    if file_name[-4:] == ".csv":
        df = pd.read_csv(
            os.path.join(folder_path, file_name)
        )

    elif file_name[-5:] == ".xlsx":
        df = pd.read_excel(
            os.path.join(folder_path, file_name)
        )
    return df