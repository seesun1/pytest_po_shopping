import allure
import pytest
from selenium import webdriver

from utils.get_filepath import get_screen_shot_path


@pytest.fixture(scope="session")
def driver_project():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://meikefresh.5istudy.online/")
    print("打开浏览器")
    yield driver
    print("关闭浏览器")
    driver.close()
    driver.quit()


# 钩子函数，结果
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     """
#
#     :param item: 代表测试函数或方法，包含测试相关的信心，比如名称，位置，标记
#     :param call: 包含测试函数执行的详细信息，比如结果，执行时间
#     :return:
#     when = setup:前置
#     when = call:执行测试用例
#     when = teardown:后置
#     """
#     print("=========================")
#     # 获取钩子函数的结果
#     out = yield
#     # 获取测试报告
#     report = out.get_result()
#
#     # print(f"测试报告：{report}")
#     # print(f"步骤：{report.when}")
#     # print(f"nodeid：{report.nodeid}")
#     # print(f"运行结果：{report.outcome}")
#     # 失败测试用例截图
#     if report.when == 'call' and report.failed:
#         # 保存到本地
#         driver.save_screenshot(get_screen_shot_path())
#         # 截图,get_screenshot_as_png二进制数据
#         # 使用allure.attach将二进制数据附加到allure报告中
#         allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
