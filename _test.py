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
    # @pytest.mark.skip
    # def test__noClass_oneManager(self):
    #     # settings ------------------
    #     count = 20
    #     time_start = time.time()
    #
    #     # define victim ------------------
    #     @ThreadsManager().decorator__to_thread
    #     def func(num):
    #         time.sleep(0.5)
    #         return num
    #
    #     # spawn ------------------
    #     for i in range(count):
    #         assert func(i) is None
    #
    #     # wait ------------------
    #     ThreadsManager().wait_all()
    #
    #     # checks ------------------
    #     for item in ThreadsManager().THREAD_ITEMS:
    #         assert item.is_alive() is False
    #
    #     assert time.time() - time_start < count/2
    #
    #     assert {item.result for item in ThreadsManager().THREAD_ITEMS} == {*range(count)}
    #
    #     # clear ------------------
    #     assert len(ThreadsManager().THREAD_ITEMS) == count
    #     assert ThreadsManager().COUNTER == count
    #     ThreadsManager().thread_items__clear()
    #     assert len(ThreadsManager().THREAD_ITEMS) == 0
    #     assert ThreadsManager().COUNTER == 0

    def test__noClass_severalManagers(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class Manager1(ThreadsManager):
            pass

        class Manager2(ThreadsManager):
            pass

        inst1 = Manager1()
        inst2 = Manager2()
        assert id(inst1) != id(inst2)
        assert Manager1() != Manager2()
        assert Manager1() is not Manager2()

        assert Manager1().COUNTER == 0
        assert Manager2().COUNTER == 0

        @Manager1().decorator__to_thread
        def func1(num):
            time.sleep(1)
            return num * 10

        @Manager2().decorator__to_thread
        def func2(num):
            time.sleep(1)
            return num * 100

        # spawn ------------------
        for i in range(count):
            assert func1(i) is None

        assert Manager1().COUNTER == count
        assert Manager2().COUNTER == 0

        for i in range(count):
            assert func2(i) is None

        assert Manager1().COUNTER == count
        assert Manager2().COUNTER == count

        # wait ------------------
        Manager1().wait_all()
        Manager2().wait_all()

        # checks ------------------
        for item in Manager1().THREAD_ITEMS:
            assert item.is_alive() is False

        assert time.time() - time_start < 5

        assert {item.result for item in Manager1().THREAD_ITEMS} == {num * 10 for num in range(count)}
        assert {item.result for item in Manager2().THREAD_ITEMS} == {num * 100 for num in range(count)}

    def test__multy(self):
        pass


# =====================================================================================================================

