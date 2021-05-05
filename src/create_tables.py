import pandas as pd

dataset = pd.read_csv('./data/preprocessed-covid.csv')

factor_tb = dataset[['state', 'entry_date', 'id']].copy()
date_dm = dataset[['entry_date', 'date_symptoms', 'date_died']]
patient_dm = dataset[['id', 'sex']]
preconditions_dm = dataset[
    list(set(dataset.columns.tolist()) - set(['id', 'sex', 'entry_date', 'date_symptoms', 'date_died', 'age']))
]



factor_tb['id_preconditions'] = [i for i in range(len(dataset))]
preconditions_dm['id_preconditions']  = factor_tb['id_preconditions'].copy()



factor_tb.to_csv('./tables/factor_tb.csv', index=False)
date_dm.to_csv('./tables/date_dm.csv', index=False)
patient_dm.to_csv('./tables/patient_dm.csv', index=False)
preconditions_dm.to_csv('./tables/preconditions_dm.csv', index=False)
