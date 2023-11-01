import os
import time
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser

from threading_manager import *


# =====================================================================================================================
class Test:
    # VICTIM: Type[ThreadsManager] = type("VICTIM", (ThreadsManager,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__noClass_severalManagers(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        class ThreadManager2(ThreadsManager):
            pass

        inst1 = ThreadManager1()
        inst2 = ThreadManager2()
        assert id(inst1) != id(inst2)
        assert ThreadManager1() != ThreadManager2()
        assert ThreadManager1() is not ThreadManager2()

        assert ThreadManager1().count == 0
        assert ThreadManager2().count == 0

        @ThreadManager1().decorator__to_thread
        def func1(num):
            time.sleep(1)
            return num * 10

        @ThreadManager2().decorator__to_thread
        def func2(num):
            time.sleep(1)
            return num * 100

        # spawn ------------------
        for i in range(count):
            assert func1(i) is None

        assert ThreadManager1().count == count
        assert ThreadManager2().count == 0

        for i in range(count):
            assert func2(i) is None

        assert ThreadManager1().count == count
        assert ThreadManager2().count == count

        # wait ------------------
        ThreadManager1().wait_all()
        ThreadManager2().wait_all()

        # checks ------------------
        for item in ThreadManager1().THREAD_ITEMS:
            assert item.is_alive() is False

        assert time.time() - time_start < 5

        assert {item.result for item in ThreadManager1().THREAD_ITEMS} == {num * 10 for num in range(count)}
        assert {item.result for item in ThreadManager2().THREAD_ITEMS} == {num * 100 for num in range(count)}

    def test__Class(self):
        # settings ------------------
        count = 5
        time_start = time.time()

        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        class Cls:
            @ThreadManager1().decorator__to_thread
            def func1(self, num):
                time.sleep(1)
                return num * 1000

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadManager1().count == count
        ThreadManager1().wait_all()
        assert {item.result for item in ThreadManager1().THREAD_ITEMS} == {num * 1000 for num in range(count)}

        ThreadManager1().thread_items__clear()

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadManager1().count == count
        ThreadManager1().wait_all()
        assert {item.result for item in ThreadManager1().THREAD_ITEMS} == {num * 1000 for num in range(count)}

    def test__check_results_all(self):
        # define victim ------------------
        class ThreadManager1(ThreadsManager):
            pass

        @ThreadManager1().decorator__to_thread
        def func1(value):
            return value

        # bool ----------
        ThreadManager1().thread_items__clear()
        [func1(True), func1(True)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all() is True

        ThreadManager1().thread_items__clear()
        [func1(True), func1(False)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all() is False

        ThreadManager1().thread_items__clear()
        [func1(False), func1(False)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(False) is True

        # int ----------
        ThreadManager1().thread_items__clear()
        [func1(1), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(1) is True

        ThreadManager1().thread_items__clear()
        [func1(1), func1(2)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(1) is False

        # func_validate ----------
        ThreadManager1().thread_items__clear()
        [func1(0), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=bool) is False

        ThreadManager1().thread_items__clear()
        [func1(1), func1(2)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=bool) is True

        def validate_int(obj: Any) -> bool:
            return isinstance(obj, int)

        ThreadManager1().thread_items__clear()
        [func1(0), func1(1)]
        ThreadManager1().wait_all()
        assert ThreadManager1().check_results_all(func_validate=validate_int) is True


# =====================================================================================================================
