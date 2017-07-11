# -*- coding: utf-8 -*-
"""
author: alexost82
"""

import zipfile, tarfile, os, sys, tempfile

zips = []
tars = []

def list_all_nested_files(path_to_target, prefix=''):
    
    def tar_processing(path_to_tar):
        print " TAR processing... \n"#, path_to_tar
        tars.append(path_to_target)
        t = tarfile.open(path_to_tar)
        for i in t.getnames():
            if t.getmember(i).isdir():
                nested_files_list.append(prefix+i+"/")
                continue
            nested_files_list.append(prefix+i)
            fd, nested_file_path = tempfile.mkstemp()
            try:
                os.write(fd, t.extractfile(i).read())
                if zipfile.is_zipfile(nested_file_path) or tarfile.is_tarfile(nested_file_path):
                    new_list = list_all_nested_files(nested_file_path, prefix+i+"/")
                    nested_files_list.extend(new_list)
                os.close(fd)
            except AttributeError as err:
                print('An exception happened: ' + str(err))
            finally:
                os.remove(nested_file_path)
        t.close()

    def zip_processing(path_to_zip):
        print ' ZIP processing... \n'#, path_to_target
        zips.append(path_to_target)
        z = zipfile.ZipFile(path_to_target)
        for i in z.namelist():
            nested_files_list.append(prefix+i)
            fd, nested_file_path = tempfile.mkstemp()
            os.write(fd, z.read(i))
            if zipfile.is_zipfile(nested_file_path) or tarfile.is_tarfile(nested_file_path):
                new_list = list_all_nested_files(nested_file_path, prefix+i+"/")
                nested_files_list.extend(new_list)
            os.close(fd)
            os.remove(nested_file_path)
        z.close()

    path_to_target = path_to_target.rstrip("/")
    if prefix == '': prefix = path_to_target+"/"
    nested_files_list = []

    print 'Parsing object: ', prefix.rstrip("/")
    print '--', path_to_target
    #processing folder
    if os.path.isdir(path_to_target):
        for i in os.listdir(path_to_target):
            direct_path = path_to_target + "/" + i
            #print direct_path, 'direct'
            nested_files_list.append(direct_path)
            if os.path.isdir(direct_path):
                index = nested_files_list.index(direct_path)
                nested_files_list[index] = direct_path + "/"
                new_list = list_all_nested_files(direct_path)
                nested_files_list.extend(new_list)
                continue
            elif os.path.islink(direct_path):
                continue
            elif os.path.getsize(direct_path) == 0:
                continue
            elif zipfile.is_zipfile(direct_path) or tarfile.is_tarfile(direct_path):
                new_list = list_all_nested_files(direct_path, prefix+i+"/")
                nested_files_list.extend(new_list)
                    
    elif tarfile.is_tarfile(path_to_target): tar_processing(path_to_target)
    elif zipfile.is_zipfile(path_to_target): zip_processing(path_to_target)
    
    else:
        print('{} is not an archive or a folder'.format(path_to_target))
    
    return sorted(nested_files_list)
    
if __name__ == '__main__':
    #print 'par', os.path.abspath(sys.argv[1])
    for i in list_all_nested_files(sys.argv[1]):
        print i
    
    print "================"
    print len(zips), 'zips detected:'
    #print zips
    print len(tars), 'tars detected:'
    #print tars

        