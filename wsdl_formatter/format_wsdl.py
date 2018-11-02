import pathlib


read_file = pathlib.Path('./wsdl.txt')
with read_file.open(mode='r') as r:
    f = r.read()

formatted = f.split(',')

write_file = pathlib.Path('./formatted.txt')
with write_file.open(mode='w') as w:
    for f in formatted:
        w.write(f'{f.strip()}\n')
