"""Remote Debug Functionality Module.

In Python based lambda serverless applications
we need to manually set some
functionalities like debugging.

"""
import os

from loguru import logger


def set_remote_debug() -> bool:
    """Set Python Remote Debug for Pycharm.

    Pycharm Instructions
    ====================
    https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html#remote-debug-config

    VSCode Instructions
    ===================
    https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-debugging-python.html

    VSCode example
    ==============
    >>>try:
    >>>     import ptvsd

    >>>     ptvsd.enable_attach(address=('0.0.0.0', 5890), redirect_output=True)
    >>>     ptvsd.wait_for_attach()
    >>>     logger.info(f"VSCode Python Debug available.")
    >>> except Exception as e:
    >>>     logger.warning(f"VSCode Python Debug not available.")

    This function will run only when serverless offline are invoked.

    :return: Boolean
    """
    if os.getenv("IS_LOCAL", False):
        return False

    # noinspection PyBroadException
    try:
        import pydevd_pycharm

        pydevd_pycharm.settrace(
            "0.0.0.0", port=58100, stdoutToServer=True, stderrToServer=True
        )
        logger.info(f"PyCharm Python Debug available.")
        return True
    except Exception:
        logger.warning(f"PyCharm Python Debug not available.")
        return False
