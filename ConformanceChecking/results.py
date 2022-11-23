from __future__ import division
import json
import xml.etree.ElementTree as ET
import sys
import conformance as cc
import copy
import os
import pandas as pd

def main():
    # Path to data
    train_path = "ConformanceChecking\Data\Train\Train_XES"
    test_path = "ConformanceChecking\Data\Test\Test_XES"

    #Header values for DataFrame
    row_header = []
    column_header = []

    #Data values for DataFrame
    data_simple = []
    data_progress = []
    data_ourconf = []

    #For every train data sheet (data model), run traces from test data sheets and calculate conformance value.
    for json_filename in os.listdir(train_path):
        if json_filename.endswith('.JSON'):
            row_header.append(json_filename)
            simple_data_row = []
            progress_data_row = []
            ourconf_data_row = []
            model = cc.DCR_graph(train_path+"/"+json_filename)

            for xes_filename in os.listdir(test_path):
                if xes_filename.endswith('.xes'):
                    if xes_filename not in column_header:
                        column_header.append(xes_filename)

                    traces = cc.read_log_from_XES(test_path+"/"+xes_filename)

                    simple_conf_val = cc.simple_conf(traces, model)
                    simple_data_row.append(simple_conf_val)
                    progress_based_conf_val = cc.progress_based_conf(traces, model)
                    progress_data_row.append(progress_based_conf_val)
                    ourconf_conf_val = cc.our_conf(traces, model)
                    ourconf_data_row.append(ourconf_conf_val)
            data_simple.append(simple_data_row)
            data_progress.append(progress_data_row)
            data_ourconf.append(ourconf_data_row)


    #Add data and max value of column to DataFrame
    simple_conf = pd.DataFrame(data_simple, column_header, row_header)
    simple_max = simple_conf.max()
    simple_max = pd.DataFrame(simple_max)
    simple_max.columns=['MAX']
    simple_max=simple_max.transpose()
    simple_df = simple_conf.append(simple_max)

    progress_conf = (pd.DataFrame(data_progress, column_header, row_header))
    progress_max = progress_conf.max()
    progress_max = pd.DataFrame(progress_max)
    progress_max.columns=['MAX']
    progress_max=progress_max.transpose()
    progress_df = progress_conf.append(progress_max)

    ourconf_conf = (pd.DataFrame(data_ourconf, column_header, row_header))
    ourconf_max = ourconf_conf.max()
    ourconf_max = pd.DataFrame(ourconf_max)
    ourconf_max.columns=['MAX']
    ourconf_max=ourconf_max.transpose()
    ourconf_df = ourconf_conf.append(ourconf_max)
    print('-----------------------------------------')
    print('Simple conformance                       ')
    print(simple_df)
    print('                                         ')
    print('-----------------------------------------')
    print('Progress conformance                     ')
    print(progress_df)
    print('                                         ')
    print('-----------------------------------------')
    print('OurConf conformance                     ')
    print(ourconf_df)
    print('                                         ')
    print('-----------------------------------------')
    simple_df.to_excel("dcr_simple_conf.xlsx")
    progress_df.to_excel("dcr_progress_conf.xlsx")
    ourconf_df.to_excel("dcr_ourconf_conf.xlsx")
    #print(simple_conf.style.to_latex())
    #print('                                         ')
    #print('                                         ')
    #print(progress_conf.style.to_latex())


if __name__ == "__main__":
    main()
