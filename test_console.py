import random
import string

import os
def make_account():
    for i in range(50):
        ran_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
        print(ran_str + "=" + ran_str)


# make_account()
name = "finish_result/2_20210101155807_finish_game_1.png"
import Utils

Utils.convert_jepg(name)
cwd = os.path.join(os.path.abspath("."), "finish_result")
Utils.execute_command("delete_old.bat", cwd)
