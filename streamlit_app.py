from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import datetime as dt
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
   

class Load():
    def __init__(self):
        self.Load_filepath = 'C:/Users/2456/Desktop/desktop/Myanmar/Load_profile/Script/'
        self.Appliance_inputs = pd.read_csv(self.Load_filepath+ 'Appliance_ownership.csv',index_col=0)
        #self.Appliance_ToU_filepath = self.Appliance_filepath + '/Time of Use/'
        self.light_n_on  = 2
        self.light_on_duration_mean = [1,4]
        self.light_on_duration_std = [0.25,0.25]
        self.light_time_on_mean = [5,18]
        self.light_time_on_std = [0.25,0.25]
        self.TV_n_on  = 1
        self.TV_on_duration_mean = [2]
        self.TV_time_on_mean = [17]
        self.TV_on_duration_std = [0.5]
        self.TV_time_on_std = [0.25]
        self.Speaker_n_on  = 1
        self.Speaker_on_duration_mean = [2]
        self.Speaker_time_on_mean = [17]
        self.Speaker_on_duration_std = [0.25]
        self.Speaker_time_on_std = [0.25]
        self.Iron_n_on  = 1
        self.Iron_on_duration_mean = [1]
        self.Iron_time_on_mean = [16]
        self.Iron_on_duration_std = [0.25]
        self.Iron_time_on_std = [0.25]
        self.Cooker_n_on  = 2
        self.Cooker_on_duration_mean = [1.5]
        self.Cooker_time_on_mean = [6,18]
        self.Cooker_on_duration_std = [0.25,0.25]
        self.Cooker_time_on_std = [0.25,0.25]
        
        self.dates = 0

#------------------------------------------
 ### Time handler
#------------------------------------------       
        
    def Fifteen_mins_profile_to_hourly_sum(self, fif_profile):
        """
        Function:
            Converts an Fifteen mins profile to a sum for each hour
        Inputs:
            hourly_profile      Fifteen min profile
        Outputs:
            Hourly profile of sum of hourly values
        """
        return fif_profile.resample('H').sum()
    
    def Hourly_to_daily_mean(self, Fifteen_mins_profile_to_hourly_sum):
        """
        Function:
            Converts an Hourly profile to a daily for each hourly mean consumption
        Inputs:
            hourly_profile      
        Outputs:
            Daily profile of mean consumption at each hour
        """
        return Fifteen_mins_profile_to_hourly_sum.resample('D').mean()
 
 #--------------------------------------------------------------------
   ###### Load profile
 #--------------------------------------------------------------------
 
    
 
    def load_yearly(self):
        
        """
        Function:
            Creates a Dataframe of load profile of a year for entire community (all households)
        Inputs:
            Appliance ownership, total number of households, time of use window      
        Outputs:
            Load profile of all households combined for entire year
        """
                
        df_appliances_per_HH = self.Appliance_inputs
        self.dates = pd.date_range('1/1/2021', periods= 37050, freq="15min")
        df_time_series = pd.DataFrame(index=self.dates)
        for HH in df_appliances_per_HH.index:    
             appliances = df_appliances_per_HH.loc[HH]
             list1 = self.label('HH%s'%HH,appliances = appliances)   
             #print(list1)
             if list1:
                 df_temp =  pd.DataFrame(np.zeros((37050,int(len(list1)))),index=self.dates, columns=list1)
                 df_time_series = df_time_series.join(df_temp)
        return df_time_series
       
        
    def label(self,prefix,appliances):
        app_names = []
        apptotal = 0
        for app,num in appliances.items():
            app_names.extend([app+str(i+1) for i in range(num)])
            apptotal += num
            full_list = ["%s%s%s" % (prefix,'_',app_names[j])  for j in range(apptotal)]
            #print(full_list)
        return full_list

    def Load_profile_time_series(self,df_time_series):
        for day in range(365):
            dates = self.dates
            #df_time_series = pd.DataFrame(index=dates)
            day_time_start = dates[0]+dt.timedelta(days=day)
            for column in df_time_series.columns:
                if 'Lights' in column:
                    for nj in range(self.light_n_on):
                        switch_on_time = np.random.normal(self.light_time_on_mean[nj], self.light_time_on_std[nj])
                        on_duration = np.random.normal(self.light_on_duration_mean[nj], self.light_on_duration_std[nj])
                        start_time = day_time_start + dt.timedelta(hours=switch_on_time)
                        end_time = start_time + dt.timedelta(hours=on_duration)
                        df_time_series[column].loc[start_time:end_time] = 5/4  
                elif 'TV' in column:
                    for nj in range(self.TV_n_on):
                        switch_on_time = np.random.normal(self.TV_time_on_mean[nj], self.TV_time_on_std[nj])
                        on_duration = np.random.normal(self.TV_on_duration_mean[nj], self.TV_on_duration_std[nj])
                        start_time = day_time_start + dt.timedelta(hours=switch_on_time)
                        end_time = start_time + dt.timedelta(hours=on_duration)
                        df_time_series[column].loc[start_time:end_time] = 20/4
                elif 'Iron' in column:
                    for nj in range(self.Iron_n_on):
                        switch_on_time = np.random.normal(self.Iron_time_on_mean[nj], self.Iron_time_on_std[nj])
                        on_duration = np.random.normal(self.Iron_on_duration_mean[nj], self.Iron_on_duration_std[nj])
                        start_time = day_time_start + dt.timedelta(hours=switch_on_time)
                        end_time = start_time + dt.timedelta(hours=on_duration)
                        df_time_series[column].loc[start_time:end_time] = 20/4
                elif 'Speaker' in column:
                    for nj in range(self.Speaker_n_on):
                        switch_on_time = np.random.normal(self.Speaker_time_on_mean[nj], self.Speaker_time_on_std[nj])
                        on_duration = np.random.normal(self.Speaker_on_duration_mean[nj], self.Speaker_on_duration_std[nj])
                        start_time = day_time_start + dt.timedelta(hours=switch_on_time)
                        end_time = start_time + dt.timedelta(hours=on_duration)
                        df_time_series[column].loc[start_time:end_time] = 10/4
                elif 'Cooker' in column: 
                    for nj in range(self.Cooker_n_on):
                        switch_on_time = np.random.normal(self.light_time_on_mean[nj], self.light_time_on_std[nj])
                        on_duration = np.random.normal(self.light_on_duration_mean[nj], self.light_on_duration_std[nj])
                        start_time = day_time_start + dt.timedelta(hours=switch_on_time)
                        end_time = start_time + dt.timedelta(hours=on_duration)
                        df_time_series[column].loc[start_time:end_time] = 500/4
        return df_time_series

    # def Daily_consumption_per_HH(self,df_time_series): 
    #     for i in range(int(len(self.Appliance_inputs.index))):
    #         df_HH_load = df_time_series.loc[:, df_time_series.columns.str.startswith("HH%s"%i)]
            

#Trying out the functions
my_load = Load()
df = my_load.load_yearly()
df1 = my_load.Load_profile_time_series(df)
print(df1.head())
