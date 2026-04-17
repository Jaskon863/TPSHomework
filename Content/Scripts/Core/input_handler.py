"""
输入处理系统
统一管理所有输入事件的处理和分发
"""

import unreal_engine as ue


class InputHandler:
    """
    输入处理器
    负责接收和分发所有输入事件到相应的系统
    """
    
    def __init__(self, player_controller):
        """
        初始化输入处理器
        
        Args:
            player_controller: 玩家控制器实例
        """
        self.player_controller = player_controller
        
        # 引用各个子系统
        self.character = None
        self.camera = None
        self.weapon = None
        
        # 输入映射配置
        self.input_enabled = True
        
        ue.log("InputHandler initialized")
    
    def set_character(self, character):
        """设置角色控制器引用"""
        self.character = character
    
    def set_camera(self, camera):
        """设置摄像机控制器引用"""
        self.camera = camera
    
    def set_weapon(self, weapon):
        """设置武器系统引用"""
        self.weapon = weapon
    
    def enable_input(self):
        """启用输入"""
        self.input_enabled = True
        ue.log("Input enabled")
    
    def disable_input(self):
        """禁用输入"""
        self.input_enabled = False
        ue.log("Input disabled")
    
    # ========== 移动输入 ==========
    
    def on_move_forward(self, axis_value):
        """前后移动输入"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_move_forward(axis_value)
    
    def on_move_right(self, axis_value):
        """左右移动输入"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_move_right(axis_value)
    
    def on_jump_pressed(self):
        """跳跃按下"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_jump()
    
    def on_jump_released(self):
        """跳跃释放"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_jump_released()
    
    def on_sprint_pressed(self):
        """冲刺按下"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_sprint_start()
    
    def on_sprint_released(self):
        """冲刺释放"""
        if not self.input_enabled or not self.character:
            return
        
        self.character.handle_sprint_stop()
    
    # ========== 摄像机输入 ==========
    
    def on_look_up(self, axis_value):
        """向上/向下看"""
        if not self.input_enabled or not self.camera:
            return
        
        self.camera.handle_look_up(axis_value)
    
    def on_turn(self, axis_value):
        """左右转向"""
        if not self.input_enabled or not self.camera:
            return
        
        self.camera.handle_turn(axis_value)
    
    def on_zoom_in(self):
        """拉近摄像机"""
        if not self.input_enabled or not self.camera:
            return
        
        self.camera.zoom_in()
    
    def on_zoom_out(self):
        """拉远摄像机"""
        if not self.input_enabled or not self.camera:
            return
        
        self.camera.zoom_out()
    
    # ========== 武器输入 ==========
    
    def on_fire_pressed(self):
        """开火按下（鼠标左键）"""
        if not self.input_enabled or not self.weapon:
            return
        
        self.weapon.start_fire()
    
    def on_fire_released(self):
        """开火释放"""
        if not self.input_enabled or not self.weapon:
            return
        
        self.weapon.stop_fire()
    
    def on_magic_arrow_pressed(self):
        """魔法箭按下（鼠标右键）"""
        if not self.input_enabled or not self.weapon:
            return
        
        self.weapon.fire_magic_arrow()
    
    def on_reload_pressed(self):
        """换弹按下（R键）"""
        if not self.input_enabled or not self.weapon:
            return
        
        self.weapon.reload()
    
    def on_toggle_fire_mode(self):
        """切换射击模式"""
        if not self.input_enabled or not self.weapon:
            return
        
        self.weapon.toggle_fire_mode()
    
    # ========== 其他输入 ==========
    
    def on_interact_pressed(self):
        """交互按键（E键）- 用于拾取道具等"""
        if not self.input_enabled:
            return
        
        # TODO: 实现交互逻辑
        ue.log("Interact pressed")
    
    def on_pause_pressed(self):
        """暂停按键（ESC键）"""
        # 暂停不受input_enabled限制
        ue.log("Pause pressed")
        # TODO: 显示暂停菜单
    
    def cleanup(self):
        """清理资源"""
        self.player_controller = None
        self.character = None
        self.camera = None
        self.weapon = None
        ue.log("InputHandler cleaned up")
