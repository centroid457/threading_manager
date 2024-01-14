# threading_manager (v0.0.8)

## DESCRIPTION_SHORT
Manage spawned threads

## DESCRIPTION_LONG
designed to working with spawned threads


## Features
1. use different managers for different funcs/methods if needed  
2. use just one decorator to spawn threads from func / methods  
3. keep all spawned threads in list by ThreadItem objects  
4. ThreadItem keeps result/exx/is_alive attributes!  
5. use wait_all()  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install threading-manager
```


## Import
```python
from threading_manager import *
```


********************************************************************************
## USAGE EXAMPLES
See tests and sourcecode for other examples.

------------------------------
### 1. example1.py
```python
from threading_manager import *

count = 5
time_start = time.time()


# define victim ------------------
class ThreadManager1(ThreadsManager):
    pass


class Cls:
    @ThreadManager1().decorator__to_thread
    def func1(self, num):
        time.sleep(1)
        return num * 1000


# spawn ------------------
for i in range(count):
    assert Cls().func1(i) is None

assert ThreadManager1().count == count
ThreadManager1().wait_all()
assert {item.result for item in ThreadManager1().THREADS} == {num * 1000 for num in range(count)}

ThreadManager1().clear()

# spawn ------------------
for i in range(count):
    assert Cls().func1(i) is None
```

********************************************************************************
