import allure
from selenium.webdriver.common.by import By

from base.base_page import BasePage
# from testcases.user_center.conftest import delete_user, delete_code
from utils.assert_util import assert_compare
from utils.read import read_yaml


class UserPage(BasePage):
    # 请登录
    ple_login = (By.CSS_SELECTOR, 'a[href="#/app/login"]')
    # 会员中心
    vip_center = (By.XPATH, '//a[contains(text(),"会员中心")]')
    # 我的订单
    my_order = (By.CSS_SELECTOR, 'a[href="#/app/home/member/order"]')
    # 我的收藏
    my_fav = (By.CSS_SELECTOR, 'a[href="#/app/home/member/collection"]')
    # 我的收货地址
    my_address = (By.CSS_SELECTOR, 'a[href="#/app/home/member/receive"]')
    # 购物车
    shopping_cart = (By.CSS_SELECTOR, 'a[href="#/app/shoppingcart/cart"]')
    """注册功能"""
    # 免费注册
    register = (By.CSS_SELECTOR, 'a[href="#/app/register"]')
    # 手机号
    register_mobile = (By.ID, 'jsRegMobile')
    # 免费获取验证码
    send_code = (By.ID, 'jsSendCode')
    # 输入手机验证码
    input_code = (By.ID, 'jsPhoneRegCaptcha')
    # 输入密码
    input_password = (By.ID, 'jsPhoneRegPwd')
    # 注册并登录
    register_submit = (By.ID, 'jsMobileRegBtn')
    # 退出
    logout = (By.XPATH, '//*[@id="ECS_MEMBERZONE"]/a[2]')
    # 用户名
    user_name = (By.CSS_SELECTOR, 'a[href="#/app/home/member/userinfo"]')
    # 验证码错误
    error_code = (By.XPATH, '//*[@id="mobile_register_form"]/p[2]')
    # 用户已存在
    user_exist = (By.XPATH, '//*[@id="mobile_register_form"]/p[1]')
    """登录相关"""
    # 用 户 名
    login_account = (By.ID, 'account_l')
    # 密     码
    login_password = (By.ID, 'password_l')
    # 登录按钮
    login_btn = (By.ID, 'jsLoginBtn')
    # 登录用户名错误信息
    login_account_error = (By.XPATH, '//*[@id="jsLoginForm"]/p[1]')
    # 登录密码为空错误信息
    login_password_error = (By.XPATH, '//*[@id="jsLoginForm"]/p[2]')
    # 登录密码错误信息
    login_error = (By.XPATH, '//*[@id="jsLoginForm"]/p[3]')

    """我的地址"""
    # 配送区域
    express_area = (By.XPATH, '//td[contains(text(),"配送区域")]')
    # 省
    province = (By.XPATH, '//td[contains(text(),"配送区域")]/following-sibling::td/div/div/select[1]')
    # 市
    city = (By.XPATH, '//td[contains(text(),"配送区域")]/following-sibling::td/div/div/select[2]')
    # 区
    district = (By.XPATH, '//td[contains(text(),"配送区域")]/following-sibling::td/div/div/select[3]')
    # 收货人姓名
    username = (By.ID, 'consignee_0')
    # 详细地址
    address = (By.ID, 'address_0')
    # 手机
    mobile = (By.ID, 'mobile_0')
    # 新增收货地址按钮
    add_address_button = (By.XPATH, '//button[contains(text(),"新增收货地址")]')
    # 确定修改
    confirm = (By.XPATH, '//button[contains(text(),"确定修改")]')
    # 删除
    delete_address = (By.XPATH, '//button[contains(text(),"删除")]')

    def register_failed(self, data):
        """
        注册失败
        :return:
        """
        self.get_url("http://meikefresh.5istudy.online/")
        with allure.step("点击免费注册"):
            self.click(self.register)
        with allure.step("输入手机号"):
            self.send_keys(self.register_mobile, data['mobile'])
        with allure.step("点击获取验证码"):
            self.click(self.send_code)
        with allure.step("输入验证码"):
            self.send_keys(self.input_code, "f123")
        with allure.step("输入密码"):
            self.send_keys(self.input_password, data['password'])
        with allure.step("点击注册并登录"):
            self.click(self.register_submit)
        text = self.get_text(self.error_code)
        assert_compare("验证码错误", '==', text)
        # delete_user(data['mobile'])
        # delete_code(data['mobile'])

    def login(self):
        self.get_url("http://meikefresh.5istudy.online/#/app/login")
        self.send_keys(self.login_account, "13800001111")
        self.send_keys(self.login_password, "123456")
        self.click(self.login_btn)

    def delete_first_address(self):
        self.click(self.delete_address)
        poptext = self.popup_window_operation(get_window_info=True)
        self.popup_window_operation()
        return poptext

