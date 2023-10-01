import os
import time
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser

from threads_manager import *


# =====================================================================================================================
class Test:
    # VICTIM: Type[ThreadsManager] = type("VICTIM", (ThreadsManager,), {})

    # -----------------------------------------------------------------------------------------------------------------
    # @pytest.mark.xfail
    def test__noClass(self):
        @ThreadsManager().decorator__thread_new
        def func(num):
            time.sleep(1)
            return num

        for i in range(20):
            assert func(i) is None

        ThreadsManager.threads_wait_all()

        assert len(ThreadsManager._threads) == 20

        for item in ThreadsManager._threads:
            assert item.is_alive() is False

    def test__Class(self):
        pass

    def test__multy(self):
        pass


# =====================================================================================================================
