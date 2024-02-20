from utils.log_util import logger

# F:\study\coding\po_shopping\testcases\user_center\test_user.py
# F:\study\coding\po_shopping\testcases\conftest.py
def assert_compare(expect, compare, actual):
    """

    :param expect: 预期结果
    :param compare: 断言方式
    :param actual: 实际结果
    :return:
    """
    logger.info(f"预期结果:{expect} {compare} {actual}")
    try:
        if compare == "==":
            assert expect == actual
        elif compare == "!=":
            assert expect != actual
        elif compare == ">":
            assert expect > actual
        elif compare == "<":
            assert expect < actual
        elif compare == "in":
            assert expect in actual
        else:
            try:
                raise NameError(f"{compare} 断言方式错误，请填写正确")
            except Exception as e:
                logger.error(e)
                raise
        logger.info("断言成功")
    except AssertionError as e:
        logger.error(f"断言失败{e}")
        raise
