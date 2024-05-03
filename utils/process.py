from __init__ import *

# variable module
from utils.variable import config

def merge_sensor(
    main_df: pd.DataFrame,
    sensor_df: pd.DataFrame,
    patient_column_name: str,
    main_df_start_date_column: str,
    main_df_end_date_column: str, 
    sensor_df_date_column: str
) -> pd.DataFrame:
    
    """
    <Explanation TBC>
    """

    def merge_sensor_from_one_of_patients(
        df: pd.DataFrame,
        sensor_df: pd.DataFrame,
        df_start_date_column: str,
        df_end_date_column: str,
        sensor_df_date_column: str
    ) -> pd.DataFrame:
        

        queried_sensor_df = [
            sensor_df.query(
                "{} >= {} & {} <= {}".format(
                    sensor_df_date_column,
                    one_df[df_start_date_column],
                    sensor_df_date_column,
                    one_df[df_end_date_column]
                )
            )
            for _, one_df in df.iterrows()
        ]
        queried_sensor_dict = [
            one_df.to_dict("list")
            for one_df in queried_sensor_df
        ]
        df = [
            {
                **one_df.to_dict(),
                **{
                    key: [i for i in value if not(pd.Series(i).isna()[0]) ]
                    for key, value in one_queried_sensor_df.items()
                    if not(key == patient_column_name)
                }
            }
            for (_, one_df), one_queried_sensor_df in zip(
                df.iterrows(),
                queried_sensor_dict
            )
        ]
        return pd.DataFrame(df)

    main_df_each_patient = main_df.groupby(by = patient_column_name)
    sensor_df_each_patient = sensor_df.groupby(by = patient_column_name)

    df = [
        merge_sensor_from_one_of_patients(
            df = one_of_patient_main_df,
            sensor_df = one_of_patient_sensor_df,
            df_start_date_column = main_df_start_date_column,
            df_end_date_column = main_df_end_date_column, 
            sensor_df_date_column = sensor_df_date_column
        )
        for (_, one_of_patient_main_df), (_, one_of_patient_sensor_df) in tqdm.tqdm(
            zip(
                main_df_each_patient, 
                sensor_df_each_patient
            ),
            total = main_df_each_patient.__len__()
        )
    ]
    return pd.concat(df, axis = 0).reset_index(drop = True)

def merge_static(
    main_df: pd.DataFrame,
    static_df: pd.DataFrame,
    patient_column_name: str
) -> pd.DataFrame:
    
    """
    Merge ALSFRS and static data into the one. 
    """

    df = pd.merge(
        left = main_df,
        right = static_df,
        how = "left",
        on = patient_column_name
    )
    return df

def build_train_predict_pairs(
    alsfrs_df: pd.DataFrame,
    patient_id_column_name: str
) -> pd.DataFrame:
    
    """
    
    """

    def build_one_patient_train_predict(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        # 選出互相配對的資料集
        head_data = df.iloc[:-1, :].reset_index(drop = True)
        tail_data = df.iloc[1:, :].reset_index(drop = True)
        
        # 依照不同資料定位，給予不同欄位名稱
        tail_data = tail_data.rename(
            columns = {
                key: f"predict_{key}"
                for key in tail_data.columns.tolist()
            }
        )

        # 合併資料
        df = pd.concat(
            [head_data, tail_data],
            axis = 1
        )
        return df

    alsfrs_df = alsfrs_df.groupby(patient_id_column_name).apply(
        func = build_one_patient_train_predict
    )
    return alsfrs_df.reset_index(drop = True)

def impute_sensor_data(
    df: pd.DataFrame,
    patient_column_name: str, 
    features_to_be_imputed: Optional[Union[str, List[str]]] = None
):
    
    def impute_sensor_data_for_one_of_the_sensor(
        one_df: pd.DataFrame, 
        features_to_be_imputed: Optional[Union[str, List[str]]] = None, 
        imputed_method: str = "linear"
    ):
        
        if not(features_to_be_imputed):
            features_to_be_imputed = [
                i for i in one_df.columns.tolist() if one_df[i].isna().sum() > 50
            ]

        if not(features_to_be_imputed):
            return one_df
        
        else:
            features_to_be_imputed = [
                config["sensor"]["time_feature"],
                *features_to_be_imputed
            ]
            try:
                one_df[features_to_be_imputed] = one_df[features_to_be_imputed].interpolate(
                    method = imputed_method
                )
                return one_df
            except:
                return one_df

    df = df.groupby(by = patient_column_name).apply(
        func = impute_sensor_data_for_one_of_the_sensor,
        features_to_be_imputed = features_to_be_imputed,
        imputed_method = "cubicspline"
    ).reset_index(drop = True)

    df = impute_sensor_data_for_one_of_the_sensor(
        one_df = df,
        imputed_method = "cubicspline"
    )

    for one_feature in df.columns.tolist():
        if not(one_feature in [config["sensor"]["primary_key"], config["sensor"]["time_feature"]]):
            df[one_feature] = df[one_feature].fillna(df[one_feature].dropna().mean())
    return df

def alsfrs_processing(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    """
    Data preprocessing for alsfrs data, including redundant features removal. 

    Args: 
    - df (pd.DataFrame)
    """

    # drop redundant features
    features_to_be_removed = [
        i for i in config["remove_columns"]["alsfrs"] if i in df.columns.tolist()
    ]
    df = df.drop(columns = features_to_be_removed)

    return df

def sensor_processing(
    df: pd.DataFrame
) -> pd.DataFrame:
    
    """
    Data preprocessing for sensor data, including data imputation. 

    Args: 
    - df (pd.DataFrame)
    """

    def detect_all_missing_value_in_one_patient(
        one_patient_df: pd.DataFrame,
        features: List[str]
    ):
        
        one_patient_dict = one_patient_df[features].to_dict("list")
        one_patient_all_values_missing_or_not = {
            key: any([i for i in value if i is not None])
            for key, value in one_patient_dict
        }
        
        return 

    # Detect the features which is totally missing value. 
    


    # Impute missing value for each patients
    

    return

def static_processing(
    df: pd.DataFrame
) -> pd.DataFrame:
    return 