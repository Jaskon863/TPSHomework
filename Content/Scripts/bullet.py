# -*- encoding: utf-8 -*-
import ue

@ue.uclass()
class Mybullet(ue.Actor):
    @ue.ufunction(override=True)
    def ReceiveBeginPlay(self):
        """子弹初始化"""
        # 子弹速度
        self.speed = 10000.0
        
        # 子弹生命周期（秒）
        self.SetLifeSpan(3.0)
        
        # 🔧 禁用重力和物理模拟（关键！）
        try:
            # 获取根组件
            root_comp = self.GetRootComponent()
            if root_comp:
                # 禁用物理模拟
                if hasattr(root_comp, 'SetSimulatePhysics'):
                    root_comp.SetSimulatePhysics(False)
                
                # 禁用重力
                if hasattr(root_comp, 'SetEnableGravity'):
                    root_comp.SetEnableGravity(False)
                
                ue.LogWarning('[Bullet] Physics disabled')
        except Exception as e:
            ue.LogWarning(f'[Bullet] Failed to disable physics: {e}')
        
        
        # 设置碰撞检测
        try:
            # 假设蓝图中有一个球体碰撞组件
            collision_comp = self.BulletCollision  # type: ue.SphereComponent
            if collision_comp:
                collision_comp.OnComponentHit.Add(self._on_hit)
                ue.LogWarning('[Bullet] Collision setup complete')
        except AttributeError:
            ue.LogWarning('[Bullet] Warning: No BulletCollision component found')
    
    @ue.ufunction(override=True)
    def ReceiveTick(self, delta_seconds):
        """每帧移动子弹"""
        # 沿着前方移动
        forward = self.GetActorForwardVector()
        movement = forward * self.speed * delta_seconds
        new_location = self.GetActorLocation() + movement
        
        # 使用 Sweep 进行移动，可以检测碰撞
        sweep_result = ue.HitResult()
        self.SetActorLocation(new_location, True, sweep_result)
        
        # 每 0.2 秒打印一次位置（避免日志刷屏）
        if not hasattr(self, 'log_timer'):
            self.log_timer = 0.0
        
        self.log_timer += delta_seconds
        if self.log_timer >= 0.2:
            ue.LogWarning(f'[Bullet] Position: {new_location}')
            self.log_timer = 0.0
    
    def _on_hit(self, hit_comp, other_actor, other_comp, normal_impulse, hit_result):
        """碰撞处理"""
        # type: (ue.PrimitiveComponent, ue.Actor, ue.PrimitiveComponent, ue.Vector, ue.HitResult) -> None
        try:
            ue.LogWarning(f'[Bullet] Hit: {other_actor.GetName()} at {hit_result.ImpactPoint}')
            
            # 生成弹痕
            self._spawn_bullet_decal(hit_result)
            
            # TODO: 添加伤害逻辑
            # if other_actor.IsA(ue.Character):
            #     # 造成伤害
            #     pass
            
            # 销毁子弹
            self.Destroy()
        except Exception as e:
            ue.LogWarning(f'[Bullet] Hit error: {e}')
    
    def _spawn_bullet_decal(self, hit_result):
        """在碰撞点生成弹痕贴花"""
        # type: (ue.HitResult) -> None
        try:
            # 弹痕蓝图路径（需要先创建）
            decal_bp_path = '/Game/Effects/Blueprints/B_WeaponDecals.B_WeaponDecals'           
            # 加载 Decal 类
            decal_class = ue.LoadClass(decal_bp_path)
            
            if not decal_class:
                ue.LogWarning('[Bullet] Decal class not found! Please create BP_BulletDecal')
                return
            
            # 获取碰撞点和法线
            impact_point = hit_result.ImpactPoint
            impact_normal = hit_result.ImpactNormal
            
            # 计算 Decal 的旋转（朝向表面法线）
            decal_rotation = self._calculate_decal_rotation(impact_normal)
            
            # 生成 Decal
            decal = self.GetWorld().SpawnActor(
                decal_class,
                impact_point,
                decal_rotation
            )
            
            if decal:
                ue.LogWarning(f'[Bullet] Decal spawned at: {impact_point}')
                
                # 设置 Decal 生命周期（可选，自动消失）
                # decal.SetLifeSpan(10.0)  # 10秒后消失
            else:
                ue.LogWarning('[Bullet] Failed to spawn decal')
                
        except Exception as e:
            ue.LogWarning(f'[Bullet] Decal spawn error: {e}')
    
    def _calculate_decal_rotation(self, normal):
        """根据表面法线计算 Decal 的旋转"""
        # type: (ue.Vector) -> ue.Rotator
        try:
            # 使用法线向量创建旋转
            # UE 中 Decal 的前方向（X轴）应该指向表面法线
            forward = normal
            right = ue.Vector(0, 1, 0)
            
            # 如果法线接近向上，使用不同的参考向量
            if abs(forward.Z) > 0.9:
                right = ue.Vector(1, 0, 0)
            
            # 创建旋转矩阵
            rotation = ue.MakeRotFromXZ(forward, ue.Vector(0, 0, 1))
            
            return rotation
        except:
            # 如果计算失败，返回默认旋转
            return ue.FRotator(0, 0, 0)
    
    def _debug_print_components(self):
        """调试：打印所有组件"""
        try:
            ue.LogWarning('[Bullet] === Components ===')
            components = self.GetComponentsByClass(ue.SceneComponent)
            for comp in components:
                ue.LogWarning(f'[Bullet]   - {comp.GetName()} ({type(comp).__name__})')
        except Exception as e:
            ue.LogWarning(f'[Bullet] Debug error: {e}')
