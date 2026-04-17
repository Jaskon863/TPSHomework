# -*- encoding: utf-8 -*-
# 简化版 reloader - 使用 importlib.reload()
import sys
import os
import gc
import importlib
import inspect
import ue

FOR_TYPE_HINT = False
if FOR_TYPE_HINT:
    import typing


class ReloadRules(object):
    # 判断module是否能被reload
    def check_module_can_reload(self, module_name, module):
        # type: (str, typing.Any) -> bool
        if not inspect.ismodule(module):
            return False
        if module_name in sys.builtin_module_names:
            return False
        if not getattr(module, '__file__', None):
            return False
        if not hasattr(module, '__dict__'):
            return False
        module_file = module.__file__.replace('\\', '/')
        if '/Lib/' in module_file or '/debuglib/' in module_file:
            return False
        return True

RULES = ReloadRules()

# 上一次reload时间，用于增量reload
g_last_reload_time = 0

def init_last_reload_time():
    import time
    global g_last_reload_time
    g_last_reload_time = time.time()

# 简化版reload - 使用importlib.reload
def reload(module_names=None, modified_only=True):
    # type: (typing.List[str] | None, bool) -> None
    if module_names is None:
        module_names = list(sys.modules.keys())

    if modified_only:
        global g_last_reload_time
        last_reload_time = g_last_reload_time

    print('********** start reload script (importlib) ***************')

    gc_is_enabled = gc.isenabled()
    if gc_is_enabled:
        gc.disable()

    reload_module_names = []
    for module_name in module_names:
        module = sys.modules.get(module_name)
        if not RULES.check_module_can_reload(module_name, module):
            continue
        
        if modified_only:
            try:
                modify_time = os.stat(module.__file__).st_mtime
                py_file = os.path.splitext(module.__file__)[0] + '.py'
                if os.path.exists(py_file):
                    modify_time = max(modify_time, os.stat(py_file).st_mtime)
                if modify_time <= last_reload_time:
                    continue
                if modify_time > g_last_reload_time:
                    g_last_reload_time = modify_time
            except Exception as e:
                sys.stderr.write('check modify time failed: "%s"\n' % (e,))
                continue
        
        reload_module_names.append(module_name)

    # 使用 importlib.reload
    success_count = 0
    fail_count = 0
    
    try:
        for module_name in reload_module_names:
            try:
                module = sys.modules.get(module_name)
                if module:
                    print('reloading "%s" ...' % module_name)
                    importlib.reload(module)
                    success_count += 1
            except Exception as e:
                print('failed to reload "%s": %s' % (module_name, e))
                fail_count += 1
    except:
        if modified_only:
            g_last_reload_time = last_reload_time
        sys.excepthook(*sys.exc_info())

    # 刷新UE生成的类型
    try:
        ue.FlushGeneratedTypeReinstancing()
    except:
        pass

    if gc_is_enabled:
        gc.enable()
        gc.collect()

    print('********** reload finished: Success=%d, Failed=%d ***************' % (success_count, fail_count))
