with open('target_rtings.txt') as file:
    target_list = []
    import json

    j_fy = json.loads(file.read())
    for line in j_fy:
        target_list.append([line[0], line[-1]])

with open('target_rtings.txt', mode='w') as file:
    for data in target_list:
        file.writelines(str(data[0]) + ', ' + str(data[1])+'\n')
