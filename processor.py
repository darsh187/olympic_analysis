import pandas as pd

def process():
    ath_df = pd.read_csv('athlete_events.csv')
    reg_df = pd.read_csv('noc_regions.csv')
    ath_df = ath_df[ath_df['Season'] == 'Summer']
    df = ath_df.merge(reg_df, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    df = pd.concat([df,pd.get_dummies(df['Medal'])], axis=1)
    return df
