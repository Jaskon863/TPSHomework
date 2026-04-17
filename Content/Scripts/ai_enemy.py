# -*- encoding: utf-8 -*-
import ue
from character import MyCharacter

@ue.uclass()
class AIEnemy(MyCharacter):
    """AI敌人 - 继承主角的战斗系统"""
    
    @ue.ufunction(override=True)
    def ReceiveBeginPlay(self):
        """初始化AI敌人"""
        ue.LogWarning(f'[AIEnemy] {self.GetName()} spawned!')
        
        # 初始化基础系统 (但不绑定输入)
        self.isFire = False
        self.fire_timer = 0.0
        self.fire_rate = 0.15  # AI射速稍慢
        
        # 弹药系统
        self.mag_size = 30
        self.current_ammo = 30
        self.total_ammo = 150
        self.is_reloading = False
        self.reload_timer = 0.0
        self.reload_finish_time = 2.17
        
        # AI 特有参数
        self.is_ai = True
        self.target_player = None
        self.attack_range = 1000.0      # 攻击范围 (cm)
        self.chase_range = 3000.0       # 追击范围
        self.rotation_speed = 2.0       # 旋转速度
        
        # AI 状态
        self.ai_state = 'Idle'  # Idle, Chase, Attack
        
        # 生命值 (继承自父类,可以自定义)
        self.max_health = 50.0    # AI 血量较少
        self.current_health = 50.0
        self.is_dead = False
        
        ue.LogWarning('[AIEnemy] Initialized')
    
    @ue.ufunction(override=True)
    def ReceiveTick(self, delta_seconds):
        """每帧更新 - AI行为 + 战斗系统"""
        # 如果已死亡,停止所有逻辑
        if self.is_dead:
            return
        
        # 1. 更新动画状态 (复用父类逻辑)
        if self.is_reloading:
            self.animation_state = 1
        elif self.isFire:
            self.animation_state = 0
        else:
            self.animation_state = -1
        
        # 2. 换弹计时器 (复用父类逻辑)
        if self.is_reloading:
            self.reload_timer += delta_seconds
            if self.reload_timer >= self.reload_finish_time:
                self._finish_reload()
        
        # 3. 连射逻辑 (复用父类逻辑)
        if self.isFire and not self.is_reloading:
            self.fire_timer += delta_seconds
            if self.fire_timer >= self.fire_rate:
                self._fire()
                self.fire_timer = 0.0
        
        # 4. AI 行为逻辑 (AI特有)
        self._ai_behavior(delta_seconds)
    
    def _ai_behavior(self, delta_seconds):
        """AI行为决策"""
        try:
            # 寻找玩家目标
            if not self.target_player:
                self.target_player = self._find_player()
                if self.target_player:
                    ue.LogWarning(f'[AIEnemy] Found player: {self.target_player.GetName()}')
            
            if not self.target_player:
                self.ai_state = 'Idle'
                self.isFire = False
                return
            
            # 计算与玩家的距离
            distance = self._get_distance_to(self.target_player)
            
            # 状态机
            if distance > self.chase_range:
                # 超出追击范围,进入待机
                self.ai_state = 'Idle'
                self.isFire = False
                
            elif distance > self.attack_range:
                # 在追击范围内,但超出攻击范围
                self.ai_state = 'Chase'
                self.isFire = False
                # TODO: 移动向玩家
                self._face_target(self.target_player, delta_seconds)
                
            else:
                # 在攻击范围内
                self.ai_state = 'Attack'
                self._face_target(self.target_player, delta_seconds)
                
                # 简单瞄准判断: 如果大致朝向玩家,开火
                if self._is_facing_target(self.target_player):
                    self.isFire = True
                else:
                    self.isFire = False
        
        except Exception as e:
            ue.LogWarning(f'[AIEnemy] AI behavior error: {e}')
    
    def _find_player(self):
        """寻找玩家角色"""
        try:
            # 获取玩家控制的角色
            player_controller = self.GetWorld().GetPlayerController()
            if player_controller:
                player_pawn = player_controller.GetPawn()
                if player_pawn and player_pawn != self:
                    return player_pawn
        except Exception as e:
            ue.LogWarning(f'[AIEnemy] Find player error: {e}')
        return None
    
    def _get_distance_to(self, target):
        """计算到目标的距离"""
        my_location = self.GetActorLocation()
        target_location = target.GetActorLocation()
        delta = target_location - my_location
        return delta.Size()
    
    def _face_target(self, target, delta_seconds):
        """平滑地面向目标"""
        try:
            # 计算朝向目标的方向
            my_location = self.GetActorLocation()
            target_location = target.GetActorLocation()
            
            direction = target_location - my_location
            direction.Z = 0  # 忽略高度差
            direction = direction.GetSafeNormal()
            
            # 计算目标旋转
            target_rotation = ue.KismetMathLibrary.MakeRotFromX(direction)
            
            # 平滑插值
            current_rotation = self.GetActorRotation()
            new_rotation = ue.KismetMathLibrary.RInterpTo(
                current_rotation,
                target_rotation,
                delta_seconds,
                self.rotation_speed
            )
            
            # 只旋转 Yaw (水平旋转)
            self.SetActorRotation(ue.Rotator(0, new_rotation.Yaw, 0), False)
        
        except Exception as e:
            ue.LogWarning(f'[AIEnemy] Face target error: {e}')
    
    def _is_facing_target(self, target, tolerance=20.0):
        """判断是否面向目标"""
        try:
            my_location = self.GetActorLocation()
            target_location = target.GetActorLocation()
            
            # 计算到目标的方向
            direction = target_location - my_location
            direction.Z = 0
            direction = direction.GetSafeNormal()
            
            # 当前朝向
            forward = self.GetActorForwardVector()
            forward.Z = 0
            forward = forward.GetSafeNormal()
            
            # 计算夹角 (点积)
            dot = forward.X * direction.X + forward.Y * direction.Y
            angle = ue.KismetMathLibrary.Acos(dot) * 180.0 / 3.14159
            
            return angle < tolerance
        
        except Exception as e:
            return False
    
    # 注意: _fire(), _start_reload(), _finish_reload() 等方法
    # 都是从父类 MyCharacter 继承的,无需重写!
