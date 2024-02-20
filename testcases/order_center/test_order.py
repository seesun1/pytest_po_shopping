import allure
import pytest

from page.order_page import OrderPage
from page.user_page import UserPage
from utils.assert_util import assert_compare


@allure.epic("美客生鲜的项目")
@allure.feature("订单中心")
@pytest.mark.run(order=2)
class TestOrder:
    @allure.title("创建订单")
    def test_add_order(self, driver_project):

        user_page = UserPage(driver_project)
        order_page = OrderPage(driver_project)
        user_page.login()
        order_page.click(order_page.first_good)
        order_page.switch_to_window()
        order_page.click(order_page.add_shopping_cart)
        order_page.click(order_page.go_pay)
        order_page.wait_ele_presence(order_page.order_good)
        order_page.click(order_page.select_address)
        order_page.click(order_page.select_alipay)
        order_page.send_keys(order_page.input_message, "测试订单")
        order_page.click(order_page.submit_order)
        text = order_page.popup_window_operation(get_window_info=True)
        assert_compare("订单创建成功", "==", text)
        order_page.popup_window_operation()
        order_page.close_driver()
        order_page.switch_to_window(to_parent_window=True)
        # 清除，回到初始页面
        with allure.step("退出"):
            user_page.click(user_page.logout)
        user_page.get_url(r'http://meikefresh.5istudy.online/')
