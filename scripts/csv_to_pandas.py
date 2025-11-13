import pandas as pd
from pathlib import Path

#pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# ---------------------------------------
# Project Structure
# ---------------------------------------
# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_DIR = PROJECT_ROOT / 'queries'
LOGS_DIR = PROJECT_ROOT / 'logs'
DATA_DIR = PROJECT_ROOT / 'data'
MEDIA_DIR = PROJECT_ROOT / 'media'



def df_from_csv(csv_filepath: str) -> pd.DataFrame:
    df_raw = pd.read_csv(csv_filepath, na_values=['NULL'], encoding='utf-8')
    return df_raw


def df_after_pivot(df_raw: pd.DataFrame) -> pd.DataFrame:
    cols_to_keep = [
    #'vessel_id',
    'vessel',
    'event_id',
    #'event_name',
    'department_name',
    'days_ago',
    #'event_type_id',
    #'event_type_name'
    ]
    df_raw = df_raw[cols_to_keep]
    df = df_raw.pivot_table(
            index=['vessel'],
            columns='department_name',
            values='days_ago',
            aggfunc=lambda x: x[x < 0].max() if not x[x < 0].empty else x.min()
    ).reset_index()
    df.columns.name = None
    df = df.rename(columns={'vessel': 'Vessel'})
    return df


if __name__ == "__main__":
    csv_filepath = DATA_DIR / 'vessel_attendances.csv'
    df_raw = df_from_csv(csv_filepath)
    df = df_after_pivot(df_raw)
    #print(df_raw)
    print(df)

