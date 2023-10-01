import pathlib
from typing import *
import time
import threading
from uuid import uuid4
from pydantic import BaseModel, Field


# =====================================================================================================================
Type_Dict = Dict[str, Optional[str]]
Type_Path = Union[str, pathlib.Path]
Type_Value = Union[str, NoReturn, None]


# =====================================================================================================================
class ThreadItem(BaseModel):
    ID: str = Field(default_factory=lambda: uuid4().hex)
    INSTANCE: threading.Thread = None
    info: Any = None
    result: Optional[Any] = None
    exx: Optional[Exception] = None

    @property
    def alive(self) -> bool:
        return self.INSTANCE.is_alive()


# =====================================================================================================================
class ThreadsManager:
    _threads: Set[ThreadItem] = {}

    def decorator__thread_new(self, func: Callable):
        thread_item = ThreadItem()
        self.__class__._threads.update({thread_item})

        def func__apply_result_to_manager(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as exx:
                msg = f"{exx!r}"
                print(msg)
                thread_item.exx = exx
                result = exx
            thread_item.result = result
            return result

        def wrapper(*args, **kwargs):
            instance = threading.Thread(target=func__apply_result_to_manager, args=args, kwargs=kwargs)
            thread_item.INSTANCE = instance
            instance.start()

        return wrapper

    @classmethod
    def threads_wait_all(cls):
        time.sleep(1)   # wait all started

        for item in cls._threads:
            item.join()


# =====================================================================================================================
