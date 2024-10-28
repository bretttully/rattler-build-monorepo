from nm_a.some_func import func_a


def func_c():
    print("func_c() in nm_c calling func_a()")
    func_a()
