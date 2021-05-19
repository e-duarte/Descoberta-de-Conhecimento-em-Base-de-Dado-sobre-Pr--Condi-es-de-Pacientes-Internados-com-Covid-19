from numpy.lib.function_base import cov
import pandas as pd
import numpy as np

class CovidDataset:
    def __init__(self):
        covid = pd.read_csv('covid.csv')

        covid['sex'] = covid['sex'] - 1

        covid['patient_type'] = covid['patient_type'] - 1

        print('applying one-hot representation')
        columns = covid.columns.tolist()
        columns = list(set(columns) - set(['id', 'sex', 'patient_type', 'entry_date', 'date_symptoms', 'date_died', 'age']))

        for c in columns:
            covid[c] = list(
                map(
                    self.to_map,
                    covid[c]
                )
            )

        
        self.one_hot(covid, columns)

        print('leaving date')
        covid['leaving_date'] = list(
            map(
                lambda l_val, e_val: pd.to_datetime(e_val) + pd.DateOffset(days=15) if l_val == '9999-99-99' else pd.to_datetime(l_val),
                covid['date_died'],
                covid['entry_date']
            
            )
        )
        print('duration of covid')
        covid['duration_covid'] = self.duration_hospitalization(covid)
        covid['duration_covid'] = abs(covid['duration_covid'].astype('int32'))
        print(covid['duration_covid'])


        print('Add var died')
        covid['state_patient'] = list(
            map(
                lambda x: 0 if x == '9999-99-99' else 1,
                covid['date_died']
            )
        )
        
        print('Removing vars')
        covid.pop('id')
        covid.pop('entry_date')
        covid.pop('date_symptoms')
        covid.pop('date_died')
        covid.pop('leaving_date')

        for c in columns:
            covid.pop(c)

        print(covid.dtypes)
        self.covid = covid
    
    def duration_hospitalization(self, covid):
        duration = list(
            map(
                lambda x, y: str(pd.to_datetime(y) - pd.to_datetime(x)),
                covid['leaving_date'],
                covid['entry_date']
            )
        )
        duration = list(
            map(
                lambda x: str(x).split(' ')[0],
                duration
            )
        )

        # print(duration)??
        # exit()

        return duration

    def one_hot(self, covid, column):
        for c in column:
            values = covid[c].drop_duplicates().tolist()
            # print(values)

            for v in values:
                covid[f'{c}-{v}'] = list(
                    map(
                        lambda x: 1 if x == v else 0,
                        covid[c]
                    )
                )
    
    def died(self, covid):
        died = list(
            map(
                lambda x: 0 if x == '9999-99-99' else 1,
                covid['date_died']
            )
        )

        return died

    def to_map(self, x):
        if x == 1:
            return 'yes'
        elif x == 2:
            return 'no'
        else:
            return 'not-specified'


class CovidDataWarehouse:
    def __init__(self):
        covid = pd.read_csv('data/covid.csv')

        covid['sex'] = list(
                map(
                    lambda x: 'female' if x == 1 else 'male',
                    covid['sex']
                )
            )

        covid['patient_type'] = list(
                map(
                    lambda x: 'not-hospitalized' if x == 1 else 'hospitalized',
                    covid['patient_type']
                )
            )

        columns = covid.columns.tolist()
        columns = list(set(columns) - set(['id', 'sex', 'patient_type', 'entry_date', 'date_symptoms', 'date_died', 'age']))
        

        for c in columns:
            covid[c] = list(
                map(
                    self.to_map,
                    covid[c]
                )
            )


        state = list(
                map(
                    lambda x: 'recovered' if x == '9999-99-99' else 'died',
                    covid['date_died']
                )
            )

        
        covid['state'] = state
        
        entry_date = list(
                map(
                    lambda x: x if x == '9999-99-99' else f'{x.split("-")[2]}-{x.split("-")[1]}-{x.split("-")[0]}',
                    covid['entry_date']
                )
            )

        covid['entry_date'] = entry_date

        date_symptoms = list(
                map(
                    lambda x: x if x == '9999-99-99' else f'{x.split("-")[2]}-{x.split("-")[1]}-{x.split("-")[0]}',
                    covid['date_symptoms']
                )
        )
        
        covid['date_symptoms'] = date_symptoms

        leaving = list(
                map(
                    lambda x: x if x == '9999-99-99' else f'{x.split("-")[2]}-{x.split("-")[1]}-{x.split("-")[0]}',
                    covid['date_died']
                )
        )

        covid['leaving_date'] = list(
            map(
                lambda l_val, e_val: str(pd.to_datetime(e_val) + pd.DateOffset(days=15)).split(' ')[0] if l_val == '9999-99-99' else l_val,
                leaving,
                entry_date
            
            )
        )
        # leaving_date = []
        # for l_val, e_val in zip(leaving, entry_date):
        #     if l_val == '9999-99-99':
        #         leaving_date.append(str(pd.to_datetime(e_val) + pd.DateOffset(days=15)))
        #     else:
        #         leaving_date.append(l_val)

        # covid['leaving_date'] = leaving_date
        # # print(covid)

        self.covid = covid

    def to_map(self, x):
        if x == 1:
            return 'yes'
        elif x == 2:
            return 'no'
        else:
            return 'not-specified'

if __name__ == '__main__':
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt


    print('Preprocessing dataset')
    dataset = CovidDataset().covid
    print(dataset)
    dataset.to_csv('covid-dataset-preprocessed.csv', index=False)

