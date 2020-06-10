import json, random
train_portion = 2
test_portion = 1
val_portion = 1

num_split = train_portion+val_portion+test_portion

dict_ = {}
for line in [ line[:-1] for line in open("gdc_manifest.txt").readlines()[1:]] :
    id = line.split('\t')[1][:12]
    if id in dict_:
        dict_[id] += 1
    else:
        dict_[id] = 1
users = []
for key, values in dict_.items():
    if(values>1):
        users.append(key)

users_dict = dict(zip(users,[[] for i in range(0,len(users))]))
print(users_dict)
data = json.load(open("chunks/training_chunks_3.json"))
train_size = len(data['chunks'][0]['imgs'])
val_size = len(data['chunks'][0]['imgs'])
test_size = len(data['chunks'][0]['imgs'])
other_users = []
for chunk in data['chunks'] :
    print(len(chunk['imgs']))
    for path_ in chunk['imgs'] :
        # print(path_)data['chunks']
        user_id = path_[path_.find('TCGA-'):path_.find('TCGA-')+12]
        if user_id in users :
            users_dict[user_id].append(path_)
        else :
            other_users.append(path_)
split_size = (sum([len(value_) for value_ in users_dict.values()]) + len(other_users))//num_split
randomly_data_size = len(other_users)//num_split
train_set = other_users[0:train_portion*randomly_data_size]
val_set   = other_users[train_portion*randomly_data_size:(train_portion+val_portion)*randomly_data_size]
test_set  = other_users[(train_portion+val_portion)*randomly_data_size:]

print(len(train_set),len(val_set),len(test_set))

for values in users_dict.values() :
    if len(train_set) < split_size*train_portion:
        train_set+= values[:] if len(train_set)+len(values)< split_size*train_portion else values[:split_size*train_portion-len(train_set)]
        continue
    elif len(val_set) < split_size*val_portion:
        val_set += values[:] if len(val_set) + len(values) < split_size * val_portion else values[:split_size * val_portion - len(val_set)]
        continue
    elif len(test_set) < split_size * test_portion:
        test_set += values[:] if len(test_set) + len(values) < split_size * test_portion else values[:split_size * test_portion - len(test_set)]


print(len(train_set),len(val_set),len(test_set))

obj = {"chunks": []}

for i, chunk in enumerate([train_set, val_set, test_set]):
    obj["chunks"].append({"id": i, "imgs": chunk})

f = open("chunks/training_chunks_3_patient.json", "w")

f.write(json.dumps(obj, indent=4))

f.close()