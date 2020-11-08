from remarkable2 import Remarkable2
from sys import argv, exit

rM = Remarkable2()

obtained_file = None
if len(argv) == 2:
    obtained_file = rM.download(document_uuid=argv[1])
elif len(argv) == 3:
    obtained_file = rM.download(document_uuid=argv[1], target_file=argv[2])
else:
    print(
        f'Example usage:\n'
        f' {argv[0]} file_uuid_in_reMarkable2_device\n'
        f' {argv[0]} file_uuid_in_reMarkable2_device ../\n'
        f' {argv[0]} file_uuid_in_reMarkable2_device /tmp/\n'
        f' {argv[0]} file_uuid_in_reMarkable2_device /tmp/filename.pdf\n'
        f' {argv[0]} file_uuid_in_reMarkable2_device new_filename.pdf\n'
        f'Keep in mind if second parameter is in directory expression (ex. /mydir/), it must exist.'
    )
    exit(1)

if obtained_file:
    print(f'Obtained file should be at "{obtained_file}"')
