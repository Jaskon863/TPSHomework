# -*- encoding: utf-8 -*-
import ue

@ue.uclass()
class MyRifle(ue.Actor):
    @ue.ufunction(override=True)
    def ReceiveBeginPlay(self):
        pick_up = self.PickUp # type: ue.SphereComponent
        pick_up.OnComponentBeginOverlap.Add(self._on_pick_up)
        self.bullet_class = ue.LoadClass('/Game/MyBulletBP.MyBulletBP_C')
        self.bullet_class.OwnByPython()

    def _on_pick_up(self, overlapped_comp, other_actor, other_comp, other_body_index, from_sweep, sweepresult):
        # type: (ue.PrimitiveComponent, ue.Actor, ue.PrimitiveComponent, int, bool, ue.HitResult) -> None
        from character import MyCharacter
        if other_actor.IsA(MyCharacter):
            my_character = other_actor # type: MyCharacter
            my_character.pick_up_weapon(self)

    def fire(self):
        """射击逻辑"""
        try:
            ue.LogWarning('[Rifle] Fire called!')
            
            # 检查子弹类是否加载
            if not self.bullet_class:
                ue.LogWarning('[Rifle] Error: bullet_class not loaded!')
                return
            
            # 获取枪口位置
            mesh = self.RifleMesh  # type: ue.SkeletalMeshComponent
            if not mesh:
                ue.LogWarning('[Rifle] Error: RifleMesh not found!')
                return
            
            # 获取 Muzzle socket 位置和旋转
            spawn_location = mesh.GetSocketLocation('Muzzle')
            spawn_rotation = mesh.GetSocketRotation('Muzzle')
            
            ue.LogWarning(f'[Rifle] Spawn bullet at: {spawn_location}')
            
            # 生成子弹
            bullet = self.GetWorld().SpawnActor(
                self.bullet_class,
                spawn_location,
                spawn_rotation
            )
            
            if bullet:
                ue.LogWarning('[Rifle] Bullet spawned successfully!')
            else:
                ue.LogWarning('[Rifle] Failed to spawn bullet!')
                
        except Exception as e:
            ue.LogWarning(f'[Rifle] Fire error: {e}')
