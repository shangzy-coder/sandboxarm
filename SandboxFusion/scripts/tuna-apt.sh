#!/bin/bash
set -o errexit

apt-get update
apt-get install -y apt-transport-https ca-certificates

# 检测架构
ARCH=$(dpkg --print-architecture)

if [ "$1" = "20.04" ]
then
    if [ "$ARCH" = "arm64" ]; then
        # ARM64使用官方Ubuntu Ports镜像源
        echo $'deb http://ports.ubuntu.com/ubuntu-ports/ focal main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ focal-updates main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ focal-backports main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ focal-security main restricted universe multiverse
' > /etc/apt/sources.list
    else
        # AMD64使用清华镜像源
        echo $'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ focal-security main restricted universe multiverse
' > /etc/apt/sources.list
    fi

elif [ "$1" = "22.04" ]
then
    if [ "$ARCH" = "arm64" ]; then
        # ARM64使用官方Ubuntu Ports镜像源
        echo $'deb http://ports.ubuntu.com/ubuntu-ports/ jammy main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-updates main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-backports main restricted universe multiverse
deb http://ports.ubuntu.com/ubuntu-ports/ jammy-security main restricted universe multiverse
' > /etc/apt/sources.list
    else
        # AMD64使用清华镜像源
        echo $'deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
' > /etc/apt/sources.list
    fi

else

echo "ubuntu version $1 not supported"
exit 1;

fi
