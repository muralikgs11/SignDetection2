import json

lines = list()
with open('gt.txt', 'r') as f:
	for line in f:
		lines.append(line.rstrip())
		print(line.rstrip())
print('File has been parsed')

config_dict = dict()
for line in lines:
	l = line.split(';')
	if l[0] not in config_dict.keys():
		config_dict[l[0]] = dict()
		config_dict[l[0]]['classes'] = list()
		config_dict[l[0]]['coord'] = list()
	config_dict[l[0]]['classes'].append(int(l[5]))
	config_dict[l[0]]['coord'].append([int(l[1]), int(l[2]), int(l[3]), int(l[4])])

with open('GTSDB.json', 'r') as myfile:
    data=myfile.read()
    
myDict = json.loads(data)

frame_data = myDict['output']['frames']

for frames in frame_data:
    for coord in frames['signs']:
        if coord['class'] == 'pn':
            frame = frames['frame_number']
            print(frame)
            coords = coord['coordinates']
            coords[2] = coords[2] + coords[0]
            coords[3] = coords[3] + coords[1]
            try:
                config_dict[frame]['classes'].append(43)
                config_dict[frame]['coord'].append(coords)
            except:
                config_dict[frame] = dict()
                config_dict[frame]['classes'] = list()
                config_dict[frame]['coord'] = list()
                config_dict[frame]['classes'].append(43)
                config_dict[frame]['coord'].append(coords)
                

with open('gt_new.txt', 'w') as file:
    for keys in sorted(config_dict.keys()):
        l_coords = len(config_dict[keys]['classes'])
        for i in range(l_coords):
            coords = config_dict[keys]['coord'][i]
            clas = config_dict[keys]['classes'][i]
            string = keys + ';' + str(coords[0]) + ';' + str(coords[1]) + ';' + str(coords[2]) + ';' + str(coords[3]) + ';' + str(clas) + '\n'
            file.write(string)
            

#for frames in frame_data:
#    for coord in frames['signs']:
#        if coord['class'] == 'RedRoundSign':
#            frame = frames['frame_number']
#            print(frame)
#            