import os.path
import subprocess
import time

from module.global_dict import Global

build_dir = './build'
ico_path = 'icon.ico'


def build_exe():
    return subprocess.run(
            args=[
                './venv/Scripts/python.exe',
                '-m',
                'nuitka',

                '--mingw64',  # 使用mingw64编译
                '--full-compat',  # 兼容嵌入式python
                # '--windows-disable-console',  # 禁用windows控制台

                # 以下选项三选一
                '--standalone',  # 生成独立可执行环境
                # '--onefile',  # 生成单文件
                # '--module',  # 生成库文件而不是可执行程序

                '--show-progress',  # 显示进度
                '--show-modules',  # 显示模块
                # '--show-memory',  # 显示内存使用量

                '--warn-implicit-exceptions',  # 警告隐式异常
                '--warn-unusual-code',  # 警告不规范代码

                # '--plugin-enable=upx',  # 开启upx压缩
                # '--plugin-enable=pyside6',  # 开启pyside6插件

                # '--nofollow-imports',  # 所有的import不打包进exe，交给python3x.dll查找
                # '--include-package=logging',  # 打包比如numpy,PyQt5 这些带文件夹的叫包或者轮子
                # '--include-module=',  # 打包比如when.py 这些以.py结尾的叫模块
                # '--follow-import-to=logging',
                # '--follow-import-to=KenkoWin',  # 需要编译成C/C++的py包

                f'--windows-icon-from-ico={ico_path}',  # 可执行文件图标
                f'--windows-company-name={Global().author_name}',
                f'--windows-product-name={Global().app_name}',
                f'--windows-file-version={Global().version_num}',
                f'--windows-product-version={Global().version_num}',
                f'--windows-file-description={Global().description}',

                f'--output-dir={build_dir}',  # 输出目录
                './src/main.py'
            ],
            cwd=os.path.curdir
        )


def make_build_env():
    return subprocess.call(args=[
        './venv/Scripts/python.exe', '-m', 'pip', 'install', '-r', 'requirements.txt'
    ], cwd=os.path.curdir)


if __name__ == '__main__':
    start_time = time.time()
    make_build_env()
    build_exe()
    os.rename(f'{build_dir}/main.dist/main.exe', f'{build_dir}/main.dist/KenkoGo.exe')
    print(f'耗时：{(time.time() - start_time):.2f}s')
