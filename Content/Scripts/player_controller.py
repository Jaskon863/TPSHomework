"""
玩家控制器主类
整合所有子系统，作为玩家控制的统一入口
"""

import unreal_engine as ue
from Core.character import PlayerCharacter
from Core.camera import CameraController
from Core.input_handler import InputHandler
from Gameplay.weapon_system import WeaponSystem
from Gameplay.health_component import HealthComponent


class PlayerController:
    """
    玩家控制器主类
    负责初始化和管理所有玩家相关的子系统
    """
    
    def __init__(self, character_actor):
        """
        初始化玩家控制器
        
        Args:
            character_actor: 玩家角色Actor引用
        """
        self.actor = character_actor
        
        # 初始化各个子系统
        self.character = PlayerCharacter(character_actor)
        self.camera = CameraController(character_actor)
        self.weapon = WeaponSystem(character_actor)
        self.health = HealthComponent(character_actor, max_health=100.0)
        self.input_handler = InputHandler(self)
        
        # 设置输入处理器的引用
        self.input_handler.set_character(self.character)
        self.input_handler.set_camera(self.camera)
        self.input_handler.set_weapon(self.weapon)
        
        # 设置健康组件的回调
        self.health.on_damage_callback = self.on_damage_received
        self.health.on_death_callback = self.on_death
        self.health.on_heal_callback = self.on_healed
        
        # 游戏状态
        self.is_active = True
        
        ue.log("=== PlayerController initialized ===")
        self._print_system_info()
    
    def _print_system_info(self):
        """打印系统信息"""
        ue.log(f"Character: {self.actor.get_name()}")
        ue.log(f"Health: {self.health.current_health}/{self.health.max_health}")
        ue.log(f"Weapon: {self.weapon.weapon_name}")
        ue.log(f"Ammo: {self.weapon.current_ammo}/{self.weapon.magazine_size}")
        ue.log("====================================")
    
    # ========== 输入绑定方法（从蓝图调用）==========
    
    def bind_move_forward(self, axis_value):
        """绑定前后移动"""
        self.input_handler.on_move_forward(axis_value)
    
    def bind_move_right(self, axis_value):
        """绑定左右移动"""
        self.input_handler.on_move_right(axis_value)
    
    def bind_jump_pressed(self):
        """绑定跳跃按下"""
        self.input_handler.on_jump_pressed()
    
    def bind_jump_released(self):
        """绑定跳跃释放"""
        self.input_handler.on_jump_released()
    
    def bind_look_up(self, axis_value):
        """绑定向上看"""
        self.input_handler.on_look_up(axis_value)
    
    def bind_turn(self, axis_value):
        """绑定转向"""
        self.input_handler.on_turn(axis_value)
    
    def bind_fire_pressed(self):
        """绑定开火按下"""
        self.input_handler.on_fire_pressed()
    
    def bind_fire_released(self):
        """绑定开火释放"""
        self.input_handler.on_fire_released()
    
    def bind_magic_arrow_pressed(self):
        """绑定魔法箭按下"""
        self.input_handler.on_magic_arrow_pressed()
    
    def bind_reload_pressed(self):
        """绑定换弹按下"""
        self.input_handler.on_reload_pressed()
    
    def bind_sprint_pressed(self):
        """绑定冲刺按下"""
        self.input_handler.on_sprint_pressed()
    
    def bind_sprint_released(self):
        """绑定冲刺释放"""
        self.input_handler.on_sprint_released()
    
    # ========== 游戏事件回调 ==========
    
    def on_damage_received(self, damage, attacker, damage_type):
        """
        受到伤害时的回调
        
        Args:
            damage: 伤害值
            attacker: 攻击者
            damage_type: 伤害类型
        """
        ue.log(f"Player received {damage} damage from {attacker}")
        
        # TODO: 更新UI显示血量
        # TODO: 播放受击音效
        # TODO: 触发屏幕抖动
        # TODO: 显示屏幕血迹效果
        
        # 检查低血量状态
        if self.health.is_low_health():
            ue.log("WARNING: Low health!")
            # TODO: 播放心跳音效
            # TODO: 显示屏幕红色脉冲效果
    
    def on_death(self, killer):
        """
        死亡时的回调
        
        Args:
            killer: 击杀者
        """
        ue.log(f"Player died! Killed by {killer}")
        
        # 禁用输入
        self.input_handler.disable_input()
        self.is_active = False
        
        # TODO: 播放死亡动画
        # TODO: 显示死亡UI
        # TODO: 延迟后重生或返回主菜单
    
    def on_healed(self, heal_amount):
        """
        治疗时的回调
        
        Args:
            heal_amount: 治疗量
        """
        ue.log(f"Player healed {heal_amount} HP")
        
        # TODO: 更新UI显示血量
        # TODO: 播放治疗音效
        # TODO: 显示治疗特效
    
    # ========== 游戏逻辑方法 ==========
    
    def respawn(self, spawn_location=None):
        """
        重生
        
        Args:
            spawn_location: 重生位置
        """
        if not self.health.is_dead:
            return
        
        # 复活角色
        self.health.revive()
        
        # 重置武器状态
        self.weapon.current_ammo = self.weapon.magazine_size
        self.weapon.reserve_ammo = self.weapon.max_ammo
        self.weapon.is_reloading = False
        self.weapon.is_firing = False
        
        # 启用输入
        self.input_handler.enable_input()
        self.is_active = True
        
        # 传送到重生点
        if spawn_location:
            self.actor.set_actor_location(spawn_location)
        
        ue.log("Player respawned!")
    
    def add_health(self, amount):
        """
        添加生命值
        
        Args:
            amount: 生命值数量
        """
        return self.health.heal(amount)
    
    def add_ammo(self, amount):
        """
        添加弹药
        
        Args:
            amount: 弹药数量
        """
        return self.weapon.add_ammo(amount)
    
    def get_player_info(self):
        """
        获取玩家信息（用于UI显示）
        
        Returns:
            dict: 玩家信息字典
        """
        return {
            'health': self.health.get_info(),
            'ammo': self.weapon.get_ammo_info(),
            'magic_arrow_cd': self.weapon.get_magic_arrow_cooldown_progress(),
            'is_moving': self.character.is_moving(),
            'is_in_air': self.character.is_in_air(),
            'speed': self.character.get_speed(),
        }
    
    # ========== 每帧更新 ==========
    
    def tick(self, delta_time):
        """
        每帧更新
        
        Args:
            delta_time: 帧间隔时间
        """
        if not self.is_active:
            return
        
        # 更新各个子系统
        self.character.tick(delta_time)
        self.camera.tick(delta_time)
        self.weapon.tick(delta_time)
    
    # ========== 清理 ==========
    
    def cleanup(self):
        """清理所有资源"""
        ue.log("Cleaning up PlayerController...")
        
        if self.character:
            self.character.cleanup()
        
        if self.camera:
            self.camera.cleanup()
        
        if self.weapon:
            self.weapon.cleanup()
        
        if self.health:
            self.health.cleanup()
        
        if self.input_handler:
            self.input_handler.cleanup()
        
        self.actor = None
        
        ue.log("PlayerController cleaned up")


# ========== 全局实例管理 ==========

_player_controller_instance = None


def init_player_controller(character_actor):
    """
    初始化玩家控制器（从蓝图调用）
    
    Args:
        character_actor: 角色Actor
    
    Returns:
        PlayerController: 玩家控制器实例
    """
    global _player_controller_instance
    
    if _player_controller_instance:
        _player_controller_instance.cleanup()
    
    _player_controller_instance = PlayerController(character_actor)
    return _player_controller_instance


def get_player_controller():
    """
    获取玩家控制器实例
    
    Returns:
        PlayerController: 玩家控制器实例
    """
    return _player_controller_instance


def cleanup_player_controller():
    """清理玩家控制器"""
    global _player_controller_instance
    
    if _player_controller_instance:
        _player_controller_instance.cleanup()
        _player_controller_instance = None
