import datetime
import time

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.log_util import logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)  # 隐式等待
        self.wait = WebDriverWait(self.driver, 10)  # 显示等待
        self.actions = ActionChains(self.driver)  # 鼠标动作链初始化

    # 这是基础的find_element封装
    # def find_element(self, locator):
    #     logger.info(f"当前定位{locator}")
    #     return self.driver.find_element(*locator)

    def find_element(self, locator, condition='visibility', retry=1):
        """

        :param locator: 元素定位信息
        :param condition: 默认是visibility
        :param retry: 重试次数，默认是1，重试一次
        :return:
        """
        for time in range(retry + 1):
            try:
                logger.info(f"定位元素{locator}")
                if condition == 'visibility':
                    node = self.wait.until(EC.visibility_of_element_located(locator))
                else:
                    node = self.wait.until(EC.presence_of_element_located(locator))
                return node
            except Exception as e:
                error_info = f"{locator}定位失败，错误信息{e}"
                logger.error(error_info)
                if time < retry:
                    logger.info(f"正在重新定位，当前重试次数:{time + 1}")
                else:
                    raise Exception(error_info)

    def find_elements(self, locator, retry=1):
        """
        返回列表节点
        :param locator: 元素定位信息
        :param retry: 重试次数，默认是1，重试一次
        :return:
        """
        for time in range(retry + 1):
            try:
                logger.info(f"定位元素{locator}")
                node = self.wait.until(lambda x: x.find_elements(*locator))
                return node
            except Exception as e:
                error_info = f"{locator}定位失败，错误信息{e}"
                logger.error(error_info)
                if time < retry:
                    logger.info(f"正在重新定位，当前重试次数:{time + 1}")
                else:
                    raise Exception(error_info)

    def send_keys(self, locator, value, enter=False):
        """
        封装输入内容函数
        :param locator: 元素定位信息
        :param value: 输入项的内容
        :return:
        """
        # 1. 先定位元素
        node = self.find_element(locator)
        # 2. 清空输入框
        node.clear()
        # 3. 输入内容
        node.send_keys(value)
        logger.info(f"输入内容为：{value}")
        if enter:
            # 调用键盘的回车键
            node.send_keys(Keys.ENTER)
            logger.info("点击回车键")

    def click(self, locator):
        """
        定位元素并点击
        :param locator: 元素定位信息
        :return:
        """
        # 1. 先定位元素
        node = self.find_element(locator)
        # 2. 点击
        node.click()
        logger.info("点击按钮")

    def get_url(self, url=''):
        """
        请求url
        :param url: 网址
        :return:
        """
        self.driver.get(url)
        logger.info(f"打开网址{url}")

    def close_driver(self):
        """
        关闭浏览器
        :return:
        """
        logger.info("关闭浏览器")
        self.driver.close()

    def quit_driver(self):
        """
        退出浏览器
        :return:
        """
        logger.info("退出浏览器")
        self.driver.quit()

    def refresh(self):
        """
        刷新浏览器
        :return:
        """
        self.driver.refresh()
        logger.info("刷新浏览器")

    def switch_to_window(self, to_parent_window=False):
        """
        切换窗口
        :param to_parent_window: 是否回到主窗口
        :return:
        """
        total = self.driver.window_handles
        if to_parent_window:
            # 切换到主窗口
            self.driver.switch_to.window(total[0])
        else:
            # 获取当前窗口
            current_window = self.driver.current_window_handle
            for window in total:
                if window != current_window:
                    logger.info("切换窗口")
                    self.driver.switch_to.window(window)

    def get_title(self):
        """
        获取网页title
        :return:
        """
        return self.driver.title

    def get_current_url(self):
        """
        获取当前的URL
        :return:
        """
        return self.driver.current_url

    def get_page_source(self):
        """
        获取网页源代码
        :return:
        """
        return self.driver.page_source

    def get_text(self, locator):
        """
        获取元素的文本内容
        :param locator: 元素定位信息
        :return:
        """
        ele = self.find_element(locator)
        text = ele.text
        if text == "":
            text = ele.accessible_name
        logger.info(f"元素{locator}的text为{text}")
        return text

    def move_to_element(self, locator):
        """
        鼠标移动到指定位置
        :param locator: 指定位置
        :return:
        """
        ele = self.find_element(locator)
        self.actions.move_to_element(ele).perform()
        logger.info(f"鼠标移动到{locator}位置")

    def drag_and_drop(self, locator_start, locator_end):
        """
        鼠标拖动元素到另一个元素
        :param locator_start: 元素开始位置
        :param locator_end: 元素结束位置
        :return:
        """
        start = self.find_element(locator_start)
        end = self.find_element(locator_end)
        self.actions.drag_and_drop(start, end).perform()
        logger.info(f"鼠标从{locator_start}拖动到{locator_end}")

    def drag_and_drop_by_offset(self, locator, x, y):
        """
        拖动一段距离
        :param locator: 拖动的元素
        :param x: x距离
        :param y: y距离
        :return:
        """
        ele = self.find_element(locator)
        self.actions.drag_and_drop_by_offset(ele, x, y)
        logger.info("鼠标拖动一段距离")

    def select_by_index(self, locator, index):
        """
        根据下标获取select
        :param locator: 元素定位信息
        :param index: 下标，从0开始
        :return:
        """
        ele = self.find_element(locator)
        select = Select(ele)
        select.select_by_index(index)
        logger.info(f"根据下表{index}获取select")

    def select_by_value(self, locator, value):
        """
        根据value值获取select
        :param locator: 元素定位信息
        :param value: value值
        :return:
        """
        ele = self.find_element(locator)
        select = Select(ele)
        select.select_by_value(value)
        logger.info(f"根据下表{value}获取select")

    def select_by_visible_text(self, locator, visible_text):
        """
        根据visible_text值获取select
        :param locator: 元素定位信息
        :param visible_text: visible_text值
        :return:
        """
        ele = self.find_element(locator)
        select = Select(ele)
        select.select_by_visible_text(visible_text)
        logger.info(f"根据下表{visible_text}获取select")

    # 等待元素存在
    def wait_ele_presence(self, locator, center=True):
        """     知识点解析：
        #scrollIntoView:
                # 如果为true，元素的顶端将和其所在滚动区的可视区域的顶端对齐。
                # 如果为false，元素的底端将和其所在滚动区的可视区域的底端对齐。
        #scrollIntoViewIfNeeded:
                #如果为true，则元素将在其所在滚动区的可视区域中居中对其。
                # 如果为false，则元素将与其所在滚动区的可视区域最近的边缘对齐。 根据可见区域最靠近元素的哪个边缘，
                # 元素的顶部将与可见区域的顶部边缘对准，或者元素的底部边缘将与可见区域的底部边缘对准。"""
        try:
            start = datetime.datetime.now()
            ele = self.wait.until(EC.presence_of_element_located(locator))
            end = datetime.datetime.now()
            logger.info("元素{}已存在，等待{}秒".format(locator, (end - start).seconds))
            self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded(arguments[1]);", ele, center)
            return ele
        except Exception:
            logger.error("元素不存在-{}".format(locator))
            raise

    def execute_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def switch_to_frame(self, index=0, to_parent_frame=False, to_default_frame=False):
        """
        切换到不同的frame框架
        :param index: expect by frame index value or id or name or element
        :param to_parent_frame: 是否切换到上一个frame，默认False
        :param to_default_frame: 是否切换到最上层的frame，默认False
        :return:
        """
        if to_parent_frame:
            self.driver.switch_to.parent_frame()
        elif to_default_frame:
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(index)
        logger.info(f'切换frame，to：{index}')

    def popup_window_operation(self, action='yes', send_info='', get_window_info=False):
        """
        弹窗操作
        :param action: 要执行的动作，yes or no
        :param send_info: 在弹窗的文本框内输入信息
        :param get_window_info: 获取弹窗的文本信息
        :return:
        """
        if self.wait.until(EC.alert_is_present()):
            if send_info:
                logger.info(f'在弹窗上输入信息：{send_info}')
                self.driver.switch_to.alert.send_keys(send_info)

            if get_window_info:
                popup_info = self.driver.switch_to.alert.text
                logger.info(f'获取弹窗的文本信息：{popup_info}')
                return popup_info

            if action == 'yes':
                logger.info('在弹窗上点击确认')
                self.driver.switch_to.alert.accept()  # 点击确认
            else:
                logger.info('在弹窗上点击取消')
                self.driver.switch_to.alert.dismiss()  # 点击取消

    def page_scrolling(self, go_to_bottom=False, rolling_distance=(0, 1000)):
        """
        页面滚动，如果没有滚动效果，添加延时（页面需要全部加载完毕才能滚动）
        :param bool go_to_bottom: 是否直接滚动到当前页面的最底部，默认False
        :param tuple rolling_distance: 滚动距离，默认是向下滚动1000像素
        :return:
        """
        if go_to_bottom:
            js = "window.scrollTo(0, document.body.scrollHeight)"
        else:
            js = "window.scrollBy({}, {})".format(rolling_distance[0], rolling_distance[1])
        self.driver.execute_script(js)
        logger.debug(f'页面滚动完毕')

    def back(self):
        """网页后退"""
        self.driver.back()
        logger.debug('网页后退')

    def forward(self):
        """网页前进"""
        self.driver.forward()
        logger.debug('网页前进')

    # 获取元素的属性
    def get_ele_attribute(self, locator, name, center=True):
        ele = self.wait_ele_presence(locator, center)
        try:
            value = ele.get_attribute(name)
            logger.info("元素{}的{}属性-{}".format(locator, name, value))
            return value
        except:
            logger.error("元素获取属性{}失败-{}".format(name, locator))
            raise
