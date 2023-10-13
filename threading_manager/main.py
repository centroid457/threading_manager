from typing import *
import time
import threading
from pydantic import BaseModel, ConfigDict, Field

from singleton_meta import *


# =====================================================================================================================
# TODO: add Group threads - in decorator+wait+...


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
        """Check if thread in process state

        :return: bool
        """
        return self.INSTANCE.is_alive()


# =====================================================================================================================
class ThreadsManager(SingletonByCallMeta):
    """Manager for spawning threads and keep its instances with additional data.
    Singleton! do you dont need saving instances!

    USAGE
    -----
    1. BEST PRACTICE
    Not recommended using it directly, use as simple nested:
        class ThreadsManager1(ThreadsManager):
            pass

        @ThreadsManager1.decorator__to_thread
        def func(*args, **kwargs):
            pass

    2. Direct usage
    But if you need only one manager - do use directly.
        @ThreadsManager.decorator__to_thread
        def func(*args, **kwargs):
            pass

    :param name: NAME for manager instance
    :param thread_items: ThreadItem instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager
    """
    # THREAD_ITEMS: List[ThreadItem] = None
    # MUTEX_THREADS: threading.Lock = None
    # COUNTER: int = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.THREAD_ITEMS = []
        self.MUTEX_THREADS = threading.Lock()
        self.COUNTER = 0

    @property
    def NAME(self) -> str:
        """classname for manager
        """
        return self.__class__.__name__

    def thread_items__clear(self) -> None:
        """clear collected thread_items.

        useful if you dont need collected items any more after some step. and need to manage new portion.
        """
        self.THREAD_ITEMS.clear()
        self.COUNTER = 0

    def decorator__to_thread(self, _func) -> Callable:
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

            self.MUTEX_THREADS.acquire()
            self.COUNTER += 1
            self.THREAD_ITEMS.append(thread_item)
            self.MUTEX_THREADS.release()

            instance.start()

        return _wrapper__spawn_thread

    def _thread__apply_exx(self, exx: Exception) -> None:
        """save exx object from active thread into corresponding threadItem

        :param exx: raised Exception in thread
        """
        self._thread_item_current_get().exx = exx

    def _thread__apply_result(self, result: Any) -> None:
        """save result from active thread into corresponding threadItem

        :param result: raised Exception in thread
        """
        self._thread_item_current_get().result = result

    def _thread_item_current_get(self) -> ThreadItem:
        """Get corresponding threadItem in code for current thread
        """
        current_ident = threading.current_thread().ident
        return list(filter(lambda item: item.INSTANCE.ident == current_ident, self.THREAD_ITEMS))[0]

    def wait_all(self) -> None:
        """wait while all spawned threads finished.
        """
        for _ in range(3):
            if not self.COUNTER:
                time.sleep(1)   # wait all started

            for item in self.THREAD_ITEMS:
                item.INSTANCE.join()

            time.sleep(0.1)


# =====================================================================================================================
