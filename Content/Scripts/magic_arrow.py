# -*- encoding: utf-8 -*-
import ue

@ue.uclass()
class MagicArrow(ue.Actor):
    """魔法箭 - 带飞行轨迹的投射物"""
    
    @ue.ufunction(override=True)
    def ReceiveBeginPlay(self):
        """初始化魔法箭"""
        ue.LogWarning(f'[MagicArrow] Spawned at {self.GetActorLocation()}')
        
        # 配置碰撞组件
        collision_comp = self.Sphere # type: ue.SphereComponent
        
        # 配置投射物移动组件
        movement_comp = self.ProjectileMovement # type: ue.ProjectileMovementComponent
        movement_comp.SetUpdatedComponent(collision_comp)
        
        # 绑定碰撞事件
        collision_comp.OnComponentHit.Add(self._on_hit)
        
        # 飞行参数
        self.lifetime = 5.0          # 生命周期(5秒后自动销毁)
        self.damage = 50.0           # 伤害值                
        
        # 设置生命周期
        self.SetLifeSpan(self.lifetime)
        
        ue.LogWarning('[MagicArrow] Collision event bound')
    
    def _on_hit(self, hit_component, other_actor, other_component, normal_impulse, hit_result):
        """碰撞回调 - 击中目标时触发"""
        try:
            # 避免重复触发
            if not hasattr(self, '_has_hit'):
                self._has_hit = False
            
            if self._has_hit:
                return
            
            self._has_hit = True
            
            # 检查是否击中了有效目标
            if other_actor and other_actor != self:
                actor_name = other_actor.GetName()
                hit_location = hit_result.ImpactPoint
                
                ue.LogWarning(f'[MagicArrow] Hit {actor_name} at {hit_location}')
                
                # TODO: 造成伤害
                # if other_actor.IsA(ue.Character):
                #     ue.GameplayStatics.ApplyDamage(
                #         other_actor,
                #         self.damage,
                #         None,  # Instigator Controller
                #         self,  # Damage Causer
                #         None   # Damage Type
                #     )
                
                # 生成击中特效
                self._spawn_hit_effect(hit_location)
                
                # 销毁魔法箭
                self.Destroy()
        
        except Exception as e:
            ue.LogWarning(f'[MagicArrow] Hit callback error: {e}')
            import traceback
            traceback.print_exc()
    
    
    def _spawn_hit_effect(self, location):
        """生成击中特效"""
        try:
            # 加载并生成粒子特效
            effect_path = '/Game/Effects/ParticleSystems/Weapons/RocketLauncher/Impact/P_Launcher_IH.P_Launcher_IH'
            effect = ue.LoadObject(ue.ParticleSystem, effect_path)
            if effect:
                 ue.GameplayStatics.SpawnEmitterAtLocation(self, effect, location)                 
            # 播放音频
            sound_path = '/Game/Audio/Sounds/Explosions/Explosions_Grenade_SFX_13.Explosions_Grenade_SFX_13'
            sound = ue.LoadObject(ue.SoundBase, sound_path)
            if sound:
                ue.GameplayStatics.PlaySoundAtLocation(
                    self,                          # World context
                    sound,                         # Sound
                    self.GetActorLocation(),       # Location
                    self.GetActorRotation(),       # Rotation
                    1.0,                           # Volume
                    1.0,                           # Pitch
                    0.0                            # Start time
                )              
        except Exception as e:
            ue.LogWarning(f'[MagicArrow] Hit effect error: {e}')
