from remarkable2 import Remarkable2
from sys import argv, exit


rM = Remarkable2()

if len(argv) > 1:
    data = rM.ls(argv[1])
else:
    data = rM.ls()

if data:
    for bookmark in data:
        id = bookmark['ID']
        object_type = bookmark['Type']
        name = bookmark['VissibleName']
        modified = bookmark['ModifiedClient']
        if object_type == 'CollectionType':
            print(f'[{modified}] [{id}] {name} [ DIR ]')
        else:
            file_type = bookmark['fileType']
            page_count = bookmark['pageCount']
            print(f'[{modified}] [{id}] {name} [{file_type}] [Pages: {page_count} ]')
else:
    print("No data obtained.")
    exit(1)
