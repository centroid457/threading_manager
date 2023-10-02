import pathlib
from typing import *
import time
import threading
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict, Field


# =====================================================================================================================


# =====================================================================================================================
class ThreadItem(BaseModel):
    """Object for keeping thread data for better managing.

    :param INSTANCE: thread instance,
    :param args: args passed into thread target,
    :param kwargs: kwargs passed into thread target,
    :param result: value from target return, None when thread is_alive or raised,
    :param exx: exception object (if raised) or None
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)     # just for Thread!

    INSTANCE: threading.Thread
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = {}

    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def is_alive(self) -> Optional[bool]:
        """Check thread in process state

        :return: bool
        """
        return self.INSTANCE.is_alive()


# =====================================================================================================================
class ThreadsManager:
    """Manager for spawning threads and keep its instances with additional data

    :param _thread_items: ThreadItem instances,
    :param _thread_mutex: mutex for safe collecting threads in this manager, creates in init
    """
    _thread_items: List[ThreadItem] = []
    _thread_mutex: threading.Lock = None

    def __init__(self):
        super().__init__()
        self._thread_mutex = threading.Lock()

    def decorator__thread_start_new(self, _func) -> Callable:
        """Decorator which start thread from funcs and methods.

        :param _func: decorated func
        """
        def func__apply_result_to_manager(*args, **kwargs) -> None:
            """internal func creates ability to save result/exx from original func into threadItem

            :param args: args passed into func/method,
            :param kwargs: kwargs passed into func/method,
            """
            result = None
            try:
                result = _func(*args, **kwargs)
            except Exception as exx:
                msg = f"{exx!r}"
                print(msg)
                self._thread__apply_exx(exx)
            self._thread__apply_result(result)

        def _wrapper__spawn_thread(*args, **kwargs) -> None:
            """actual wrapper which spawn thread from decorated func.

            :param args: args passed into func/method,
            :param kwargs: kwargs passed into func/method,
            """
            instance = threading.Thread(target=func__apply_result_to_manager, args=args, kwargs=kwargs)
            thread_item = ThreadItem(INSTANCE=instance)
            thread_item.args = args
            thread_item.kwargs = kwargs

            self._thread_mutex.acquire()
            self.__class__._thread_items.append(thread_item)
            self._thread_mutex.release()

            instance.start()

        return _wrapper__spawn_thread

    def _thread__apply_exx(self, exx: Exception) -> None:
        """save exx object from active thread into corresponding threadItem

        :param exx: raised Exception in thread
        """
        self.thread_item_current_get().exx = exx

    def _thread__apply_result(self, result: Any) -> None:
        """save result from active thread into corresponding threadItem

        :param result: raised Exception in thread
        """
        self.thread_item_current_get().result = result

    def thread_item_current_get(self) -> ThreadItem:
        """Get corresponding threadItem in code for current thread
        """
        current_ident = threading.current_thread().ident
        return filter(lambda item: item.INSTANCE.ident == current_ident, self.__class__._thread_items)[0]

    @classmethod
    def threads_wait_all(cls) -> None:
        """wait while all spawned threads finished
        """
        time.sleep(1)   # wait all started

        for item in cls._thread_items:
            item.INSTANCE.join()


# =====================================================================================================================
