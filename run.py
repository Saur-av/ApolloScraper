import os

cwd = os.getcwd()
files = os.listdir(cwd)

for file in files:
    # print(file)
    if file.endswith('.py') and not file.startswith('_'):
        if file == 'run.py' or file == 'des.py':
            pass
        else:
            os.system(f'start cmd.exe /k python ./{file}')