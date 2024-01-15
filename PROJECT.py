from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 1)

    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_INSTALL: str = "threading-manager"
    NAME_IMPORT: str = "threading_manager"
    KEYWORDS: List[str] = [
        "threading", "threads", "thread",
        "thread manager"
    ]

    # GIT --------------------------------------------------
    DESCRIPTION_SHORT: str = "manage spawned threads"

    # README -----------------------------------------------
    pass

    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_LONG: str = """
Designed to working with spawned threads

NOTE: maybe you dont need use it if you need only one class method - use direct QThread
"""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "use different managers for different funcs/methods if needed",
        "use just one decorator to spawn threads from func / methods",
        "keep all spawned threads in list by ThreadItem objects",
        "ThreadItem keeps result/exx/is_alive attributes!",
        "use wait_all()",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 0, 8)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "add SERIAL execution as method wait_all_piped! paired up with wait_all_parallel()",
        "add meta cumulative funks",
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "apply new pypi template"
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
