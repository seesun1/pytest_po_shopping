# python-jenkins
import os

import requests
from jenkins import Jenkins

jenkins_url = "http://localhost:8080/"
# 链接jenkins
server = Jenkins(url=jenkins_url, username="admin", password="123456", timeout=10)
job_name = "job/pytest_selenium"
# 获取job地址
job_url = server.get_info(job_name)['url']
job_last_number = server.get_info(job_name)['lastBuild']['number']
# allure报告地址
allure_url = job_url + str(job_last_number) + '/allure/'


def push_message():
    file_path = os.path.dirname(os.getcwd()) + '/allure-report/export/prometheusData.txt'
    print(file_path)
    # file_path = '/Users/tester/Documents/web自动化测试/WebAutoTest/allure-report/export/prometheusData.txt'
    content = {}
    with open(file_path) as f:
        for line in f.readlines():
            launch_name = line.strip('\n').split(' ')[0]
            launch_num = line.strip('\n').split(' ')[1]
            content.update({launch_name: launch_num})
    # 测试用例数
    case_num = content['launch_retries_run']
    # 通过数量
    passed_num = content['launch_status_passed']
    # 失败数量
    failed_num = content['launch_status_failed']
    # 阻塞数量
    broken_num = content['launch_status_broken']
    # 跳过数量
    skipped_num = content['launch_status_skipped']
    # 未知数量
    unknown_num = content['launch_status_unknown']
    """
    发送消息，通过webhook的方式
    """
    webhook = ""
    json_data = {
        "msgtype": "text",
        "text": {
            "content": "UI自动化脚本执行结果：\n运行总数" + case_num
                       + "\n通过数量：" + passed_num
                       + "\n失败数量：" + failed_num
                       + "\n阻塞数量：" + broken_num
                       + "\n跳过数量：" + skipped_num
                       + "\n未知数量：" + unknown_num
                       + "\n构建地址：\n" + job_url
                       + "\n报告地址：\n" + allure_url
        }
    }
    requests.post(url=webhook, json=json_data, verify=False)


# push_message()
if __name__ == '__main__':
    push_message()
