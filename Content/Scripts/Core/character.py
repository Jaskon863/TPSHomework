"""
玩家角色控制系统
负责角色移动、跳跃等基础控制
"""

import unreal_engine as ue
from unreal_engine import FVector, FRotator
from unreal_engine.classes import CharacterMovementComponent


class PlayerCharacter:
    """
    玩家角色控制器
    处理WASD移动、跳跃、输入响应等功能
    """
    
    def __init__(self, character_actor):
        """
        初始化玩家角色
        
        Args:
            character_actor: UE角色Actor引用
        """
        self.actor = character_actor
        self.movement_component = None
        
        # 移动参数配置
        self.move_speed = 600.0  # 移动速度
        self.sprint_speed = 900.0  # 冲刺速度
        self.jump_velocity = 600.0  # 跳跃初速度
        
        # 输入状态
        self.forward_input = 0.0
        self.right_input = 0.0
        self.is_sprinting = False
        
        # 初始化组件
        self._init_components()
    
    def _init_components(self):
        """初始化角色组件"""
        if self.actor:
            # 获取角色移动组件
            self.movement_component = self.actor.get_component_by_class(CharacterMovementComponent)
            
            if self.movement_component:
                # 配置移动组件
                self.movement_component.MaxWalkSpeed = self.move_speed
                self.movement_component.JumpZVelocity = self.jump_velocity
                self.movement_component.AirControl = 0.3  # 空中控制能力
                self.movement_component.GravityScale = 1.0
                
                ue.log(f"PlayerCharacter initialized: {self.actor.get_name()}")
            else:
                ue.log_warning("CharacterMovementComponent not found!")
    
    def handle_move_forward(self, axis_value):
        """
        处理前后移动输入
        
        Args:
            axis_value: 输入轴值 (-1.0 到 1.0)
        """
        self.forward_input = axis_value
        self._apply_movement()
    
    def handle_move_right(self, axis_value):
        """
        处理左右移动输入
        
        Args:
            axis_value: 输入轴值 (-1.0 到 1.0)
        """
        self.right_input = axis_value
        self._apply_movement()
    
    def _apply_movement(self):
        """应用移动输入"""
        if not self.actor:
            return
        
        # 获取角色朝向
        rotation = self.actor.get_actor_rotation()
        
        # 计算前后移动方向
        if self.forward_input != 0:
            forward_vector = ue.get_forward_vector(rotation)
            self.actor.add_movement_input(forward_vector, self.forward_input)
        
        # 计算左右移动方向
        if self.right_input != 0:
            right_vector = ue.get_right_vector(rotation)
            self.actor.add_movement_input(right_vector, self.right_input)
    
    def handle_jump(self):
        """处理跳跃"""
        if self.actor and self.can_jump():
            self.actor.jump()
            ue.log("Player jumping")
    
    def handle_jump_released(self):
        """处理跳跃释放（可中断跳跃）"""
        if self.actor:
            self.actor.stop_jumping()
    
    def can_jump(self):
        """
        检查是否可以跳跃
        
        Returns:
            bool: 是否可以跳跃
        """
        if not self.movement_component:
            return False
        
        return self.movement_component.IsMovingOnGround()
    
    def handle_sprint_start(self):
        """开始冲刺"""
        self.is_sprinting = True
        if self.movement_component:
            self.movement_component.MaxWalkSpeed = self.sprint_speed
            ue.log("Sprint started")
    
    def handle_sprint_stop(self):
        """停止冲刺"""
        self.is_sprinting = False
        if self.movement_component:
            self.movement_component.MaxWalkSpeed = self.move_speed
            ue.log("Sprint stopped")
    
    def get_velocity(self):
        """
        获取当前速度
        
        Returns:
            FVector: 速度向量
        """
        if self.actor:
            return self.actor.get_velocity()
        return FVector(0, 0, 0)
    
    def get_speed(self):
        """
        获取当前移动速度（标量）
        
        Returns:
            float: 移动速度
        """
        velocity = self.get_velocity()
        return velocity.size()
    
    def is_moving(self):
        """
        检查是否在移动
        
        Returns:
            bool: 是否在移动
        """
        return self.get_speed() > 0.1
    
    def is_in_air(self):
        """
        检查是否在空中
        
        Returns:
            bool: 是否在空中
        """
        if not self.movement_component:
            return False
        
        return self.movement_component.IsFalling()
    
    def tick(self, delta_time):
        """
        每帧更新
        
        Args:
            delta_time: 帧间隔时间
        """
        # 这里可以添加需要每帧更新的逻辑
        pass
    
    def cleanup(self):
        """清理资源"""
        self.actor = None
        self.movement_component = None
        ue.log("PlayerCharacter cleaned up")
