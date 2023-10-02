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

        assert ThreadManager1().COUNTER == 0
        assert ThreadManager2().COUNTER == 0

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

        assert ThreadManager1().COUNTER == count
        assert ThreadManager2().COUNTER == 0

        for i in range(count):
            assert func2(i) is None

        assert ThreadManager1().COUNTER == count
        assert ThreadManager2().COUNTER == count

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

        assert ThreadManager1().COUNTER == count
        ThreadManager1().wait_all()
        assert {item.result for item in ThreadManager1().THREAD_ITEMS} == {num * 1000 for num in range(count)}

        ThreadManager1().thread_items__clear()

        # spawn ------------------
        for i in range(count):
            assert Cls().func1(i) is None

        assert ThreadManager1().COUNTER == count
        ThreadManager1().wait_all()
        assert {item.result for item in ThreadManager1().THREAD_ITEMS} == {num * 1000 for num in range(count)}


# =====================================================================================================================
