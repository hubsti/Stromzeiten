from entsoe import EntsoePandasClient
import sqlite3
import pandas as pd
from datetime import date, timedelta
import time
import seaborn as sns


end_date = date.today()+timedelta(days=1)
current_date = end_date.strftime("%Y%m%d")

client = EntsoePandasClient(api_key='444fc771-5d0f-499f-9328-90c05c459219')

start = pd.Timestamp('20201125', tz='Europe/Brussels')
end = pd.Timestamp(current_date, tz='Europe/Brussels')
country_code = 'DE'


generation = client.query_generation_forecast(country_code, start=start, end=end)
load = client.query_load_forecast(country_code, start=start, end=end)
renewable = client.query_wind_and_solar_forecast(country_code, start=start, end=end)

renewable['Total'] = renewable['Solar']+renewable['Wind Offshore']+renewable['Wind Onshore']

load1 = pd.DataFrame(load)

renewable['Renewable/Load_ratio'] = renewable['Total']/load1[0]*100

renewable['Quality_ratio'] = renewable['Renewable/Load_ratio']/renewable['Renewable/Load_ratio'].max()*100

print(renewable)
print(renewable['Renewable/Load_ratio'].max())

renewable['Date'] = renewable.index
renewable.insert(0, 'id', range(0 , len(renewable)))

rounded_renewables = renewable['Quality_ratio'].round(decimals=1)
renewable['Quality_ratio'] = rounded_renewables

renewable.rename(columns={"Wind Offshore": "Wind_Offshore",
                                "Wind Onshore": "Wind_Onshore", "Renewable/Load_ratio": "Renewable_Load_ratio"}, inplace=True)

print(renewable.head())

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
renewable.to_sql('Stromzeiten_app_stromzeiten_table', conn, if_exists='replace', index = False)

c.execute('''  
SELECT * FROM Stromzeiten_app_stromzeiten_table
          ''')

for row in c.fetchall():
    print(row)

g = sns.relplot(x="Date", y="Quality_ratio", kind="line", data=renewable)
g.fig.autofmt_xdate()

print(g)

renewable.to_csv('renewable_13.11.csv')
