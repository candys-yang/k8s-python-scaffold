FROM rockylinux
#
# 环境变量
ENV LANG C.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
#
# YUM
RUN sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak /etc/yum.repos.d/Rocky-*.repo && dnf install epel-release -y
#
# 基础环境
RUN yum install gcc wget libffi-devel xz make openssl* zlib zlib-devel -y  \
  && cd /root \
  && wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tar.xz \
  && tar -xvJf Python-3.10.4.tar.xz \
  && cd Python-3.10.4 \
  && ./configure  \
  && make && make install && yum install python3-pip -y 
RUN groupadd --gid 5000 py \
  && useradd --home-dir /home/py --create-home --uid 5000 \
    --gid 5000 --shell /bin/sh --skel /dev/null py \
  && yum install passwd -y && echo 'yaokai' | passwd --stdin root
#
# 应用环境
WORKDIR /usr/app
ADD ./requirements.txt /app/
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple --upgrade pip \
  && pip3 install -r /app/requirements.txt
COPY ./ /usr/app
USER py
ENTRYPOINT ["python3","app.py"]