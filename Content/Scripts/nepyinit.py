# -*- encoding: utf-8 -*-
import sys
import os
import ue
import traceback

def on_init():
	ue.LogWarning('hello, nepy!')		
	if ue.GIsEditor:		
		try:
			import reload_monitor
			reload_monitor.start()
		except:
			traceback.print_exc()
		try:
			import gmcmds
			gmcmds.debug()
		except:
			traceback.print_exc()
	
	# 导入游戏模块
	try:
		import character # noqa
		import rifle # noqa
		import bullet # noqa
		import magic_arrow # noqa
		import ai_enemy
		ue.LogWarning('Game modules imported successfully!')
	except Exception as e:
		ue.LogWarning(f'Error importing game modules: {e}')
		traceback.print_exc()

def on_shutdown():
	ue.LogWarning('bye, nepy!')

def on_debug_input(cmd_str):
	import gmcmds
	return gmcmds.handle_debug_input(cmd_str)

def on_tick(dt):
	pass