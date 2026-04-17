"""
生命值系统
处理角色生命值、受伤和死亡
"""

import unreal_engine as ue


class HealthComponent:
    """
    生命值组件
    管理角色的生命值、受伤、治疗和死亡
    """
    
    def __init__(self, owner_actor, max_health=100.0):
        """
        初始化生命值组件
        
        Args:
            owner_actor: 所属Actor
            max_health: 最大生命值
        """
        self.owner = owner_actor
        self.max_health = max_health
        self.current_health = max_health
        self.is_dead = False
        
        # 回调函数
        self.on_damage_callback = None
        self.on_death_callback = None
        self.on_heal_callback = None
        
        ue.log(f"HealthComponent initialized: {max_health} HP")
    
    def take_damage(self, damage, attacker=None, damage_type=None):
        """
        受到伤害
        
        Args:
            damage: 伤害值
            attacker: 攻击者
            damage_type: 伤害类型
        
        Returns:
            float: 实际造成的伤害
        """
        if self.is_dead:
            return 0.0
        
        if damage <= 0:
            return 0.0
        
        # 计算实际伤害
        actual_damage = min(damage, self.current_health)
        old_health = self.current_health
        self.current_health -= actual_damage
        
        ue.log(f"{self.owner.get_name()} took {actual_damage} damage. HP: {self.current_health}/{self.max_health}")
        
        # 触发受伤回调
        if self.on_damage_callback:
            self.on_damage_callback(actual_damage, attacker, damage_type)
        
        # 播放受击效果
        self._play_damage_effects(actual_damage)
        
        # 检查是否死亡
        if self.current_health <= 0:
            self.die(attacker)
        
        return actual_damage
    
    def heal(self, amount):
        """
        治疗
        
        Args:
            amount: 治疗量
        
        Returns:
            float: 实际治疗量
        """
        if self.is_dead:
            return 0.0
        
        if amount <= 0:
            return 0.0
        
        old_health = self.current_health
        self.current_health = min(self.current_health + amount, self.max_health)
        actual_heal = self.current_health - old_health
        
        ue.log(f"{self.owner.get_name()} healed {actual_heal}. HP: {self.current_health}/{self.max_health}")
        
        # 触发治疗回调
        if self.on_heal_callback:
            self.on_heal_callback(actual_heal)
        
        # 播放治疗效果
        self._play_heal_effects(actual_heal)
        
        return actual_heal
    
    def die(self, killer=None):
        """
        死亡
        
        Args:
            killer: 击杀者
        """
        if self.is_dead:
            return
        
        self.is_dead = True
        self.current_health = 0.0
        
        ue.log(f"{self.owner.get_name()} died!")
        
        # 触发死亡回调
        if self.on_death_callback:
            self.on_death_callback(killer)
        
        # 播放死亡效果
        self._play_death_effects()
    
    def revive(self, health_amount=None):
        """
        复活
        
        Args:
            health_amount: 复活后的生命值（None则满血复活）
        """
        if not self.is_dead:
            return
        
        self.is_dead = False
        
        if health_amount is None:
            self.current_health = self.max_health
        else:
            self.current_health = min(health_amount, self.max_health)
        
        ue.log(f"{self.owner.get_name()} revived with {self.current_health} HP")
    
    def set_max_health(self, new_max_health):
        """
        设置最大生命值
        
        Args:
            new_max_health: 新的最大生命值
        """
        old_max = self.max_health
        self.max_health = new_max_health
        
        # 如果当前血量超过新的最大值，则裁剪
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        
        ue.log(f"Max health changed: {old_max} -> {self.max_health}")
    
    def get_health_percentage(self):
        """
        获取生命值百分比
        
        Returns:
            float: 生命值百分比 (0.0-1.0)
        """
        if self.max_health <= 0:
            return 0.0
        
        return self.current_health / self.max_health
    
    def is_low_health(self, threshold=0.3):
        """
        检查是否低血量
        
        Args:
            threshold: 低血量阈值 (0.0-1.0)
        
        Returns:
            bool: 是否低血量
        """
        return self.get_health_percentage() <= threshold
    
    def is_full_health(self):
        """
        检查是否满血
        
        Returns:
            bool: 是否满血
        """
        return self.current_health >= self.max_health
    
    def _play_damage_effects(self, damage):
        """
        播放受伤特效
        
        Args:
            damage: 伤害值
        """
        # TODO: 播放受击音效
        # TODO: 播放受击粒子特效
        # TODO: 触发受击动画
        # TODO: 如果是玩家，显示屏幕血迹效果
        pass
    
    def _play_heal_effects(self, heal_amount):
        """
        播放治疗特效
        
        Args:
            heal_amount: 治疗量
        """
        # TODO: 播放治疗音效
        # TODO: 播放治疗粒子特效
        pass
    
    def _play_death_effects(self):
        """播放死亡特效"""
        # TODO: 播放死亡音效
        # TODO: 播放死亡动画
        # TODO: 如果是敌人，触发溶解效果
        # TODO: 掉落道具
        pass
    
    def get_info(self):
        """
        获取生命值信息
        
        Returns:
            dict: 生命值信息字典
        """
        return {
            'current': self.current_health,
            'max': self.max_health,
            'percentage': self.get_health_percentage(),
            'is_dead': self.is_dead,
            'is_low': self.is_low_health(),
            'is_full': self.is_full_health(),
        }
    
    def cleanup(self):
        """清理资源"""
        self.owner = None
        self.on_damage_callback = None
        self.on_death_callback = None
        self.on_heal_callback = None
        ue.log("HealthComponent cleaned up")
