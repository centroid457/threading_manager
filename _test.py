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
            time.sleep(2)
            return num

        # start all
        for i in range(10):
            assert func(i) is None

        for item in ThreadsManager._threads:
            assert item.is_alive() is False

        ThreadsManager.threads_wait_all()

        assert len(ThreadsManager._threads) == 10

        for item in ThreadsManager._threads:
            assert item.is_alive() is False

        assert set([item.result for item in ThreadsManager._threads]) == {*range(10)}


    def test__Class(self):
        class Cls(ThreadsManager):
            pass

        assert True

    def test__multy(self):
        assert True


# =====================================================================================================================
