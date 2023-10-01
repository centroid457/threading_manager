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

    UUID: UUID = Field(default_factory=uuid4)

    INSTANCE: threading.Thread
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = {}
    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def __hash__(self):
        print(f"{hash(self.UUID)=}")
        return hash(self.UUID)

    def is_alive(self) -> Optional[bool]:
        return self.INSTANCE.is_alive()


# =====================================================================================================================
class ThreadsManager:
    _threads: Set[ThreadItem] = set()

    def decorator__thread_new(self, func):
        def func__apply_result_to_manager(*args, **kwargs):
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as exx:
                msg = f"{exx!r}"
                print(msg)
            #     self._thread__apply_exx(exx)
            # self._thread__apply_result(result)
            return result

        def wrapper(*args, **kwargs):
            instance = threading.Thread(target=func__apply_result_to_manager, args=args, kwargs=kwargs)
            thread_item = ThreadItem(INSTANCE=instance)
            thread_item.args = args
            thread_item.kwargs = kwargs

            ident = instance.ident

            self.__class__._threads.add(thread_item)
            instance.start()

        return wrapper

    # def _thread__apply_exx(self, exx: Exception) -> None:
    #     self.thread_item_current_get().exx = exx
    #
    # def _thread__apply_result(self, result: Any) -> None:
    #     self.thread_item_current_get().result = result
    #
    # def thread_item_current_get(self) -> ThreadItem:
    #     current_ident = threading.current_thread().ident
    #     return list(filter(lambda item: item.INSTANCE.ident == current_ident, self.__class__._threads))[0]

    @classmethod
    def threads_wait_all(cls):
        time.sleep(1)   # wait all started

        for item in cls._threads:
            item.INSTANCE.join()


# =====================================================================================================================
