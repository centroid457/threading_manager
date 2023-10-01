import pathlib
from typing import *
import time
import threading
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict, Field


# =====================================================================================================================


# =====================================================================================================================
class ThreadItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)     # just for Thread!

    INSTANCE: threading.Thread
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = {}
    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def is_alive(self) -> Optional[bool]:
        return self.INSTANCE.is_alive()


# =====================================================================================================================
class ThreadsManager:
    _threads: List[ThreadItem] = []
    _mutex: threading.Lock = None

    def __init__(self):
        super().__init__()
        self.__class__._mutex = threading.Lock()

    @classmethod
    def decorator__thread_new(cls, func):
        def func__apply_result_to_manager(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as exx:
                msg = f"{exx!r}"
                print(msg)
                cls._thread__apply_exx(exx)
            cls._thread__apply_result(result)
            return result

        def wrapper(*args, **kwargs):
            instance = threading.Thread(target=func__apply_result_to_manager, args=args, kwargs=kwargs)
            thread_item = ThreadItem(INSTANCE=instance)
            thread_item.args = args
            thread_item.kwargs = kwargs

            cls._mutex.acquire()
            cls._threads.append(thread_item)
            cls._mutex.release()

            instance.start()

        return wrapper

    @classmethod
    def _thread__apply_exx(cls, exx: Exception) -> None:
        cls.thread_item_current_get().exx = exx

    @classmethod
    def _thread__apply_result(cls, result: Any) -> None:
        cls.thread_item_current_get().result = result

    @classmethod
    def thread_item_current_get(cls) -> ThreadItem:
        current_ident = threading.current_thread().ident
        return list(filter(lambda item: item.INSTANCE.ident == current_ident, cls._threads))[0]

    @classmethod
    def threads_wait_all(cls):
        time.sleep(1)   # wait all started

        for item in cls._threads:
            item.INSTANCE.join()


# =====================================================================================================================
