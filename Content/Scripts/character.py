# -*- encoding: utf-8 -*-
import ue

@ue.uclass()
class MyCharacter(ue.Character):
    # 暴露变量到蓝图和 UI
    isFire = ue.uproperty(bool)
    current_ammo = ue.uproperty(int)      # 当前弹夹子弹数
    total_ammo = ue.uproperty(int)        # 备弹总数
    is_reloading = ue.uproperty(bool)     # 是否正在换弹
    animation_state = ue.uproperty(int)   # 动画状态：0=Fire, 1=Reload
    
    # 生命值系统
    max_health = ue.uproperty(float)      # 最大生命值
    current_health = ue.uproperty(float)  # 当前生命值
    is_dead = ue.uproperty(bool)          # 是否死亡
    
    @ue.ufunction(override=True)
    def ReceiveBeginPlay(self):
        ue.LogWarning('%s ReceiveBeginPlay!' % self)
        controller = self.GetWorld().GetPlayerController()
        controller.UnPossess()
        controller.Possess(self)
        self.EnableInput(controller)        
        self.InputComponent.BindAxis('MoveForward', self._move_forward)
        self.InputComponent.BindAxis('MoveRight', self._move_right)
        self.InputComponent.BindAxis('TurnRight', self._turn_right)
        self.InputComponent.BindAxis('LookUp', self._look_up)
        self.InputComponent.BindAction('Jump', ue.EInputEvent.IE_Pressed, self._jump)    
        
        # 连射支持：绑定按下和释放
        self.InputComponent.BindAction('Fire', ue.EInputEvent.IE_Pressed, self._fire_pressed)
        self.InputComponent.BindAction('Fire', ue.EInputEvent.IE_Released, self._fire_released)
        
        # 换弹支持：绑定 R 键
        self.InputComponent.BindAction('Reload', ue.EInputEvent.IE_Pressed, self._reload_pressed)
        
        # 魔法箭：绑定鼠标右键
        self.InputComponent.BindAction('FireMagic', ue.EInputEvent.IE_Pressed, self._fire_magic)
        
        # 连射状态
        self.isFire = False
        self.fire_timer = 0.0
        self.fire_rate = 0.08  # 射速：每 0.1 秒一发（600 RPM）
        
        # 弹药系统
        self.mag_size = 30          # 弹夹容量
        self.current_ammo = 30      # 当前弹夹子弹数
        self.total_ammo = 150       # 备弹总数 (不包含当前弹夹)
        self.is_reloading = False   # 是否正在换弹
        self.reload_timer = 0.0     # 换弹计时器
        self.reload_finish_time = 2.17  # 换弹动画时长
        
        # 魔法箭系统
        self.magic_cooldown = 2.0   # 魔法箭CD时间(秒)
        self.magic_timer = 0.0      # CD计时器 (0 = 可以使用)
        self.magic_arrow_class = ue.LoadClass('/Game/MagicArrowBP.MagicArrowBP_C')
        if self.magic_arrow_class:
            self.magic_arrow_class.OwnByPython()        
        
        # 生命值系统
        self.max_health = 100.0
        self.current_health = 100.0
        self.is_dead = False
        
        # 显示UI
        self._create_ui()

    def _move_forward(self, value):
        """前后移动"""
        if value:
            self.AddMovementInput(self.GetActorForwardVector(), value)
    
    def _move_right(self, value):
        """左右移动"""
        if value:
            self.AddMovementInput(self.GetActorRightVector(), value)   

    def _turn_right(self, value):
        self.AddControllerYawInput(value * 45 * ue.GetDeltaTime())

    def _look_up(self, value):
        self.AddControllerPitchInput(value * 45 * ue.GetDeltaTime())

    def _jump(self):
        self.Jump()
    
    def _fire_pressed(self):
        """按下射击键"""
        self.isFire = True
        self.fire_timer = 0.0  # 立即开火
        ue.LogWarning('[Character] ========== Fire pressed - continuous fire enabled ==========')
    
    def _fire_released(self):
        """释放射击键"""
        self.isFire = False
        ue.LogWarning('[Character] Fire released')
        
    
    def _reload_pressed(self):
        """按下换弹键"""
        self._start_reload()
    
    def _start_reload(self):
        """开始换弹"""
        # 检查是否需要换弹
        if self.is_reloading:
            ue.LogWarning('[Character] Already reloading')
            return
        
        if self.current_ammo >= self.mag_size:
            ue.LogWarning('[Character] Magazine is full')
            return
        
        if self.total_ammo <= 0:
            ue.LogWarning('[Character] No reserve ammo to reload')
            return
        
        # 开始换弹
        self.is_reloading = True
        self.isFire = False  # 停止射击
        self.reload_timer = 0.0  # 重置计时器
        
        ue.LogWarning(f'[Character] Reloading... Current: {self.current_ammo}, Total: {self.total_ammo}')
    
    def _finish_reload(self):
        """完成换弹"""
        if not self.is_reloading:
            return
        
        # 计算需要装填的子弹数
        ammo_needed = self.mag_size - self.current_ammo  # 弹夹还需要多少发
        ammo_to_load = min(ammo_needed, self.total_ammo)  # 实际能装填的数量 (取备弹和需求的最小值)
        
        # 更新弹药数
        self.current_ammo += ammo_to_load  # 弹夹增加
        self.total_ammo -= ammo_to_load    # 备弹减少
        
        self.is_reloading = False
        
        ue.LogWarning(f'[Character] Reload complete! Magazine: {self.current_ammo}/{self.mag_size}, Reserve: {self.total_ammo}')
        
        # 更新 UI
        self._update_ammo_ui()
    
    def _fire(self):
        """射击处理 - 使用射线检测"""
        # 检查是否已死亡
        if self.is_dead:
            return
        
        # 检查是否可以射击
        if self.is_reloading:
            ue.LogWarning('[Character] Cannot fire while reloading')
            return
        
        if self.current_ammo <= 0:
            ue.LogWarning('[Character] Out of ammo! Auto reloading...')
            self._start_reload()
            return
        
        ue.LogWarning('[Character] Fire input triggered!')
        
        try:
            # 消耗子弹
            self.current_ammo -= 1
            ue.LogWarning(f'[Character] Ammo: {self.current_ammo}/{self.total_ammo}')
            
            # 更新 UI
            self._update_ammo_ui()
            
            # 如果弹夹打空且有备弹，自动换弹
            if self.current_ammo <= 0:
                if self.total_ammo > 0:
                    ue.LogWarning('[Character] Magazine empty! Auto reloading...')
                    self._start_reload()
                else:
                    ue.LogWarning('[Character] Out of ammo! No reserve ammunition!')
            
            # 播放射击音效
            self._play_fire_sound()
            
            # 从摄像机中心（屏幕中心/准星位置）发射射线
            player_controller = self.GetWorld().GetPlayerController()
            
            # 获取摄像机位置和朝向
            camera_location = player_controller.PlayerCameraManager.GetCameraLocation()
            camera_rotation = player_controller.PlayerCameraManager.GetCameraRotation()
            
            # 计算射线终点（射程 10000 单位）
            fire_range = 10000.0
            
            # 手动计算摄像机前方向量
            import math
            pitch_rad = math.radians(camera_rotation.Pitch)
            yaw_rad = math.radians(camera_rotation.Yaw)
            
            forward = ue.Vector(
                math.cos(pitch_rad) * math.cos(yaw_rad),
                math.cos(pitch_rad) * math.sin(yaw_rad),
                math.sin(pitch_rad)
            )
            
            # 射线起点 = 摄像机位置
            trace_start = camera_location
            trace_end = trace_start + (forward * fire_range)
            
            ue.LogWarning(f'[Character] Trace from camera {trace_start} to {trace_end}')
            # 执行射线检测（使用 KismetSystemLibrary）
            # 使用 TraceTypeQuery1 (Visibility) - 检测所有可见物体
            hit, hit_result = ue.KismetSystemLibrary.LineTraceSingle(
                self,                               # WorldContextObject
                trace_start,                        # Start (从摄像机开始)
                trace_end,                          # End
                ue.ETraceTypeQuery.TraceTypeQuery1, # TraceChannel (Visibility - 检测所有Block Visibility的物体)
                False,                              # bTraceComplex
                [self],                             # ActorsToIgnore (忽略自己)
                ue.EDrawDebugTrace.ForDuration,     # 开启调试射线
                True,                               # bIgnoreSelf
                ue.LinearColor(1, 0, 0, 1),         # TraceColor (红色)
                ue.LinearColor(0, 1, 0, 1),         # TraceHitColor (绿色)
                5.0                                 # DrawTime (显示5秒,更明显)
            )
            
            if hit:
                # 射线击中了某物
                hit_location = hit_result.ImpactPoint
                hit_normal = hit_result.ImpactNormal
                
                # 通过 Component 获取 Actor（需要解引用 WeakPtr）
                hit_component_weak = hit_result.Component
                if hit_component_weak:
                    # 解引用 WeakPtr
                    hit_component = hit_component_weak.Get() if hasattr(hit_component_weak, 'Get') else hit_component_weak
                    if hit_component:
                        hit_actor = hit_component.GetOwner()
                        actor_name = hit_actor.GetName() if hit_actor else "Unknown"
                        ue.LogWarning(f'[Character] Hit: {actor_name} at {hit_location}')
                    else:
                        ue.LogWarning(f'[Character] Hit at {hit_location} (component is null)')
                else:
                    ue.LogWarning(f'[Character] Hit at {hit_location} (no component)')
                
                # 生成弹痕（传入完整的 hit_result 以便更好地计算旋转）
                self._spawn_bullet_decal(hit_location, hit_normal)
                
                # 造成伤害
                if hit_actor and hit_actor.IsA(ue.Character):
                    self._apply_damage_to_target(hit_actor, 10.0)  # 每发子弹10点伤害
            else:
                ue.LogWarning('[Character] No hit detected')
                
        except AttributeError as e:
            ue.LogWarning(f'[Character] AttributeError: {e}')
        except Exception as e:
            ue.LogWarning(f'[Character] Fire error: {e}')
    
    def _play_fire_sound(self):
        """播放射击音效"""
        try:
            # 尝试多个可能的音效路径
            sound_paths = [
                '/Game/Audio/Sounds/Weapons/Rifle2/Weapons_Rifle2_Punch_01.Weapons_Rifle2_Punch_01'
            ]
            
            sound_to_play = None
            for path in sound_paths:
                sound = ue.LoadObject(ue.SoundBase, path)
                if sound:
                    sound_to_play = sound
                    ue.LogWarning(f'[Character] Fire sound loaded: {path}')
                    break
            
            if sound_to_play:
                # 在角色位置播放音效
                ue.GameplayStatics.PlaySoundAtLocation(
                    self,                          # World context
                    sound_to_play,                 # Sound
                    self.GetActorLocation(),       # Location
                    self.GetActorRotation(),          # Rotation
                    1.0,                           # Volume
                    1.0,                           # Pitch
                    0.0                            # Start time
                )
                ue.LogWarning('[Character] Fire sound played')
            else:
                # 如果没有音效文件，使用简单的测试音效或跳过
                ue.LogWarning('[Character] No fire sound found (add sound asset to /Game/Audio/)')
                
        except Exception as e:
            ue.LogWarning(f'[Character] Fire sound error: {e}')
    
    def _spawn_bullet_decal(self, hit_location, hit_normal):
        """生成弹痕"""
        # type: (ue.HitResult) -> None
        try:
            decal_bp_path = '/Game/MyDecalBP.MyDecalBP_C'
            decal_class = ue.LoadClass(decal_bp_path)
            
            if not decal_class:
                ue.LogWarning('[Character] Decal class not found!')
                return
                        
            
            # 计算旋转：让 Decal 贴合表面
            decal_rotation = ue.KismetMathLibrary.MakeRotFromZ(hit_normal)
            
            # 生成 Decal
            decal = self.GetWorld().SpawnActor(
                decal_class,
                hit_location,
                decal_rotation
            )
            
            if decal:
                # 设置 Decal 2秒后自动消失
                decal.SetLifeSpan(5.0)
                ue.LogWarning(f'[Character] Decal spawned at: {hit_location}, will fade in 2s')
            else:
                ue.LogWarning('[Character] Failed to spawn decal')
                
        except Exception as e:
            ue.LogWarning(f'[Character] Decal error: {e}')
    
    def _spawn_bullet_tracer(self, start, end):
        """生成子弹轨迹视觉效果（可选）"""
        # type: (ue.Vector, ue.Vector) -> None
        try:
            # 如果有子弹轨迹特效，可以在这里生成
            # 例如：粒子系统、Beam 特效等
            pass
        except Exception as e:
            ue.LogWarning(f'[Character] Tracer error: {e}')
    
    def _create_ui(self):
        """创建并显示游戏 UI（准心 + 弹药）"""
        try:
            # 加载统一的 UI Widget（包含准心和弹药显示）
            widget_path = '/Game/MyWidget.MyWidget_C'
            widget_class = ue.LoadClass(widget_path)
            
            if widget_class:
                ue.LogWarning(f'[Character] UI widget loaded: {widget_path}')
                
                # 获取玩家控制器
                player_controller = self.GetWorld().GetPlayerController()
                
                if player_controller:
                    # 创建 Widget 实例
                    self.game_ui = ue.WidgetBlueprintLibrary.Create(
                        self,
                        widget_class,
                        player_controller
                    )
                    
                    if self.game_ui:
                        # 添加到视口
                        self.game_ui.AddToViewport()
                        ue.LogWarning('[Character] Game UI displayed!')
                        
                        # 初始化弹药显示
                        self._update_ammo_ui()
                    else:
                        ue.LogWarning('[Character] Failed to create game UI widget')
                else:
                    ue.LogWarning('[Character] Player controller not found')
            else:
                ue.LogWarning('[Character] Game UI widget not found. Create MyWidget in UE Editor.')
                
        except Exception as e:
            ue.LogWarning(f'[Character] UI error: {e}')
            import traceback
            traceback.print_exc()
    
    def _update_ammo_ui(self):
        """更新弹药 UI"""
        try:
            if hasattr(self, 'game_ui') and self.game_ui:
                # 更新 cur 和 total 文本
                # Widget 中应有 TextBlock_Cur 和 TextBlock_Total 组件
                if hasattr(self.game_ui, 'TextBlock_Cur'):
                    self.game_ui.TextBlock_Cur.SetText(str(self.current_ammo))
                
                if hasattr(self.game_ui, 'TextBlock_Total'):
                    self.game_ui.TextBlock_Total.SetText(str(self.total_ammo))
                    
                ue.LogWarning(f'[Character] UI updated: {self.current_ammo}/{self.total_ammo}')
        except Exception as e:
            ue.LogWarning(f'[Character] Update UI error: {e}')
    
    def _fire_magic(self):
        """发射魔法箭"""
        try:
            # 检查CD
            if self.magic_timer > 0:
                ue.LogWarning(f'[Character] Magic arrow on cooldown! {self.magic_timer:.1f}s remaining')
                return
            
            # 检查蓝图类是否加载
            if not self.magic_arrow_class:
                ue.LogWarning('[Character] Magic arrow class not loaded!')
                return
            
            ue.LogWarning('[Character] Firing magic arrow!')
            
            # 获取摄像机朝向
            player_controller = self.GetWorld().GetPlayerController()
            camera_rotation = player_controller.PlayerCameraManager.GetCameraRotation()
            
            # 从角色手部/前方生成魔法箭
            forward = self.GetActorForwardVector()
            spawn_location = self.GetActorLocation() + (forward * 80.0) + ue.Vector(0, 0, 60)  # 前方80,上方60
            
            # 生成魔法箭 Actor (使用蓝图类)
            magic_arrow = self.GetWorld().SpawnActor(
                self.magic_arrow_class,   # 蓝图类
                spawn_location,
                camera_rotation           # 朝向摄像机方向
            )
            
            if magic_arrow:
                ue.LogWarning(f'[Character] Magic arrow spawned at {spawn_location}, rotation: {camera_rotation}')
                
                # 触发CD
                self.magic_timer = self.magic_cooldown
            else:
                ue.LogWarning('[Character] Failed to spawn magic arrow')
                
        except Exception as e:
            ue.LogWarning(f'[Character] Fire magic error: {e}')
            import traceback
            traceback.print_exc()
    
    def _apply_damage_to_target(self, target, damage):
        """对目标造成伤害"""
        try:
            # 检查目标是否有 TakeDamageFromCharacter 方法
            if hasattr(target, 'TakeDamageFromCharacter'):
                target.TakeDamageFromCharacter(damage, self)
                ue.LogWarning(f'[Character] Dealt {damage} damage to {target.GetName()}')
            else:
                ue.LogWarning(f'[Character] Target {target.GetName()} cannot take damage')
        except Exception as e:
            ue.LogWarning(f'[Character] Apply damage error: {e}')
    
    def TakeDamageFromCharacter(self, damage, instigator):
        """受到伤害 - 被其他角色调用"""
        if self.is_dead:
            return
        
        # 扣除生命值
        self.current_health -= damage
        ue.LogWarning(f'[Character] {self.GetName()} took {damage} damage! Health: {self.current_health}/{self.max_health}')
        
        # 更新 UI (如果有血条)
        self._update_health_ui()
        
        # 检查是否死亡
        if self.current_health <= 0:
            self.current_health = 0
            self._on_death(instigator)
    
    def _on_death(self, killer):
        """死亡处理"""
        if self.is_dead:
            return
        
        self.is_dead = True
        self.isFire = False  # 停止射击
        
        ue.LogWarning(f'[Character] {self.GetName()} died! Killed by {killer.GetName() if killer else "Unknown"}')
        
        # 播放死亡动画
        self._play_death_animation()
        
        # 禁用输入 (如果是玩家)
        if self.InputComponent:
            self.DisableInput(self.GetWorld().GetPlayerController())
        
        # 禁用碰撞 (可选,让尸体可以穿过)
        # self.GetCapsuleComponent().SetCollisionEnabled(ue.ECollisionEnabled.NoCollision)
        
        # 5秒后销毁
        # self.SetLifeSpan(5.0)
    
    def _play_death_animation(self):
        """播放死亡动画"""
        try:
            # 加载死亡动画
            death_anim_path = '/Game/Character/Death_1.Death_1'
            death_anim = ue.LoadObject(ue.AnimSequence, death_anim_path)
            
            if death_anim:
                anim_instance = self.Mesh1P.GetAnimInstance()
                if anim_instance:
                    # 播放死亡动画
                    montage = anim_instance.PlaySlotAnimationAsDynamicMontage(
                        death_anim,
                        'DefaultSlot',
                        0.2,    # BlendIn
                        0.0,    # BlendOut (死亡不需要淡出)
                        1.0,    # PlayRate
                        1,      # LoopCount
                        0.0
                    )
                    
                    if montage:
                        ue.LogWarning(f'[Character] Death animation playing')
                    else:
                        ue.LogWarning('[Character] Failed to play death animation')
            else:
                ue.LogWarning('[Character] Death animation not found')
        except Exception as e:
            ue.LogWarning(f'[Character] Death animation error: {e}')
    
    def _update_health_ui(self):
        """更新生命值UI"""
        try:
            if hasattr(self, 'game_ui') and self.game_ui:
                # 如果 Widget 中有血条组件
                if hasattr(self.game_ui, 'ProgressBar_Health'):
                    health_percent = self.current_health / self.max_health
                    self.game_ui.ProgressBar_Health.SetPercent(health_percent)            
        except Exception as e:
            ue.LogWarning(f'[Character] Update health UI error: {e}')
    
    def _debug_print_components(self):
        """调试：打印所有组件"""
        try:
            ue.LogWarning('[Character] === Listing all components ===')
            components = self.GetComponentsByClass(ue.SceneComponent)
            for i, comp in enumerate(components):
                ue.LogWarning(f'[Character] Component {i}: {comp.GetName()} (Type: {type(comp).__name__})')
        except Exception as e:
            ue.LogWarning(f'[Character] Debug error: {e}')
