# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi.testclient import TestClient

from sandbox.server.sandbox_api import RunCodeRequest, RunCodeResponse, RunStatus
from sandbox.server.server import app

client = TestClient(app)

code = r'''
def word_count(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 移除标点符号并转换为小写
        translator = str.maketrans("", "", string.punctuation)
        content = content.translate(translator).lower()

        # 使用 Counter 统计单词出现次数
        words = content.split()
        word_counter = Counter(words)

        # 按照出现次数降序排列
        sorted_word_count = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)

        for word, count in sorted_word_count:
            print(f"'{word}': {count}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

import string
from collections import Counter


class Testword_count:
    def test_word_count_case_sensitive_file(self, capfd, tmp_path):
        file_path = tmp_path / 'test_case_sensitive.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("Case case CASE")
        word_count(file_path)
        captured = capfd.readouterr()
        assert "'case': 3" in captured.out


    def test_word_count_punctuation_file(self, capfd, tmp_path):
        file_path = tmp_path / 'test_punctuation.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("This sentence has some punctuation, like commas and periods.")
        word_count(file_path)
        captured = capfd.readouterr()
        assert "'this': 1\n'sentence': 1\n'has': 1\n'some': 1\n'punctuation': 1\n'like': 1\n'commas': 1\n'and': 1\n'periods': 1\n" in captured.out
'''

fail_code = r'''
def word_count(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 移除标点符号并转换为小写
        translator = str.maketrans("", "", string.punctuation)
        content = content.translate(translator).lower()

        # 使用 Counter 统计单词出现次数
        words = content.split()
        word_counter = Counter(words)

        # 按照出现次数降序排列
        sorted_word_count = sorted(word_counter.items(), key=lambda x: x[1], reverse=True)

        for word, count in sorted_word_count:
            print(f"'{word}': {count}")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

import string
from collections import Counter


class Testword_count:
    def test_word_count_case_sensitive_file(self, capfd, tmp_path):
        file_path = tmp_path / 'test_case_sensitive.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("Case case CASE")
        word_count(file_path)
        captured = capfd.readouterr()
        assert "'case': 3" not in captured.out


    def test_word_count_punctuation_file(self, capfd, tmp_path):
        file_path = tmp_path / 'test_punctuation.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("This sentence has some punctuation, like commas and periods.")
        word_count(file_path)
        captured = capfd.readouterr()
        assert "'this': 1\n'sentence': 1\n'has': 1\n'some': 1\n'punctuation': 1\n'like': 1\n'commas': 1\n'and': 1\n'periods': 1\n" not in captured.out
'''


def test_pytest_pass():
    request = RunCodeRequest(language='python', code=code, run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Success

    request = RunCodeRequest(language='pytest', code=code, run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    print(result)
    assert result.status == RunStatus.Success


def test_pytest_fail():
    request = RunCodeRequest(language='python', code=fail_code, run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Success

    request = RunCodeRequest(language='pytest', code=fail_code, run_timeout=5)
    response = client.post('/run_code', json=request.model_dump())
    assert response.status_code == 200
    result = RunCodeResponse(**response.json())
    assert result.status == RunStatus.Failed
