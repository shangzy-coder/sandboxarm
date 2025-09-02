#!/bin/bash
set -o errexit

py_ver="$1"
location="$2"

# 检测架构
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ]; then
    ARCH_SUFFIX="aarch64"
else
    ARCH_SUFFIX="x86_64"
fi

FILENAME=Miniconda3-py${py_ver//.}_23.5.2-0-Linux-${ARCH_SUFFIX}.sh

if [ "$1" = "3.7" ]
then
FILENAME=Miniconda3-py${py_ver//.}_23.1.0-1-Linux-${ARCH_SUFFIX}.sh
fi

if [ "$location" = "us" ]
then
  MIRROR="https://repo.anaconda.com/miniconda"
else
  MIRROR="https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda"
fi

wget ${MIRROR}/${FILENAME}
mkdir -p /root/.conda
bash ${FILENAME} -b
rm -f ${FILENAME}
