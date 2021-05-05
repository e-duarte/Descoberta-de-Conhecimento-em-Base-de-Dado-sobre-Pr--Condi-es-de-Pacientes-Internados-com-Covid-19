from numpy.lib.function_base import cov
import pandas as pd

class CovidDataset:
    def __init__(self):
        covid = pd.read_csv('data/covid.csv')

        covid['sex'] = covid['sex'] - 1
        covid['patient_type'] = covid['patient_type'] - 1

        columns = covid.columns.tolist()
        columns = list(set(columns) - set(['id', 'sex', 'patient_type', 'entry_date', 'date_symptoms', 'date_died', 'age']))


        for c in columns:
            covid[c] = list(
                map(
                    lambda x: 'not-specified' if x == 97 or x == 98 or x == 99 else x,
                    covid[c]
                )
            )
        
        self.one_hot(covid, columns)
        

        covid['entry_date'] = pd.to_datetime(covid['entry_date'], format='%d-%m-%Y')
        covid['date_symptoms'] = pd.to_datetime(covid['date_symptoms'], format='%d-%m-%Y')

        duration_entry_symptoms = covid['entry_date'] - covid['date_symptoms']
        covid['duration_entry_symptoms'] = duration_entry_symptoms
    
        covid['duration_hospitalization'] = self.duration_hospitalization(covid)
        covid['died'] = self.died(covid)


        covid.pop('id')
        covid.pop('entry_date')
        covid.pop('date_symptoms')
        covid.pop('date_died')

        for c in columns:
            covid.pop(c)
        print(covid.dtypes)
        self.covid = covid
    
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


    def duration_hospitalization(self, covid):
        duration = list(
            map(
                lambda x, y: -1 if x == '9999-99-99' else str(pd.to_datetime(x, format='%d-%m-%Y') - y),
                covid['date_died'],
                covid['date_symptoms']
            )
        )

        duration = list(
            map(
                lambda x: int(x.split(' ')[0]) if isinstance(x, str) else x,
                duration
            )
        )

        return duration
    
    def died(self, covid):
        died = list(
            map(
                lambda x: 0 if x == '9999-99-99' else 1,
                covid['date_died']
            )
        )

        return died



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

        date_died = list(
                map(
                    lambda x: x if x == '9999-99-99' else f'{x.split("-")[2]}-{x.split("-")[1]}-{x.split("-")[0]}',
                    covid['date_died']
                )
            )
        
        covid['date_died'] = date_died
        print(covid)

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
   
    CovidDataWarehouse().covid.to_csv('data/preocessed-covid.csv', index=False)
