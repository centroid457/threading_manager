import time
import pip
from setuptools import find_packages


# TODO: use as main or additional CLI-USER???


pip.main(["install", "--upgrade", "pip"])

pip.main(["install", "-r", "requirements.txt"])
pip.main(["install", "-r", "requirements__AST.txt"])


for item in find_packages():
    print(item)
    pip.main(["install", "--upgrade", item])


# EXIT PAUSE ==========================================================================================================
# for i in range(10, 0, -1):
#     print(f"exit in [{i}] seconds")
#     time.sleep(1)

input("press Enter to close")


# =====================================================================================================================
