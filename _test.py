import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser

from threads_manager import *


# =====================================================================================================================
class Test:
    VICTIM: Type[ThreadsManager] = type("VICTIM", (ThreadsManager,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__ClassMethod_and_obj(self):
        assert True


# =====================================================================================================================
