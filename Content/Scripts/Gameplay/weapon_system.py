"""
武器系统
包含枪械射击和魔法箭功能
"""

import unreal_engine as ue
from unreal_engine import FVector, FRotator, FHitResult
import time


class WeaponSystem:
    """
    武器系统
    处理枪械射击、魔法箭、换弹等功能
    """
    
    def __init__(self, owner_actor):
        """
        初始化武器系统
        
        Args:
            owner_actor: 武器持有者Actor
        """
        self.owner = owner_actor
        
        # 枪械参数（按照readme.md设计）
        self.weapon_name = "Rifle"
        self.damage = 20.0  # 基础伤害
        self.fire_rate = 10.0  # 射速（发/秒）
        self.magazine_size = 30  # 弹夹容量
        self.reload_time = 2.0  # 换弹时间（秒）
        self.fire_mode = "auto"  # "single" 或 "auto"
        self.max_ammo = 90  # 最大备弹
        
        # 当前状态
        self.current_ammo = self.magazine_size  # 当前弹夹弹药
        self.reserve_ammo = self.max_ammo  # 备弹
        self.is_firing = False  # 是否正在射击
        self.is_reloading = False  # 是否正在换弹
        self.last_fire_time = 0.0  # 上次射击时间
        
        # 魔法箭参数
        self.magic_arrow_damage = 50.0
        self.magic_arrow_speed = 2000.0
        self.magic_arrow_cooldown = 5.0  # CD时间
        self.stun_duration = 3.0  # 晕眩持续时间
        self.stun_radius = 300.0  # 晕眩范围
        self.last_magic_arrow_time = 0.0  # 上次释放时间
        
        # 射线检测参数
        self.weapon_range = 10000.0  # 武器射程
        
        ue.log("WeaponSystem initialized")
    
    # ========== 枪械系统 ==========
    
    def start_fire(self):
        """开始射击"""
        if self.is_reloading:
            ue.log("Cannot fire while reloading")
            return
        
        self.is_firing = True
        
        if self.fire_mode == "single":
            # 单发模式，只射击一次
            self._fire_single_shot()
        else:
            # 自动模式，需要在tick中持续射击
            pass
    
    def stop_fire(self):
        """停止射击"""
        self.is_firing = False
    
    def _fire_single_shot(self):
        """射击单发子弹"""
        if not self._can_fire():
            return
        
        # 消耗弹药
        self.current_ammo -= 1
        self.last_fire_time = time.time()
        
        # 执行射线检测
        self._perform_raycast()
        
        # 播放射击特效和音效
        self._play_fire_effects()
        
        ue.log(f"Fired! Ammo: {self.current_ammo}/{self.magazine_size}")
        
        # 如果弹药耗尽，自动换弹
        if self.current_ammo == 0:
            self.reload()
    
    def _can_fire(self):
        """
        检查是否可以射击
        
        Returns:
            bool: 是否可以射击
        """
        if self.is_reloading:
            return False
        
        if self.current_ammo <= 0:
            ue.log("Out of ammo! Reloading...")
            self.reload()
            return False
        
        # 检查射速CD
        current_time = time.time()
        fire_interval = 1.0 / self.fire_rate
        
        if current_time - self.last_fire_time < fire_interval:
            return False
        
        return True
    
    def _perform_raycast(self):
        """执行射线检测"""
        if not self.owner:
            return
        
        # 获取摄像机位置和方向
        camera_location = self.owner.get_actor_location()
        camera_rotation = self.owner.get_control_rotation()
        
        # 计算射线终点
        forward_vector = ue.get_forward_vector(camera_rotation)
        end_location = camera_location + (forward_vector * self.weapon_range)
        
        # 执行射线检测
        hit_result = ue.line_trace_single(
            self.owner.get_world(),
            camera_location,
            end_location,
            trace_complex=True,
            ignore_self=True
        )
        
        if hit_result and hit_result.bBlockingHit:
            hit_actor = hit_result.Actor
            hit_location = hit_result.Location
            
            ue.log(f"Hit: {hit_actor.get_name()} at {hit_location}")
            
            # 应用伤害
            self._apply_damage(hit_actor, hit_location)
            
            # 播放命中特效
            self._play_impact_effects(hit_location, hit_result.Normal)
    
    def _apply_damage(self, target_actor, hit_location):
        """
        对目标应用伤害
        
        Args:
            target_actor: 目标Actor
            hit_location: 命中位置
        """
        if not target_actor:
            return
        
        # TODO: 获取Buff系统的伤害修正
        final_damage = self.damage
        
        # 应用伤害到目标
        # 这里需要目标有HealthComponent
        # target_actor.take_damage(final_damage, self.owner)
        
        ue.log(f"Applied {final_damage} damage to {target_actor.get_name()}")
    
    def _play_fire_effects(self):
        """播放射击特效和音效"""
        # TODO: 播放枪口火焰特效
        # TODO: 播放枪声音效
        # TODO: 播放武器后坐力动画
        pass
    
    def _play_impact_effects(self, location, normal):
        """
        播放命中特效
        
        Args:
            location: 命中位置
            normal: 命中表面法线
        """
        # TODO: 在命中点生成弹孔贴花
        # TODO: 播放命中火花特效
        # TODO: 播放命中音效
        pass
    
    def reload(self):
        """换弹"""
        if self.is_reloading:
            ue.log("Already reloading")
            return
        
        if self.current_ammo == self.magazine_size:
            ue.log("Magazine is full")
            return
        
        if self.reserve_ammo <= 0:
            ue.log("No reserve ammo")
            return
        
        self.is_reloading = True
        ue.log(f"Reloading... ({self.reload_time}s)")
        
        # 停止射击
        self.stop_fire()
        
        # TODO: 播放换弹动画
        # TODO: 设置定时器，在reload_time后完成换弹
        # 这里简化处理，直接完成换弹（实际应该使用Timer）
        ue.set_timer(self.owner, self._finish_reload, self.reload_time, False)
    
    def _finish_reload(self):
        """完成换弹"""
        if not self.is_reloading:
            return
        
        # 计算需要补充的弹药
        ammo_needed = self.magazine_size - self.current_ammo
        ammo_to_reload = min(ammo_needed, self.reserve_ammo)
        
        # 更新弹药数量
        self.current_ammo += ammo_to_reload
        self.reserve_ammo -= ammo_to_reload
        
        self.is_reloading = False
        ue.log(f"Reload complete! Ammo: {self.current_ammo}/{self.magazine_size}, Reserve: {self.reserve_ammo}")
    
    def toggle_fire_mode(self):
        """切换射击模式"""
        if self.fire_mode == "single":
            self.fire_mode = "auto"
            ue.log("Fire mode: AUTO")
        else:
            self.fire_mode = "single"
            ue.log("Fire mode: SINGLE")
    
    # ========== 魔法箭系统 ==========
    
    def fire_magic_arrow(self):
        """发射魔法箭"""
        if not self._can_fire_magic_arrow():
            return
        
        self.last_magic_arrow_time = time.time()
        
        # 获取发射位置和方向
        spawn_location = self.owner.get_actor_location()
        spawn_rotation = self.owner.get_control_rotation()
        
        # TODO: 生成魔法箭投射物
        # 这需要在蓝图中创建投射物Actor
        # projectile = ue.spawn_actor(MagicArrowClass, spawn_location, spawn_rotation)
        
        ue.log(f"Magic Arrow fired! CD: {self.magic_arrow_cooldown}s")
        
        # 播放特效
        self._play_magic_arrow_effects()
    
    def _can_fire_magic_arrow(self):
        """
        检查是否可以发射魔法箭
        
        Returns:
            bool: 是否可以发射
        """
        current_time = time.time()
        
        if current_time - self.last_magic_arrow_time < self.magic_arrow_cooldown:
            remaining_cd = self.magic_arrow_cooldown - (current_time - self.last_magic_arrow_time)
            ue.log(f"Magic Arrow on cooldown: {remaining_cd:.1f}s remaining")
            return False
        
        return True
    
    def _play_magic_arrow_effects(self):
        """播放魔法箭特效"""
        # TODO: 播放魔法箭充能特效
        # TODO: 播放魔法箭释放音效
        pass
    
    def get_magic_arrow_cooldown_progress(self):
        """
        获取魔法箭CD进度
        
        Returns:
            float: CD进度 (0.0-1.0)
        """
        current_time = time.time()
        elapsed = current_time - self.last_magic_arrow_time
        
        if elapsed >= self.magic_arrow_cooldown:
            return 1.0
        
        return elapsed / self.magic_arrow_cooldown
    
    # ========== 弹药管理 ==========
    
    def add_ammo(self, amount):
        """
        添加备弹
        
        Args:
            amount: 弹药数量
        """
        old_ammo = self.reserve_ammo
        self.reserve_ammo = min(self.reserve_ammo + amount, self.max_ammo)
        actual_added = self.reserve_ammo - old_ammo
        
        ue.log(f"Added {actual_added} ammo. Reserve: {self.reserve_ammo}/{self.max_ammo}")
        
        return actual_added
    
    def get_ammo_info(self):
        """
        获取弹药信息
        
        Returns:
            dict: 弹药信息字典
        """
        return {
            'current': self.current_ammo,
            'magazine': self.magazine_size,
            'reserve': self.reserve_ammo,
            'max_reserve': self.max_ammo,
        }
    
    # ========== 每帧更新 ==========
    
    def tick(self, delta_time):
        """
        每帧更新
        
        Args:
            delta_time: 帧间隔时间
        """
        # 自动射击模式下持续射击
        if self.is_firing and self.fire_mode == "auto" and not self.is_reloading:
            self._fire_single_shot()
    
    def cleanup(self):
        """清理资源"""
        self.owner = None
        self.stop_fire()
        ue.log("WeaponSystem cleaned up")
