dict_ = {}
for line in [ line[:-1] for line in open("gdc_manifest.txt").readlines()[1:]] :
    id = line.split('\t')[1][:12]
    if id in dict_:
        dict_[id] += 1
    else:
        dict_[id] = 1
value = 0
print (dict_)
for key, values in dict_.items():
    if(values>1):
        print(key)