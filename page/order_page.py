from selenium.webdriver.common.by import By

from base.base_page import BasePage


class OrderPage(BasePage):
    # 首页商品
    first_good = (By.CSS_SELECTOR, '.newgoods_fastbuy>li>div>a')
    # 点击加入购物车
    add_shopping_cart = (By.ID, 'buy_btn')
    # 点击去结算
    go_pay = (By.XPATH, '//*[@id="cart_show"]/div[2]/a[2]')
    # 选择地址
    select_address = (By.XPATH, '//p[contains(text(),"配送地址")]/following-sibling::ul/li[2]')
    # 选择支付方式
    select_alipay = (By.XPATH, '//p[contains(text(),"支付方式")]/following-sibling::p/img')
    # 留言
    input_message = (By.XPATH, '//*[@id="cart-box"]/div[3]/textarea')
    # 去结算
    submit_order = (By.XPATH, '//*[@id="cart-box"]/div[3]/p/a')
    # 创建订单商品
    order_good = (By.XPATH, '//*[@id="cart-box"]/div[2]/ul/li')



