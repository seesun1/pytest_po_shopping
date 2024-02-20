# -*- coding: utf-8 -*-
# @Time    : 2024/2/16 17:30
# @File    : test_user.py
# @Software: PyCharm
import time

import allure
import pytest

from page.user_page import UserPage
from testcases.user_center.conftest import delete_user, delete_code
from utils.assert_util import assert_compare
from utils.mysql_util import db
from utils.read import read_yaml



@allure.epic("美客生鲜的项目")
@allure.feature("用户中心")
@pytest.mark.run(order=1)
class TestUser:
    @allure.title("未登录时跳转")
    def test_go_login(self,driver_project):
        page=UserPage(driver_project)
        with allure.step('点击登录'):
            page.click(page.ple_login)
        actual_url=page.get_current_url()
        expected_url=r'http://meikefresh.5istudy.online/#/app/login'
        assert_compare(expected_url,'==',actual_url)
        page.back()
        page.move_to_element(page.vip_center)
        with allure.step('点击我的收藏'):
            page.click(page.my_fav)
        actual_url=page.get_current_url()
        expected_url=r'http://meikefresh.5istudy.online/#/app/login'
        assert_compare(expected_url,'==',actual_url)
        page.back()
        with allure.step('点击去购物车结算'):
            page.click(page.shopping_cart)
        page.switch_to_window()
        actual_url = page.get_current_url()
        expected_url = r'http://meikefresh.5istudy.online/#/app/login'
        assert_compare(expected_url, '==', actual_url)
        page.switch_to_window(to_parent_window=True)

    @allure.title("用户注册成功")
    def test_register(self, driver_project):
        page=UserPage(driver_project)
        data=read_yaml()['register_ok']
        with allure.step('点击免费注册'):
            page.click(page.register)
        with allure.step('输入手机号'):
            page.send_keys(page.register_mobile,data['mobile'])
        with allure.step("点击获取验证码"):
            page.click(page.send_code)
            time.sleep(2)  #等待数据库查询最新的验证码，以防多次点击使用的旧验证码
        with allure.step("获取短信验证码"):
            sql = f"select code from users_verifycode where mobile = {data['mobile']} order by id desc limit 1;"
            code = db.select_db_one(sql)['code']
        with allure.step("输入验证码"):
            page.send_keys(page.input_code, code)
        with allure.step("输入密码"):
            page.send_keys(page.input_password, data['password'])
        with allure.step("点击注册并登录"):
            page.click(page.register_submit)
        text = page.get_text(page.user_name)
        assert_compare(str(data['mobile']), "==", text)
        #清除数据到初始页面
        with allure.step("退出"):
            page.click(page.logout)
        page.get_url(r'http://meikefresh.5istudy.online/')
        delete_user(data['mobile'])
        delete_code(data['mobile'])

    @allure.title("用户注册失败-用户已存在")
    def test_register_exist(self, driver_project):
        """
        已存在的用户注册
        :param driver_project:
        :return:
        """
        mobile = read_yaml()['register_exist']['mobile']
        page = UserPage(driver_project)
        # page.refresh()
        page.click(page.register)
        page.send_keys(page.register_mobile, mobile)
        page.click(page.send_code)
        text = page.get_text(page.user_exist)
        assert_compare("用户已经存在", '==', text)
        # 清除数据到初始页面
        page.get_url(r'http://meikefresh.5istudy.online/')


    @allure.title("用户登录4个场景")
    @pytest.mark.parametrize('data', read_yaml()['user_login'])
    def test_user_login(self, driver_project, data):
        mobile, password = str(data['mobile']), str(data['password'])
        page = UserPage(driver_project)
        page.get_url(r'http://meikefresh.5istudy.online/')
        with allure.step('点击登录'):
            page.click(page.ple_login)
        page.send_keys(page.login_account, mobile)
        page.send_keys(page.login_password, password)
        page.click(page.login_btn)
        if mobile == '':
            text = page.get_text(page.login_account_error)
            assert_compare("该字段不能为空。", '==', text)
        elif password == '':
            text = page.get_text(page.login_password_error)
            assert_compare("该字段不能为空。", '==', text)
        elif mobile == '13800001111' and password == '123451':
            text = page.get_text(page.login_error)
            assert_compare("无法使用提供的认证信息登录。", '==', text)
        else:
            text = page.get_text(page.user_name)
            assert_compare(mobile, '==', text)
            with allure.step("登录成功需退出不影响后续操作"):
                page.click(page.logout)
        # 清除数据到初始页面
        page.get_url(r'http://meikefresh.5istudy.online/')

    @allure.title("新增用户收货地址")
    def test_add_address(self, driver_project):
        page = UserPage(driver_project)
        info = read_yaml()['user_address']
        page.login()
        page.move_to_element(page.vip_center)
        page.click(page.my_address)
        page.select_by_value(page.province, info['province'])
        page.select_by_value(page.city, info['city'])
        page.select_by_value(page.district, info['district'])
        page.send_keys(page.username, info['username'])
        page.send_keys(page.address, info['useraddress'])
        page.send_keys(page.mobile, info['mobile'])
        page.click(page.add_address_button)
        text = page.popup_window_operation(get_window_info=True)
        assert_compare("添加成功", "==", text)
        page.popup_window_operation()
        confirm = page.get_text(page.confirm)
        assert_compare("确定修改", "==", confirm)
        # nodes = page.find_elements(page.express_area)
        # assert_compare(2, '==', len(nodes))
        #清除添加的地址
        poptext=page.delete_first_address()
        assert_compare("删除成功", "==", poptext)
        with allure.step("退出"):
            page.click(page.logout)
        page.get_url(r'http://meikefresh.5istudy.online/')












