import pandas as pd

def is_na(value)->bool:
    if pd.isna(value):
        return True
    if value==0:
        return True
    if isinstance(value, str) and ((set(value) <= set(".-_/ \n\r")) or value=="#RIF!"):
        return True
    return False