from typing import *
import time

from PyQt5.QtCore import QThread
from singleton_meta import *


# =====================================================================================================================
# ISSUES ==============================================================================================================
# TODOs ---------------------------------------------------------------------------------------------------------------
# TODO: add GROUP threads - in decorator+wait+...
# TODO: maybe AUTO CLEAR if decorator get new funcName?
# TODO: add KILL/STOP! switch to Qthread?
# TODO: TIME item+group
# TODO: SECOND start7 - restart or even always generate new thread instance?

# READY ---------------------------------------------------------------------------------------------------------------
# 1=SINGLETON


# =====================================================================================================================
class ThreadItem(QThread):
    """Object for keeping thread data for better managing.

    :param args: args passed into thread target,
    :param kwargs: kwargs passed into thread target,
    :param result: value from target return, None when thread is_alive or raised,
    :param exx: exception object (if raised) or None
    """
    result: Optional[Any] = None
    exx: Optional[Exception] = None

    def __init__(self, target: Callable, t_args, t_kwargs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target: Callable = target
        self.args: Tuple[Any, ...] = t_args or ()
        self.kwargs: Dict[str, Any] = t_kwargs or {}

    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception as exx:
            msg = f"{exx!r}"
            print(msg)
            self.exx = exx

    def SLOTS_EXAMPLES(self):
        # checkers --------------------
        self.started
        self.isRunning()

        self.finished
        self.isFinished()

        self.destroyed
        self.signalsBlocked()

        # settings --------------------
        self.setTerminationEnabled()

        # info --------------------
        self.currentThread()
        self.currentThreadId()
        self.priority()
        self.loopLevel()
        self.stackSize()

        self.setPriority()
        self.setProperty()
        self.setObjectName()

        self.tr()

        # CONTROL --------------------
        self.run()
        self.start()
        self.startTimer()

        self.sleep(100)
        self.msleep(100)
        self.usleep(100)

        self.wait()

        self.disconnect()
        self.deleteLater()
        self.terminate()
        self.quit()
        self.exit(100)

        # WTF --------------------
        self.thread()


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

    :ivar _PARAM__NOTHREAD: parameter for passing in decorated function which can run target without thread

    :param args: NAME for manager instance
    :param thread_items: ThreadItem instances,
    :param MUTEX: mutex for safe collecting threads in this manager, creates in init
    :param counter: counter for collected threads in this manager
    """
    THREADS: List[ThreadItem]
    _PARAM__NOTHREAD: str = "nothread"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.THREADS = []

    @property
    def NAME(self) -> str:
        """classname for manager
        """
        return self.__class__.__name__

    @property
    def count(self) -> int:
        return len(self.THREADS)

    # =================================================================================================================
    def decorator__to_thread(self, _func) -> Callable:
        """Decorator which start thread from funcs and methods.

        always collect objects threads in result object! even if nothread! so you can get results from group!

        :param _func: decorated target
        """
        def _wrapper__spawn_thread(*args, **kwargs) -> Optional[Any]:
            """actual wrapper which spawn thread from decorated target.

            :param args: args passed into target/method,
            :param kwargs: kwargs passed into target/method,
            """
            nothread = self._PARAM__NOTHREAD in kwargs and kwargs.pop(self._PARAM__NOTHREAD)

            thread_item = ThreadItem(target=_func, t_args=args, t_kwargs=kwargs)
            self.THREADS.append(thread_item)
            thread_item.start()

            if nothread:
                thread_item.wait()
                return thread_item.result

        return _wrapper__spawn_thread

    # =================================================================================================================
    def thread_items__clear(self) -> None:
        """clear collected thread_items.

        useful if you dont need collected items any more after some step. and need to manage new portion.
        """
        self.THREADS.clear()

    def wait_all(self) -> None:
        """wait while all spawned threads finished.
        """
        for _ in range(3):
            if not self.count:
                time.sleep(1)   # wait all started

            for item in self.THREADS:
                item.wait()

            time.sleep(0.1)

    def check_results_all(self, value: Any = True, func_validate: Callable[[Any], bool] = None) -> bool:
        """check if result values for all threads are equal to the value

        :param value: expected comparing value for all thread results
        :param func_validate:
        """
        for thread in self.THREADS:
            if func_validate is not None:
                if not func_validate(thread.result):
                    return False
            else:
                if thread.result != value:
                    return False
        return True


# =====================================================================================================================
