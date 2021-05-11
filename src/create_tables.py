import pandas as pd

dataset = pd.read_csv('./data/preprocessed-covid.csv')

factor_tb = dataset[['state', 'entry_date', 'id']].copy()
entry_date_dm = dataset['entry_date'].copy().drop_duplicates()
date_symptoms_dm = dataset['date_symptoms'].copy().drop_duplicates()
date_died_dm = dataset['date_died'].copy().drop_duplicates()

patient_dm = dataset[['id', 'sex']]
print(len(patient_dm))
patient_dm = dataset[['id', 'sex']].drop_duplicates()
print(len(patient_dm))
# exit()
preconditions_dm = dataset[
    list(set(dataset.columns.tolist()) - set(['id', 'sex', 'entry_date', 'date_symptoms', 'date_died', 'age']))
].drop_duplicates()


factor_tb['id_preconditions'] = [i for i in range(len(dataset))]
preconditions_dm['id_preconditions']  = factor_tb['id_preconditions'].copy()



factor_tb.to_csv('./tables/factor_tb.csv', index=False)

entry_date_dm.to_csv('./tables/entry_date_dm.csv', index=False)
date_symptoms_dm.to_csv('./tables/date_symptoms_dm.csv', index=False)
date_died_dm.to_csv('./tables/date_died_dm.csv', index=False)

patient_dm.to_csv('./tables/patient_dm.csv', index=False)
preconditions_dm.to_csv('./tables/preconditions_dm.csv', index=False)
