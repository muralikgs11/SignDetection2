#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:23:15 2019

@author: murali
"""
import json
import numpy as np

def modGTDict(lines):
    config_dict = dict()
    for line in lines:
    	l = line.split(';')
    	if l[0] not in config_dict.keys():
    		config_dict[l[0]] = dict()
    		config_dict[l[0]]['classes'] = list()
    		config_dict[l[0]]['coord'] = list()
    	config_dict[l[0]]['classes'].append(int(l[5]))
    	config_dict[l[0]]['coord'].append([int(l[1]), int(l[2]), int(l[3]), int(l[4])])
    
    classes_dict = {'pn': [43], 'pne': [17], 'ps': [14], 'pg': [13], 'RedRoundSign': [0,1,2,3,4,5,7,8,9,10,15,16]}
    
    mod_dict = dict()
    for f in range(1,899):
        frame_no = '{0:05}'.format(f) + '.ppm'
        mod_dict[frame_no] = dict()
        mod_dict[frame_no]['classes'] = list()
        mod_dict[frame_no]['coord'] = list()
        
        try:
            l_classes = len(config_dict[frame_no]['classes'])
            for i in range(l_classes):
                classes = config_dict[frame_no]['classes'][i]
                coord = config_dict[frame_no]['coord'][i]
                for key in classes_dict:
                    if classes in classes_dict[key]:
                        mod_dict[frame_no]['classes'].append(key)
                        mod_dict[frame_no]['coord'].append(coord)
        except:
            continue
        
    return mod_dict

def predDict(myDict):
    pred_dict = dict()

    frame_data = myDict['output']['frames']
    
    for frames in frame_data:
        frame = frames['frame_number']
        pred_dict[frame] = dict()
        pred_dict[frame]['classes'] = list()
        pred_dict[frame]['coord'] = list()
        for coord in frames['signs']:
            pred_dict[frame]['classes'].append(coord['class'])
            coords = coord['coordinates']
            coords[2] = coords[2] + coords[0]
            coords[3] = coords[3] + coords[1]
            pred_dict[frame]['coord'].append(coords)

    return pred_dict    

def comArea(coords):
    return (coords[2] - coords[0])*(coords[3] - coords[1])

def interCoords(d_coords, t_coords):
    x1 = (d_coords[0] > t_coords[0])*d_coords[0] + (d_coords[0] <= t_coords[0])*t_coords[0] 
    y1 = (d_coords[1] > t_coords[1])*d_coords[1] + (d_coords[1] <= t_coords[1])*t_coords[1]
    x2 = (d_coords[2] < t_coords[2])*d_coords[2] + (d_coords[2] >= t_coords[2])*t_coords[2]
    y2 = (d_coords[3] < t_coords[3])*d_coords[3] + (d_coords[3] >= t_coords[3])*t_coords[3]
    return [x1, y1, x2, y2]

def computeIOU(d_coords, t_coords):
    
    inter_coords = interCoords(d_coords, t_coords)
    inter_area = comArea(inter_coords)    
    union_area = comArea(d_coords) + comArea(t_coords) - inter_area
    return inter_area/union_area
    

def computeStats(pred_dict, gt_dict):
    classes_dict = {'pn': {'TP': 0, 'FP': 0, 'FN': 0, 'precision': 0, 'recall': 0}, 'pne': {'TP': 0, 'FP': 0, 'FN': 0, 'precision': 0, 'recall': 0}, 'ps': {'TP': 0, 'FP': 0, 'FN': 0, 'precision': 0, 'recall': 0}, 'pg': {'TP': 0, 'FP': 0, 'FN': 0, 'precision': 0, 'recall': 0}, 'RedRoundSign': {'TP': 0, 'FP': 0, 'FN': 0, 'precision': 0, 'recall': 0}}
    
    for key in pred_dict:
        p_classes = pred_dict[key]['classes']
        p_coords = pred_dict[key]['coord']
        
        g_classes = gt_dict[key]['classes']
        g_coords = gt_dict[key]['coord']
        g_miss = np.ones(len(g_classes))
        for i in range(len(p_classes)):
            if p_classes[i] in g_classes:
                cl_ind = [it for it in range(len(g_classes)) if p_classes[i] == g_classes[it]]
                flag = 0
                for ind in cl_ind:
                    # compute IoU between p_coords[i] and g_coords[ind]
                    IoU = computeIOU(p_coords[i], g_coords[ind])
                    if IoU >= 0.5:
                        classes_dict[p_classes[i]]['TP'] += 1
                        flag = 1
                        g_miss[ind] = 0
                        
                if flag == 0:
                    if p_classes[i] == 'pg':
                        print('FP', key)
                    classes_dict[p_classes[i]]['FP'] += 1
                
        for i in range(len(g_classes)):
            if g_miss[i] == 1:
                if g_classes[i] == 'ps':
                    print('FN', key)
                    
                classes_dict[g_classes[i]]['FN'] += 1
    
    for key in classes_dict:
        TP = classes_dict[key]['TP']
        FP = classes_dict[key]['FP']
        FN = classes_dict[key]['FN']
        classes_dict[key]['precision'] = TP/(TP + FP)
        classes_dict[key]['recall'] = TP/(TP + FN)
    
    return classes_dict

if __name__ == '__main__':
    
    lines = list()
    with open('gt_new.txt', 'r') as f:
    	for line in f:
    		lines.append(line.rstrip())
        
    print('File has been parsed')
    
    gt_dict = modGTDict(lines)

    with open('GTSDB.json', 'r') as myfile:
        data=myfile.read()    
    myDict = json.loads(data)

    pred_dict = predDict(myDict)
    
    classes_dict = computeStats(pred_dict, gt_dict)