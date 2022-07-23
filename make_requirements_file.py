# 生成 requirements.txt
import subprocess

status = 0

for i in ('requirements', 'requirements-dev'):
    status += subprocess.call(['pip-compile', f'{i}.in',
                               '--output-file', f'{i}.txt',
                               '--annotation-style=line'])
    with open(f'{i}.txt', 'r') as f:
        lines = f.readlines()
    with open(f'{i}.txt', 'w') as f:
        for line in lines:
            if line.startswith('--index-url'):
                continue
            f.write(line)

exit(status != 0)
