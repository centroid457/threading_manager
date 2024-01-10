# DON'T DELETE!
# useful to start smth without pytest and not to run in main script!

import time

from object_info import ObjectInfo

from threading_manager import *


def target(value):
    time.sleep(value)
    return value


victim = ThreadItem(target=target, args=0.5)

ObjectInfo(victim).print()
victim.start()
ObjectInfo(victim).print()
