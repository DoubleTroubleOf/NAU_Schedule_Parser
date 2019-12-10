import requests
import collections, json, codecs
import os,datetime,time

#убираем дублирование групп в словаре по департаментах
def get_unique_items(list_of_dicts, key="NAME"):
    # Count how many times each key occurs.
    key_count = collections.defaultdict(lambda: 0)
    for d in list_of_dicts:
        key_count[d[key]] += 1

    return [d for d in list_of_dicts if key_count[d[key]] == 1]

# получаем коды всех подразделений университета
def get_dep_codes():
    response1 = requests.get('http://rozklad.nau.edu.ua/api/v1/departments')
    d = dict(response1.json())['departments']
    dep_codes = []
    for i in range(len(d)):
        dep_codes.append(d[i]['CODE'])
    return dep_codes

#получаем словарь групп готовый для дальнейшей обработки
def get_groups_by_deps(codes):
    groups = dict()
    for code in codes:
        response2 = requests.get('http://rozklad.nau.edu.ua/api/v1/groups/{0}'.format(code))
        group = response2.json()
        if group['status'] == True:
            groups[code] = group['groups']

    #список групп по департаментах
    grp = dict()
    for key in list(groups.keys()):
        grp[key] = get_unique_items(groups[key])
    return grp


dep_codes = get_dep_codes()

ready_groups = get_groups_by_deps(dep_codes)

#ready_groups.values()
#количество групп в универе
def ccccccc(grp):
    count = 0
    for key,value in grp.items():
        count += len(value)
    print('\n\n\n', count, '\n\n\n')

ccccccc(ready_groups)

def write_to_files(grp):
    for values in grp.values():
        for v in values:
            response = requests.get('http://rozklad.nau.edu.ua/api/v1/schedule/{department_code}/{course}/{stream}/{group_code}/{subgroup}'.format(department_code=v['DEP'],
                                                                                                                                        course=v['COURSE'], 
                                                                                                                                        stream=v['STRM'], 
                                                                                                                                        group_code=v['GRP'], 
                                                                                                                                        subgroup=1)
                                                                                                                                       )
            time.sleep(1)
            print(response.ok)
            if response.ok == True and dict(response.json())['status'] == True:
                with codecs.open(r'.\Folder\group{0}.txt'.format(v['NAME']), mode='w') as group_file:
                    
                    y = json.dumps(dict(response.json()) ["schedule"] , ensure_ascii=False).encode('utf-8')
                    #print(y.decode())
                    group_file.writelines(y.decode())

print('\n\n\nSTART\n\n\n')
write_to_files(ready_groups)
print('\n\n\nFINISH\n\n\n')




item = ready_groups[2][69]
response = requests.get('http://rozklad.nau.edu.ua/api/v1/schedule/{department_code}/{course}/{stream}/{group_code}/{subgroup}'.format(department_code=item['DEP'],
                                                                                                                                        course=item['COURSE'], 
                                                                                                                                        stream=item['STRM'], 
                                                                                                                                        group_code=item['GRP'], 
                                                                                                                                        subgroup=1)
                                                                                                                                        )
if response.ok == True and dict(response.json())['status'] == True:
    schedule = dict(response.json())['schedule']

print(schedule)