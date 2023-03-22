import matplotlib.pyplot as plt
import json
import time

history = []
x = time.time()
result = []

with open('history.json', 'r+') as f:
    history_data = json.load(f)
    print(type(history_data))
    print(len(history_data))


print(f"Загрузка заняла: {time.time() - x}")

for i in range(4999, 1, -1):
    now = json.loads(history_data[i])
    future = json.loads(history_data[i - 1])
    #print(now['Date'])
    #print(future['Date'])
    try:
        now_value =         now['Valute'][f"AMD"]['Value']
        previous_value =    now['Valute'][f"AMD"]['Previous']
        future_value =      future['Valute'][f"AMD"]['Value']
        result.append({
            "Value":    now_value,
            "Previous": previous_value,
            "Need":     1 if future_value > now_value else 0,
            "V":        "AMD"
        })
    except Exception as E:
        pass

for i in range(4999, 1, -1):
    now = json.loads(history_data[i])
    future = json.loads(history_data[i - 1])
    #print(now['Date'])
    #print(future['Date'])
    try:
        now_value =         now['Valute'][f"USD"]['Value']
        previous_value =    now['Valute'][f"USD"]['Previous']
        future_value =      future['Valute'][f"USD"]['Value']
        result.append({
            "Value":    now_value,
            "Previous": previous_value,
            "Need":     1 if future_value > now_value else 0,
            "V":        "USD"
        })
    except Exception as E:
        pass
    '''
    for _, j in now['Valute'].items():
        try:
            result.append({
                "Value":    j['Value'],
                "Previous": j['Previous'],
                "Need":     round(future['Valute'][f"{_}"]['Value'] - j['Value'], 4),
            })
        except Exception as E:
            pass
    '''
    '''
        print(j['Value'])
        print(future['Valute'][f"{_}"]['Value'])
        print(round(future['Valute'][f"{_}"]['Value'] - j['Value'], 4))'''
with open('result.json', 'w+') as f:
    json.dump(result, f, sort_keys=True, indent=4)
print(f"Полная работа скрипта заняла: {time.time() - x}")

'''
    for key, value in history.items():
        if type(value) == dict:
            for _key, _value in value.items():                
                if type(_value) == dict:
                    for __key, __value in _value.items():
                        print(__key, __value)
        else:
            print(key, value)
'''