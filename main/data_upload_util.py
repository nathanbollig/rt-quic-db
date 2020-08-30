# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:58:56 2020

@author: NBOLLIG
"""
import csv
import io

"""
Parse file into a dictionary of the following format:
    rows[well_name] = [content, fluorescence_series]

where content is a string and fluorescence_series is an array parallel to array of times time_s_vals.

Returns:
    rows
    time_s_vals
"""
def parse_rt_quic_csv(file, decode="UTF8"):
    reading_fluor_data = False
    rows = {}
    
    stream = io.StringIO(file.stream.read().decode(decode), newline=None)
    csv_reader = csv.reader(stream)
    
    for row in csv_reader:
        well_name = None
        content = None
        fluorescence_series = None
        
        if (reading_fluor_data == True):
            well_name = row[0]
            content = row[1]
            fluorescence_series = row[2:]
            rows[well_name] = [content, fluorescence_series]
            
        if (reading_fluor_data == False) and row[1] == 'Time [sec]':
            time_s_vals = row[2:]
            reading_fluor_data = True
            
    return rows, time_s_vals


"""
Class for creating .csv that will be directly used to upload data into the Observation table.
"""
class UploadObsCSV:
    
    def __init__(self):
        self.rows = []
        header = ['fluorescence', 'time_s', 'x_coord', 'y_coord', 'plate_ID', 'wc_ID', 'index_in_well']
        self.rows.append(header)
    
    def add_observation(self, data, well_data, obs_data):
        fluorescence = obs_data['fluorescence']
        time_s = obs_data['time_s'] 
        x_coord = obs_data['x_coord'] 
        y_coord = obs_data['y_coord'] 
        plate_ID = data['plate']
        wc_ID = well_data['wc_ID']
        index_in_well = obs_data['index_in_well']
        
        new_row = [fluorescence, time_s, x_coord, y_coord, plate_ID, wc_ID, index_in_well]
        self.rows.append(new_row)
    
    def write_csv(self, path = 'temp_observation_load.csv'):
        with open(path, 'w', newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            for row in self.rows:
                wr.writerow(row)
        return file

"""
Class for creating .csv that will be directly used to upload data into the Well_Condition table.
"""
class UploadWellConditionCSV:
    
    def __init__(self):
        self.rows = []
        header = ['wc_ID', 'salt_type', 'salt_conc', 'substrate_type', 'substrate_conc', 
                  'surfact_type', 'surfact_conc', 'other_wc_attr', 'sample_ID', 'assay_ID', 'contents', 'well_name']
        self.rows.append(header)
    
    def add_record(self, data):
        wc_ID = data['wc_ID']
        salt_type = data['salt_type']
        salt_conc = data['salt_conc']
        substrate_type = data['substrate_type']
        substrate_conc = data['substrate_conc']
        surfact_type = data['surfact_type']
        surfact_conc = data['surfact_conc']
        other_wc_attr = data['other_wc_attr']
        sample_ID = data['sample_ID']
        assay_ID = data['assay_ID']
        contents = data['contents']
        well_name = data['well_name']
        
        new_row = [wc_ID, salt_type, salt_conc, substrate_type, substrate_conc, 
                  surfact_type, surfact_conc, other_wc_attr, sample_ID, assay_ID, contents, well_name]
        self.rows.append(new_row)
    
    def write_csv(self, path = 'temp_wc_load.csv'):
        with open(path, 'w', newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            for row in self.rows:
                wr.writerow(row)
        return file
    
    
    
    
    
    
    
    