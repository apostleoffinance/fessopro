import pandas as pd 
time_zone='America/New_York'


data = pd.read_csv('/Users/olaoluwatunmise/fessopro/12_datetime_analysis/data (2).csv')
#drop the first two rows that are not needed
data.drop([0,1], axis=0,inplace=True)

#Rename column
data.rename(columns={'Price':'Date'}, inplace=True)

#convert date column from object to datetime
data['Date']=pd.to_datetime(data['Date'])

#convert to timezone
data['Date'] = data['Date'].dt.tz_convert(time_zone)

data['Date'] = data['Date'].dt.tz_localize(None)

print(data)
print(data.info())