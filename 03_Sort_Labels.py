#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, argparse


# In[2]:


patch_dir = None
sorted_dir = None
labels_file = None


def sort_folders(patch_dir, sorted_dir):
    if not os.path.exists(sorted_dir):
        os.mkdir(sorted_dir)
    for sub_folder in os.listdir(patch_dir):
        for label in os.listdir(os.path.join(patch_dir,sub_folder)) :
            if not os.path.exists(os.path.join(sorted_dir,label)):
                os.mkdir(os.path.join(sorted_dir,label))
            print(os.path.join(sorted_dir,label,sub_folder), os.path.join(patch_dir,sub_folder,label))
            os.symlink(os.path.join(patch_dir,sub_folder,label),os.path.join(sorted_dir,label,sub_folder))

    return


def run():
    global patch_dir
    global sorted_dir
    global labels_file

    parser = argparse.ArgumentParser()
    parser.add_argument("--patch_location", help="local location of patch images")
    parser.add_argument("--sorted_location", help="desired local location of sorted patches")

    args = parser.parse_args()

    if args.patch_location != None:
        patch_dir = args.patch_location
    else:
        raise ValueError('No patch_location given')

    if args.sorted_location != None:
        sorted_dir = args.sorted_location
    else:
        raise ValueError('No sorted_location given')

    sort_folders(patch_dir, sorted_dir)



if __name__ == "__main__":
    run()

