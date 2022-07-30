"""构建生成二进制版本
该版本仅在 Windows 上适用"""
import os.path
import subprocess
import time

from module.global_dict import Global

build_dir = './build'
ico_path = 'icon.ico'


def build_exe():
    return subprocess.run(
            args=[
                './venv/Scripts/python.exe', '-m', 'nuitka',

                '--mingw64',  # 使用mingw64编译
                '--full-compat',  # 兼容嵌入式python
                # '--windows-disable-console',  # 禁用windows控制台

                # 以下选项最多三选一，不选则编译为需要Python环境的可执行文件
                # '--standalone',  # 生成独立可执行环境，不嵌入python
                # '--onefile',  # 生成单文件
                # '--module',  # 生成库文件而不是可执行程序

                '--show-progress',  # 显示进度
                '--show-modules',  # 显示模块
                # '--show-memory',  # 显示内存使用量

                '--warn-implicit-exceptions',  # 警告隐式异常
                '--warn-unusual-code',  # 警告不规范代码

                '--plugin-enable=upx',  # 开启upx压缩

                '--nofollow-imports',  # 所有的import不打包进exe，交给python3x.dll查找
                # '--include-package=pyzbar',  # 打包比如 numpy, PyQt5 这些带文件夹的叫包或者轮子
                '--include-module=kenko_go',  # 需要打包进exe的模块
                '--follow-import-to=module,assets',  # 需要打包进exe的包

                f'--windows-icon-from-ico={ico_path}',  # 可执行文件图标
                f'--windows-company-name={Global().author_name}',
                f'--windows-product-name={Global().app_name}',
                f'--windows-file-version={Global().version_str}',
                f'--windows-product-version={Global().version_str}',
                f'--windows-file-description={Global().description}',

                f'--output-dir={build_dir}',  # 输出目录
                '-o', f'{build_dir}/{Global().app_name}.exe',
                './src/main.py'
            ],
            cwd=os.path.curdir
        )


def make_build_env():
    """安装运行时环境"""
    return subprocess.call(args=[
        './venv/Scripts/python.exe', '-m', 'pip', 'install', '-r', 'requirements.txt'
    ], cwd=os.path.curdir)


if __name__ == '__main__':
    start_time = time.time()
    make_build_env()
    build_exe()
    # if Path(f'{build_dir}/KenkoGo.exe').exists():
    #     Path(f'{build_dir}/KenkoGo.exe').unlink()
    # Path(f'{build_dir}/main.exe').rename(f'{build_dir}/KenkoGo.exe')
    # Path(f'{build_dir}/release').mkdir(exist_ok=True)
    # Path(f'{build_dir}/KenkoGo.exe').rename(f'{build_dir}/release/KenkoGo.exe')
    print(f'Time consumption: {(time.time() - start_time):.2f}s')
