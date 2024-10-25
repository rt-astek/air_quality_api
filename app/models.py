import pandas as pd


class AirQualityData:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def get_all_data(self):
        return self.data.to_json(orient='records')

    def get_data_by_id(self, id):
        return self.data.iloc[id].to_dict() if id < len(self.data) else None

    def add_data_entry(self, entry):
        self.data = pd.concat([self.data, pd.DataFrame([entry])], ignore_index=True)

    def update_data_entry(self, id, entry):
        self.data.iloc[id] = entry

    def delete_data_entry(self, id):
        self.data = self.data.drop(index=id)

    def filter_data(self, year=None, lat=None, long=None):
        filtered_data = self.data
        if year:
            filtered_data = filtered_data[filtered_data['year'] == year]
        if lat:
            filtered_data = filtered_data[filtered_data['lat'] == lat]
        if long:
            filtered_data = filtered_data[filtered_data['long'] == long]
        return filtered_data.to_dict(orient='records')

    def get_statistics(self):
        return {
            "count": len(self.data),
            "average_pm25": self.data['GWRPM25'].mean(),
            "min_pm25": self.data['GWRPM25'].min(),
            "max_pm25": self.data['GWRPM25'].max(),
        }
