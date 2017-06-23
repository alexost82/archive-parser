import StringIO, zipfile, tarfile, os, tempfile

def list_all_nested_files(path_to_archive, prefix=''):
    nested_files_list = []
    #processing tar
    if tarfile.is_tarfile(path_to_archive):
        t = tarfile.open(path_to_archive)
        for i in t.getnames():
            nested_files_list.append(prefix+i)
            if t.getmember(i).isdir():
                continue
            fd, nested_file_path = tempfile.mkstemp()
            os.write(fd, t.extractfile(i).read())
            if zipfile.is_zipfile(nested_file_path) or tarfile.is_tarfile(nested_file_path):
                new_list = list_all_nested_files(nested_file_path, prefix+i+'/')
                nested_files_list.extend(new_list)
            os.close(fd)
    #processing zip
    elif zipfile.is_zipfile(path_to_archive):
        z = zipfile.ZipFile(path_to_archive)
        for i in z.namelist():
            nested_files_list.append(prefix+i)
            fd, nested_file_path = tempfile.mkstemp()
            os.write(fd, z.read(i))
            if zipfile.is_zipfile(nested_file_path) or tarfile.is_tarfile(nested_file_path):
                new_list = list_all_nested_files(nested_file_path, prefix+i+'/')
                nested_files_list.extend(new_list)
            os.close(fd)
    else:
        print('{} is not an accepted archive file'.format(path_to_archive))

    return nested_files_list