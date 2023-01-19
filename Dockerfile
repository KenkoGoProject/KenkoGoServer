FROM python:3.9-slim
COPY . /build

# 设置时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& dpkg-reconfigure -f noninteractive tzdata \
# 修改镜像源
# && sed -i s@/deb.debian.org/@/mirrors.163.com/@g /etc/apt/sources.list \
# && sed -i s@/security.debian.org/@/mirrors.163.com/@g /etc/apt/sources.list \
# 更新系统
# && apt update -y \
# && apt upgrade -y \
# 配置pip国内源
&& pip config set global.index-url https://pypi.doubanio.com/simple \
# 安装依赖
# && apt install -y libzbar0 \
&& pip --no-cache-dir install --upgrade pip \
&& pip --no-cache-dir install wheel \
# 部署程序
&& cd /build \
&& pip --no-cache-dir install -r requirements.txt \
&& mkdir /app \
&& cp -r ./src/* /app \
# 清理缓存 \
&& cd \
&& rm -rf /build \
# && apt clean \
# && rm -rf /var/lib/apt/lists/* \
&& rm -rf ~/.cache/pip

EXPOSE 18082
VOLUME /app/data

WORKDIR /app
ENTRYPOINT ["python", "main.py"]
CMD ["--docker"]
