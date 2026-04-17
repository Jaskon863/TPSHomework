# TPS游戏 - 素材资源需求清单

## 📦 第一阶段（基础框架）资源清单

### 🎭 角色资源 (Content/Characters/)

#### 必需资源
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 骨骼网格体 | `SK_PlayerCharacter` | 标准人形骨骼 | 玩家角色模型 |
| 动画蓝图 | `ABP_PlayerCharacter` | 包含基础状态机 | 角色动画控制 |
| 动画序列 | `Anim_Idle` | 循环动画 | 待机动画 |
| 动画序列 | `Anim_Walk` | 循环动画 | 行走动画 |
| 动画序列 | `Anim_Run` | 循环动画 | 奔跑/冲刺动画 |
| 动画序列 | `Anim_Jump_Start` | 单次播放 | 起跳动画 |
| 动画序列 | `Anim_Jump_Loop` | 循环动画 | 空中动画 |
| 动画序列 | `Anim_Jump_End` | 单次播放 | 落地动画 |

#### 推荐资源（暂可使用默认）
- `Anim_WalkForward` - 向前走
- `Anim_WalkBackward` - 向后走
- `Anim_WalkLeft` - 向左走
- `Anim_WalkRight` - 向右走

---

### 🔫 武器资源 (Content/Weapons/)

#### 必需资源
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 骨骼网格体 | `SK_Rifle` | 步枪模型，带骨骼 | 主武器模型 |
| 静态网格体 | `SM_Rifle` | 静态步枪模型（备选） | 如不需要换弹动画可用 |

#### 推荐动画
- `Anim_Rifle_Fire` - 射击动画（枪械后坐力）
- `Anim_Rifle_Reload` - 换弹动画（2秒）
- `Anim_Rifle_Idle` - 持枪待机

---

### ✨ 特效资源 (Content/VFX/)

#### 核心特效（优先级高）
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 粒子系统 | `P_MuzzleFlash` | 枪口火焰，0.1秒 | 射击时枪口特效 |
| 粒子系统 | `P_BulletImpact` | 命中火花 | 子弹命中物体 |
| 贴花 | `M_BulletHole` | 弹孔贴花材质 | 墙面弹孔 |

#### 次要特效（可延后）
- `P_BulletTrail` - 子弹轨迹（曳光弹）
- `P_ShellEject` - 弹壳抛出
- `P_BloodSplatter` - 血液飞溅
- `P_HitFlesh` - 命中身体特效

#### 魔法箭特效（第二阶段）
- `P_MagicArrow_Charge` - 魔法箭充能特效
- `P_MagicArrow_Trail` - 魔法箭飞行轨迹
- `P_MagicArrow_Impact` - 魔法箭爆炸特效
- `P_MagicArrow_Stun` - 范围晕眩特效圈

---

### 🔊 音效资源 (Content/SFX/)

#### 武器音效
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 音效 | `SFX_GunShot` | 单声道，响亮 | 枪声 |
| 音效 | `SFX_Reload_Start` | 单声道 | 开始换弹 |
| 音效 | `SFX_Reload_Insert` | 单声道 | 插入弹夹 |
| 音效 | `SFX_Reload_End` | 单声道 | 完成换弹 |
| 音效 | `SFX_EmptyGun` | 单声道 | 空枪空响 |

#### 角色音效
- `SFX_Footstep_Concrete` - 水泥地脚步声
- `SFX_Footstep_Grass` - 草地脚步声
- `SFX_Jump` - 跳跃音效
- `SFX_Land` - 落地音效

#### 受击音效
- `SFX_Hit_Body` - 命中身体
- `SFX_Hit_Wall` - 命中墙壁
- `SFX_Hit_Metal` - 命中金属

#### 魔法箭音效（第二阶段）
- `SFX_MagicArrow_Charge` - 充能音效
- `SFX_MagicArrow_Release` - 释放音效
- `SFX_MagicArrow_Fly` - 飞行音效（循环）
- `SFX_MagicArrow_Impact` - 爆炸音效

---

### 🎵 背景音乐 (Content/Music/)

#### 推荐音乐（第三阶段）
- `Music_MainMenu` - 主菜单音乐（轻快）
- `Music_Battle` - 战斗音乐（紧张）
- `Music_Victory` - 胜利音乐
- `Music_Defeat` - 失败音乐

---

### 🎨 UI资源 (Content/UI/Textures/)

#### 必需UI贴图
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 贴图 | `T_Crosshair` | 64x64, PNG透明 | 准星 |
| 贴图 | `T_HealthBar` | 512x64, 红色 | 血条 |
| 贴图 | `T_AmmoIcon` | 64x64 | 弹药图标 |
| 贴图 | `T_BuffIcon_Positive` | 64x64 | 增益Buff图标 |
| 贴图 | `T_BuffIcon_Negative` | 64x64 | 减益Buff图标 |

#### 推荐UI贴图
- `T_Crosshair_Active` - 瞄准敌人时的准星（红色）
- `T_ReloadIcon` - 换弹提示图标
- `T_MagicArrowIcon` - 魔法箭技能图标

---

### 🗺️ 场景资源 (Content/Maps/)

#### 测试关卡（第一阶段）
| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 关卡 | `TestLevel` | 简单场景 | 基础功能测试 |

**TestLevel 要求：**
- 一个平坦的地面（Floor）
- 几个简单的障碍物（Cube/Wall）
- 玩家出生点（PlayerStart）
- 基础光照

#### 正式关卡（第二阶段）
- `Level01_Forest` - 关卡1：森林场景
- `Level02_Warehouse` - 关卡2：仓库场景

---

### 👾 敌人资源 (Content/Enemies/) - 第二阶段

#### 近战敌人
- `SK_MeleeEnemy` - 近战敌人骨骼网格体
- `ABP_MeleeEnemy` - 近战敌人动画蓝图
- `BT_MeleeEnemy` - 近战敌人行为树
- `BB_MeleeEnemy` - 近战敌人黑板

#### 远程敌人
- `SK_RangedEnemy` - 远程敌人骨骼网格体
- `ABP_RangedEnemy` - 远程敌人动画蓝图
- `BT_RangedEnemy` - 远程敌人行为树
- `BB_RangedEnemy` - 远程敌人黑板

---

### 🎁 道具资源 (Content/Items/) - 第二阶段

| 资源类型 | 资源名称 | 规格说明 | 用途 |
|---------|---------|---------|------|
| 静态网格体 | `SM_AmmoBox` | 弹药箱模型 | 弹药补给 |
| 静态网格体 | `SM_HealthPack` | 血包模型（小） | 回复50HP |
| 静态网格体 | `SM_HealthPackBig` | 血包模型（大） | 回复100HP |

---

## 📋 资源优先级

### 🔴 高优先级（第一阶段必需）
1. ✅ 玩家角色模型 + 基础动画
2. ✅ 武器模型（步枪）
3. ✅ 测试关卡地图
4. ⚠️ 基础音效（可临时使用占位符）
5. ⚠️ 基础特效（可临时使用占位符）

### 🟡 中优先级（第二阶段）
1. 敌人模型和动画
2. 道具模型
3. 完整特效
4. 完整音效
5. 正式关卡

### 🟢 低优先级（第三阶段）
1. UI美术资源
2. 背景音乐
3. 高级材质效果
4. 装饰性特效

---

## 🎨 资源规格建议

### 模型规格
- **角色骨骼网格体**: 10k-15k 三角面
- **武器模型**: 2k-5k 三角面
- **道具模型**: 500-1k 三角面
- **场景静态网格**: 视具体情况而定

### 贴图规格
- **角色贴图**: 2048x2048 或 4096x4096
- **武器贴图**: 1024x1024 或 2048x2048
- **UI贴图**: 512x512 或更小
- **特效贴图**: 256x256 或 512x512

### 音效规格
- **格式**: WAV 或 OGG
- **采样率**: 44.1kHz 或 48kHz
- **音量**: 统一标准化处理
- **时长**: 根据需要，一般0.1-3秒

---

## 💡 资源获取建议

### 免费资源商店
1. **Unreal Marketplace** - Epic官方商店（每月免费资源）
2. **Mixamo** - 免费角色和动画
3. **Freesound.org** - 免费音效
4. **Poly Haven** - 免费材质和HDR

### 商业资源商店
1. **Unreal Marketplace** - 付费高质量资源
2. **Unity Asset Store** - 通用资源（需转换）
3. **TurboSquid** - 3D模型
4. **AudioJungle** - 音效和音乐

### 自制资源
- **Blender** - 免费3D建模软件
- **Substance Painter** - 材质绘制
- **Audacity** - 免费音频编辑
- **GIMP** - 免费图像编辑

---

## ✅ 资源导入检查清单

### 模型导入
- [ ] 骨骼方向正确（朝向+X轴）
- [ ] 缩放比例正确（100单位 = 1米）
- [ ] LOD设置正确
- [ ] 碰撞体设置正确

### 动画导入
- [ ] 骨骼匹配正确
- [ ] 帧率设置正确（30fps或60fps）
- [ ] 根骨骼运动正确
- [ ] 动画循环设置正确

### 音效导入
- [ ] 音量标准化
- [ ] 采样率一致
- [ ] 声道设置正确（单声道/立体声）
- [ ] 压缩格式合适

### 特效资源
- [ ] 粒子数量优化
- [ ] 贴图格式正确
- [ ] 材质设置合理
- [ ] 性能开销可接受

---

## 📞 资源需求反馈

如果需要更详细的资源规格说明，请告知：
1. 具体哪个资源需要详细说明
2. 遇到什么导入或使用问题
3. 需要什么格式或规格的资源

---

**创建日期**: 2026-04-12  
**版本**: v1.0  
**更新**: 根据开发进度随时更新
