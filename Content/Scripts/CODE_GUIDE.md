# TPS游戏 - 第一阶段代码框架说明

## 📁 已创建的文件结构

```
Content/Scripts/
├── Core/                          # 核心系统
│   ├── __init__.py               # 核心模块初始化
│   ├── character.py              # 角色移动控制
│   ├── camera.py                 # TPS摄像机系统
│   └── input_handler.py          # 输入处理器
│
├── Gameplay/                      # 游戏玩法
│   ├── __init__.py               # 玩法模块初始化
│   ├── weapon_system.py          # 武器系统（枪械+魔法箭）
│   └── health_component.py       # 生命值组件
│
└── player_controller.py           # 玩家控制器主类（整合所有系统）
```

## 🎯 已实现的功能

### 1. 角色控制系统 (character.py)
- ✅ WASD 8向移动
- ✅ 空格跳跃（支持中断跳跃）
- ✅ Shift 冲刺
- ✅ 移动速度可配置
- ✅ 空中控制
- ✅ 速度和状态查询

### 2. TPS摄像机系统 (camera.py)
- ✅ 第三人称跟随视角
- ✅ 鼠标控制旋转
- ✅ 俯仰角限制（-60° ~ 60°）
- ✅ 摄像机碰撞检测（防止穿墙）
- ✅ 平滑跟随插值
- ✅ 摄像机距离和高度可调
- ✅ 滚轮缩放功能

### 3. 武器系统 (weapon_system.py)
- ✅ 枪械射击（点射/连射模式）
- ✅ 弹夹机制（30发弹夹，90发备弹）
- ✅ 换弹系统（2秒换弹时间）
- ✅ 射线检测命中判定
- ✅ 射速控制（10发/秒）
- ✅ 魔法箭系统（5秒CD）
- ✅ 弹药管理和补充

### 4. 生命值系统 (health_component.py)
- ✅ 生命值管理（100HP）
- ✅ 受伤和治疗
- ✅ 死亡和复活
- ✅ 低血量检测
- ✅ 回调事件系统

### 5. 输入处理 (input_handler.py)
- ✅ 统一输入管理
- ✅ 输入事件分发
- ✅ 输入启用/禁用

### 6. 主控制器 (player_controller.py)
- ✅ 所有系统整合
- ✅ 输入绑定接口
- ✅ 游戏事件回调
- ✅ 玩家信息获取
- ✅ Tick更新管理

## 🔧 如何在UE5中使用

### 方法1：在蓝图中集成（推荐）

1. **创建角色蓝图（BP_PlayerCharacter）**
   - 继承自 `Character` 类
   - 添加 `SpringArm` 组件
   - 添加 `Camera` 组件（作为SpringArm的子组件）
   - 添加 `SkeletalMesh` 组件（角色模型）

2. **在角色蓝图的EventGraph中初始化Python控制器**

```python
# Event BeginPlay
import player_controller

# 初始化玩家控制器
self.py_controller = player_controller.init_player_controller(self)
```

3. **绑定输入事件**

在角色蓝图的 Event Graph 中：

```
InputAxis MoveForward (绑定W/S)
    └─> Call Python Function: self.py_controller.bind_move_forward(AxisValue)

InputAxis MoveRight (绑定A/D)
    └─> Call Python Function: self.py_controller.bind_move_right(AxisValue)

InputAction Jump (绑定Space)
    Pressed  └─> Call: self.py_controller.bind_jump_pressed()
    Released └─> Call: self.py_controller.bind_jump_released()

InputAxis LookUp (绑定鼠标Y)
    └─> Call: self.py_controller.bind_look_up(AxisValue)

InputAxis Turn (绑定鼠标X)
    └─> Call: self.py_controller.bind_turn(AxisValue)

InputAction Fire (绑定鼠标左键)
    Pressed  └─> Call: self.py_controller.bind_fire_pressed()
    Released └─> Call: self.py_controller.bind_fire_released()

InputAction MagicArrow (绑定鼠标右键)
    Pressed  └─> Call: self.py_controller.bind_magic_arrow_pressed()

InputAction Reload (绑定R键)
    Pressed  └─> Call: self.py_controller.bind_reload_pressed()

InputAction Sprint (绑定Shift键)
    Pressed  └─> Call: self.py_controller.bind_sprint_pressed()
    Released └─> Call: self.py_controller.bind_sprint_released()
```

4. **添加Tick更新**

```
Event Tick
    └─> Call Python Function: self.py_controller.tick(DeltaSeconds)
```

5. **清理资源**

```
Event EndPlay
    └─> Call Python Function: player_controller.cleanup_player_controller()
```

### 方法2：纯Python实现（高级）

如果你熟悉NePy的绑定机制，可以直接在Python中绑定输入：

```python
# 在character.py或单独的绑定文件中
def setup_input_bindings(character):
    character.bind_axis("MoveForward", lambda x: controller.bind_move_forward(x))
    character.bind_axis("MoveRight", lambda x: controller.bind_move_right(x))
    # ... 其他绑定
```

## 🎮 输入配置

确保在 **Project Settings > Input** 中配置以下输入映射：

### Axis Mappings（轴映射）
- `MoveForward`: W(1.0), S(-1.0)
- `MoveRight`: D(1.0), A(-1.0)
- `LookUp`: Mouse Y(-1.0)
- `Turn`: Mouse X(1.0)

### Action Mappings（动作映射）
- `Jump`: Space
- `Fire`: Left Mouse Button
- `MagicArrow`: Right Mouse Button
- `Reload`: R
- `Sprint`: Left Shift

## 📦 需要的素材资源

### 必需资源
1. **角色模型**
   - 骨骼网格体：`SK_PlayerCharacter`
   - 动画蓝图：`ABP_PlayerCharacter`
   - 动画：Idle, Walk, Run, Jump

2. **武器模型**
   - 步枪模型：`SK_Rifle`
   - 武器动画：Fire, Reload

### 可选资源（特效和音效）
3. **特效资源**
   - 枪口火焰：`P_MuzzleFlash`
   - 弹孔贴花：`M_BulletHole`
   - 命中火花：`P_ImpactSpark`

4. **音效资源**
   - 枪声：`SFX_GunShot`
   - 换弹音效：`SFX_Reload`
   - 脚步声：`SFX_Footstep`

## 🔍 测试方法

1. **基础移动测试**
   - 按 WASD 测试8向移动
   - 按 Space 测试跳跃
   - 按 Shift 测试冲刺

2. **摄像机测试**
   - 移动鼠标测试视角旋转
   - 测试俯仰角限制
   - 靠近墙壁测试碰撞检测

3. **射击测试**
   - 按鼠标左键测试射击
   - 查看控制台日志确认射线检测
   - 按 R 测试换弹
   - 测试弹药耗尽自动换弹

4. **魔法箭测试**
   - 按鼠标右键释放魔法箭
   - 测试5秒CD

## 🐛 调试技巧

### 查看日志
所有系统都有详细的日志输出，使用以下方式查看：

1. **UE编辑器输出日志**（Output Log窗口）
2. **控制台命令**：在游戏中按 `~` 打开控制台

### 常见问题排查

**问题1：角色不移动**
- 检查CharacterMovementComponent是否存在
- 检查输入绑定是否正确
- 查看日志中的"PlayerCharacter initialized"消息

**问题2：摄像机不跟随**
- 检查SpringArmComponent和CameraComponent是否正确设置
- 确认摄像机组件是SpringArm的子组件

**问题3：射击无反应**
- 检查武器系统是否初始化
- 查看弹药是否耗尽
- 检查是否在换弹状态

## 📝 TODO清单（待实现的功能）

代码中标记了 `TODO` 的部分需要后续实现：

### 特效相关
- [ ] 枪口火焰粒子特效
- [ ] 弹孔贴花生成
- [ ] 命中火花特效
- [ ] 受击血液特效
- [ ] 魔法箭轨迹特效

### 音效相关
- [ ] 枪声音效播放
- [ ] 换弹音效播放
- [ ] 脚步声播放
- [ ] 受击音效播放

### 动画相关
- [ ] 射击动画播放
- [ ] 换弹动画播放
- [ ] 受击动画播放
- [ ] 死亡动画播放

### UI相关
- [ ] 血条UI更新
- [ ] 弹药UI更新
- [ ] 伤害跳字
- [ ] 准星显示
- [ ] 魔法箭CD显示

### 其他
- [ ] 魔法箭投射物生成
- [ ] 屏幕抖动效果
- [ ] 低血量屏幕效果
- [ ] 定时器系统完善

## 🚀 下一步开发计划

**第二阶段：核心玩法扩展**
- Buff系统实现
- AI敌人系统
- 道具系统
- 关卡管理

**第三阶段：表现优化**
- UI系统完善
- 音效特效集成
- 材质和渲染效果
- 性能优化

## 💡 使用建议

1. **逐步测试**：先测试基础移动和摄像机，确认正常后再测试射击
2. **查看日志**：所有关键操作都有日志输出，便于调试
3. **先用占位符**：特效和音效可以先不实现，专注于逻辑功能
4. **保持模块化**：每个系统独立，便于后续扩展和维护

## 📧 需要帮助？

如果在使用过程中遇到问题，请：
1. 检查日志输出
2. 确认输入绑定正确
3. 验证组件是否正确创建
4. 查看本文档的"常见问题排查"部分

---

**创建日期**: 2026-04-12  
**版本**: v1.0 - 第一阶段基础框架
