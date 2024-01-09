from typing import *
import time
import threading
from pydantic import BaseModel, ConfigDict, Field

from singleton_meta import *


# =====================================================================================================================
# ISSUES ==============================================================================================================
# TODOs ---------------------------------------------------------------------------------------------------------------
# TODO: add GROUP threads - in decorator+wait+...
# TODO: maybe AUTO CLEAR if decorator get new funcName?
# TODO: add KILL/STOP! switch to Qthread?
# TODO: TIME item+group
# TODO: SECOND start - restart or even always generate new thread instance?

# READY ---------------------------------------------------------------------------------------------------------------
# 1=SINGLETON


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
    func: Callable = None
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

    :ivar PARAM__NOTHREAD: parameter for passing in decorated function which can run func without thread

    :param args: NAME for manager instance
    :param thread_items: ThreadItem instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager
    """
    THREAD_ITEMS: List[ThreadItem]
    # MUTEX_THREADS: threading.Lock = None
    PARAM__NOTHREAD: str = "nothread"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.THREAD_ITEMS = []
        self.MUTEX_THREADS = threading.Lock()

    @property
    def NAME(self) -> str:
        """classname for manager
        """
        return self.__class__.__name__

    @property
    def count(self) -> int:
        return len(self.THREAD_ITEMS)

    def thread_items__clear(self) -> None:
        """clear collected thread_items.

        useful if you dont need collected items any more after some step. and need to manage new portion.
        """
        self.THREAD_ITEMS.clear()

    def decorator__to_thread(self, _func) -> Callable:
        """Decorator which start thread from funcs and methods.

        always collect objects threads in result object! even if nothread! so you can get results from group!

        :param _func: decorated func
        """
        def _wrapper__spawn_thread(*args, **kwargs) -> Optional[Any]:
            """actual wrapper which spawn thread from decorated func.

            :param args: args passed into func/method,
            :param kwargs: kwargs passed into func/method,
            """
            nothread = self.PARAM__NOTHREAD in kwargs and kwargs.pop(self.PARAM__NOTHREAD)

            instance = threading.Thread(target=self._func_execution, kwargs={"func": _func, "args": args, "kwargs": kwargs})
            thread_item = ThreadItem(INSTANCE=instance)
            thread_item.func = _func
            thread_item.args = args
            thread_item.kwargs = kwargs

            self.MUTEX_THREADS.acquire()
            self.THREAD_ITEMS.append(thread_item)
            self.MUTEX_THREADS.release()

            instance.start()

            if nothread:
                instance.join()
                return thread_item.result

        return _wrapper__spawn_thread

    def _func_execution(self, func, args, kwargs) -> Optional[Any]:
        """save result/exx from original func into threadItem

        :param func: decorated func,
        :param args: args passed into func/method,
        :param kwargs: kwargs passed into func/method,
        """
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as exx:
            msg = f"{exx!r}"
            print(msg)
            self._thread__apply_exx(exx)
        self._thread__apply_result(result)
        return result

    def _thread__apply_exx(self, exx: Exception) -> None:
        """save exx object from active thread into corresponding threadItem

        :param exx: raised Exception in thread
        """
        try:
            self._thread_item__current_get().exx = exx
        except:
            pass

    def _thread__apply_result(self, result: Any) -> None:
        """save result from active thread into corresponding threadItem

        :param result: raised Exception in thread
        """
        try:
            self._thread_item__current_get().result = result
        except:
            pass

    def _thread_item__current_get(self) -> ThreadItem:
        """Get corresponding threadItem in code for current thread
        """
        current_ident = threading.current_thread().ident
        return list(filter(lambda item: item.INSTANCE.ident == current_ident, self.THREAD_ITEMS))[0]

    def wait_all(self) -> None:
        """wait while all spawned threads finished.
        """
        for _ in range(3):
            if not self.count:
                time.sleep(1)   # wait all started

            for item in self.THREAD_ITEMS:
                item.INSTANCE.join()

            time.sleep(0.1)

    def check_results_all(self, value: Any = True, func_validate: Callable[[Any], bool] = None) -> bool:
        """check if result values for all threads are equal to the value

        :param value: expected comparing value for all thread results
        :param func_validate:
        """
        for thread in self.THREAD_ITEMS:
            if func_validate is not None:
                if not func_validate(thread.result):
                    return False
            else:
                if thread.result != value:
                    return False
        return True


# =====================================================================================================================
