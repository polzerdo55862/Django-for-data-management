import os
import django
from sqlalchemy import create_engine

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_management.settings')
django.setup()

import data_processing_app.models as models
from data_processing_app.helper_functions import connect_to_toggl, \
    get_all_clients_and_projects, get_all_time_entries, data_processing, \
    define_working_days_table, write_toggl_data_in_database, \
    write_working_days_list
from data_management import settings as config
from django.conf import settings
from datetime import datetime
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import django


import data_processing_app.models as models
from data_management import settings

#new_workspace = toggl_workspaces(wid=1, name='Testworkspace')
#new_workspace.save()

def collect_data_from_toggl():
    email, workspaces, headers = connect_to_toggl(config.toggl_api)

    my_workspace = workspaces[0]['id']
    my_workspace_name = workspaces[0]['name']

    new_workspace = models.toggl_workspaces(wid=my_workspace, name=my_workspace_name)
    new_workspace.save()

    clients, projects = get_all_clients_and_projects(my_workspace, headers)

    time_entries_extended_df = get_all_time_entries(headers, start_date=config.start_date,
                                                    end_date=config.end_date)
    #process the information
    projects_df, clients_df, time_entries_df  = data_processing(clients, projects, time_entries_extended_df)

    #fill NaN fields with "-"
    time_entries_df = time_entries_df.fillna("-")

    return projects_df, clients_df, time_entries_df, my_workspace

projects_df, clients_df, time_entries_df, my_workspace = collect_data_from_toggl()

#drop row where stop isnt defined yet
time_entries_df = time_entries_df[time_entries_df.duration > 0]



def df_directly_to_mysql():
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']

    database_url = 'mysql://{user}:{password}@localhost:3308/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )


    engine = create_engine(database_url, echo=False)
    clients_df.to_sql('data_processing_app_toggl_clients', con=engine, if_exists="replace", index=False)


for index, row in clients_df.iterrows():
    new_client = models.toggl_clients(cid=row.cid, workspace=models.toggl_workspaces.objects.get(wid=my_workspace), name=row.client_name)
    new_client.save()

for index, row in projects_df.iterrows():
    new_project = models.toggl_projects(pid=row.pid, client=models.toggl_clients.objects.get(cid=row.cid), project_name=row.project_name)
    new_project.save()

for index, row in time_entries_df.iterrows():
    new_time_entry = models.time_entries(id=row.id,
                                           project=models.toggl_projects.objects.get(pid=int(row.pid)),
                                           start=row.start,
                                           duration=row.duration)
    new_time_entry.save()

# working_days_df = define_working_days_table(config.start_date, config.end_date)
# working_days_df["week"] = [item.strftime("%Y-%V") for item in working_days_df['days']]
# working_days_sum_by_week_df = working_days_df.groupby(['week'])
# working_days_sum_by_week_df = working_days_sum_by_week_df['working_hours'].agg(np.sum)
# working_days_sum_by_week_df = pd.DataFrame(working_days_sum_by_week_df)
#
# def write_tables_to_mysql(time_entries_extended, working_days_df):
#     '''write the collected and processed data to tables in the MySQL database'''
#
#     try:
#         cnx, cursor = connect_to_database(password=config.mysql["user"], database=config.mysql["database"],
#                                           user=config.mysql["user"], port=config.mysql["port"], host=config.mysql["host"])
#
#         return_messages_time_entries = write_toggl_data_in_database(cursor, cnx, time_entries_extended)
#         for item in return_messages_time_entries:
#             print(item)
#
#         return_messages_working_days = write_working_days_list(cursor, cnx, working_days_df)
#         for item in return_messages_working_days:
#             print(item)
#     finally:
#         cnx.close()
#
# if config.write_to_mysql == True:
#     write_tables_to_mysql(time_entries_extended_df, working_days_df)
#
#
# def sum_worked_hours_by_week(time_entries_extended_df):
#     '''
#     Sums up the hours in the Toogl time entries by the calendar week
#     :return: DataFrame with CW and the sum of the time entries duration in this week
#     '''
#
#     time_entries = copy.deepcopy(time_entries_extended_df)
#
#     time_entries.loc[:, 'week'] = time_entries.start.map(lambda x: datetime.date(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+00:00')).strftime("%Y-%V"))
#     time_entries.loc[:, 'duration_hours'] = time_entries.duration.map(lambda x: x/3600)
#
#     time_entries_sum_per_week_df = time_entries.groupby(['week']).agg("sum")
#
#     return time_entries_sum_per_week_df
#
#
# #calculate worked hours for a certain client
# time_entries_sum_only_DI_df = sum_worked_hours_by_week(
#     time_entries_extended_df[time_entries_extended_df.client_name == "DI"]
# )
#
# worked_hours = time_entries_sum_only_DI_df["duration_hours"].sum()
# target_hours = working_days_sum_by_week_df["working_hours"].sum()
# over_hours =round((worked_hours - target_hours),1)
#
# #plot diagram with matplotlib
# fig, ax = plt.subplots(figsize=(15, 7))
# ax.bar(working_days_sum_by_week_df.index.tolist(), working_days_sum_by_week_df["working_hours"].tolist(), width=0.35, label="Target working hours", color="grey")
#
# for i, client in enumerate(time_entries_extended_df.client_name.unique()):
#     time_entries_sum_per_week_df = sum_worked_hours_by_week(
#         time_entries_extended_df[time_entries_extended_df.client_name == client]
#     )
#
#     bar = ax.plot(time_entries_sum_per_week_df.index.tolist(), time_entries_sum_per_week_df["duration_hours"].tolist(),
#                   "-o", label=client)
#
# ax.set(xlabel='Calendar week', ylabel='Hours',
#        title=f'Working hours (total overhours: {over_hours})')
#
#
#
# ax.legend(title="Clients")
# plt.xticks(rotation=45)
# plt.show()