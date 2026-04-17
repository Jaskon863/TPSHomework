"""
TPS摄像机控制系统
负责第三人称视角的摄像机跟随和旋转
"""

import unreal_engine as ue
from unreal_engine import FVector, FRotator
from unreal_engine.classes import SpringArmComponent, CameraComponent


class CameraController:
    """
    TPS摄像机控制器
    处理摄像机跟随、鼠标旋转、碰撞检测等
    """
    
    def __init__(self, character_actor):
        """
        初始化摄像机控制器
        
        Args:
            character_actor: 角色Actor引用
        """
        self.actor = character_actor
        self.spring_arm = None
        self.camera = None
        
        # 摄像机配置参数（按照readme.md设计）
        self.camera_distance = 300.0  # 摄像机距离
        self.height_offset = 60.0  # 高度偏移
        self.rotation_speed = 1.0  # 旋转速度
        self.pitch_min = -60.0  # 最小俯仰角
        self.pitch_max = 60.0  # 最大俯仰角
        self.interpolation_speed = 10.0  # 平滑跟随速度
        
        # 当前旋转状态
        self.current_pitch = 0.0
        self.current_yaw = 0.0
        
        # 初始化组件
        self._init_components()
    
    def _init_components(self):
        """初始化摄像机组件"""
        if not self.actor:
            return
        
        # 获取或创建Spring Arm组件
        self.spring_arm = self.actor.get_component_by_class(SpringArmComponent)
        
        if self.spring_arm:
            # 配置Spring Arm
            self.spring_arm.TargetArmLength = self.camera_distance
            self.spring_arm.bUsePawnControlRotation = True  # 使用Pawn控制旋转
            self.spring_arm.bEnableCameraLag = True  # 启用摄像机延迟
            self.spring_arm.CameraLagSpeed = self.interpolation_speed
            self.spring_arm.bDoCollisionTest = True  # 启用碰撞检测防止穿墙
            
            # 设置Socket偏移（高度偏移）
            socket_offset = FVector(0, 0, self.height_offset)
            self.spring_arm.SocketOffset = socket_offset
            
            ue.log(f"SpringArm configured: Distance={self.camera_distance}, Height={self.height_offset}")
        else:
            ue.log_warning("SpringArmComponent not found!")
        
        # 获取摄像机组件
        self.camera = self.actor.get_component_by_class(CameraComponent)
        
        if self.camera:
            ue.log("Camera component found and ready")
        else:
            ue.log_warning("CameraComponent not found!")
    
    def handle_look_up(self, axis_value):
        """
        处理向上/向下看输入（俯仰）
        
        Args:
            axis_value: 输入轴值
        """
        if not self.actor:
            return
        
        # 应用旋转速度
        pitch_delta = axis_value * self.rotation_speed
        
        # 累加当前pitch
        self.current_pitch += pitch_delta
        
        # 限制pitch范围
        self.current_pitch = max(self.pitch_min, min(self.pitch_max, self.current_pitch))
        
        # 应用到Controller
        self.actor.add_controller_pitch_input(pitch_delta)
    
    def handle_turn(self, axis_value):
        """
        处理左右转向输入（偏航）
        
        Args:
            axis_value: 输入轴值
        """
        if not self.actor:
            return
        
        # 应用旋转速度
        yaw_delta = axis_value * self.rotation_speed
        
        # 累加当前yaw
        self.current_yaw += yaw_delta
        
        # 应用到Controller
        self.actor.add_controller_yaw_input(yaw_delta)
    
    def set_camera_distance(self, distance):
        """
        设置摄像机距离
        
        Args:
            distance: 新的摄像机距离
        """
        self.camera_distance = distance
        
        if self.spring_arm:
            self.spring_arm.TargetArmLength = distance
            ue.log(f"Camera distance set to {distance}")
    
    def set_height_offset(self, height):
        """
        设置摄像机高度偏移
        
        Args:
            height: 新的高度偏移
        """
        self.height_offset = height
        
        if self.spring_arm:
            socket_offset = FVector(0, 0, height)
            self.spring_arm.SocketOffset = socket_offset
            ue.log(f"Camera height offset set to {height}")
    
    def set_rotation_speed(self, speed):
        """
        设置旋转速度
        
        Args:
            speed: 新的旋转速度
        """
        self.rotation_speed = speed
        ue.log(f"Camera rotation speed set to {speed}")
    
    def get_camera_location(self):
        """
        获取摄像机世界位置
        
        Returns:
            FVector: 摄像机位置
        """
        if self.camera:
            return self.camera.get_world_location()
        return FVector(0, 0, 0)
    
    def get_camera_rotation(self):
        """
        获取摄像机世界旋转
        
        Returns:
            FRotator: 摄像机旋转
        """
        if self.camera:
            return self.camera.get_world_rotation()
        return FRotator(0, 0, 0)
    
    def get_camera_forward_vector(self):
        """
        获取摄像机前向向量
        
        Returns:
            FVector: 前向向量
        """
        rotation = self.get_camera_rotation()
        return ue.get_forward_vector(rotation)
    
    def zoom_in(self, amount=50.0):
        """
        拉近摄像机
        
        Args:
            amount: 拉近距离
        """
        new_distance = max(100.0, self.camera_distance - amount)
        self.set_camera_distance(new_distance)
    
    def zoom_out(self, amount=50.0):
        """
        拉远摄像机
        
        Args:
            amount: 拉远距离
        """
        new_distance = min(600.0, self.camera_distance + amount)
        self.set_camera_distance(new_distance)
    
    def reset_camera(self):
        """重置摄像机到默认状态"""
        self.current_pitch = 0.0
        self.current_yaw = 0.0
        self.set_camera_distance(300.0)
        self.set_height_offset(60.0)
        ue.log("Camera reset to default")
    
    def tick(self, delta_time):
        """
        每帧更新
        
        Args:
            delta_time: 帧间隔时间
        """
        # 这里可以添加需要每帧更新的摄像机逻辑
        # 例如：动态调整FOV、屏幕震动等
        pass
    
    def cleanup(self):
        """清理资源"""
        self.actor = None
        self.spring_arm = None
        self.camera = None
        ue.log("CameraController cleaned up")
