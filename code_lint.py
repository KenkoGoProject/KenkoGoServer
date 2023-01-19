"""
优化 import 排序，进行代码规范检查
"""
import subprocess

status = 0

status += subprocess.call(['isort', 'src/'])  # 导入排序
status += subprocess.call(['flake8', 'src/'])  # flake8代码规范
# status += subprocess.call(['mypy'])  # mypy代码规范

if status != 0:
    print('代码规范检查失败')
exit(status != 0)
