# Coast Stack Calculator (CSCal) 使用说明书

## 概述

**Coast Stack Calculator (CSCal)** 是一款基于 **RPN（Reverse Polish Notation，逆波兰表示法）** 的栈式计算器。它采用栈作为核心数据结构，通过将操作数压入栈中、运算符弹出栈顶元素进行运算的方式，实现高效、无歧义的计算流程。

---

## 目录

- [设计理念](#设计理念)
- [快速开始](#快速开始)
- [核心 API](#核心-api)
- [运算符说明](#运算符说明)
- [异常处理](#异常处理)
- [完整示例](#完整示例)
- [开发者须知](#开发者须知)

---

## 设计理念

传统中缀表达式（如 `1 + 2`）需要处理运算符优先级和括号，而 RPN 将运算符置于操作数之后（如 `1 2 +`），无需括号和优先级规则，计算过程与栈操作天然契合：

1. 遇到**操作数** → 压入栈
2. 遇到**运算符** → 从栈中弹出所需数量的操作数，运算后将结果压回栈

---

## 快速开始

### 安装

将项目克隆或复制到本地，确保目录结构如下：

```
coast_stackcalculator/
├── __init__.py
├── example.py
├── readme.md
├── calc/
│   ├── __init__.py
│   ├── base_csc.py
│   └── exceptions.py
└── doc/
    └── instructions.md
```

### 基本使用

```python
from calc import base_csc as cscal

# 创建计算器实例
calc = cscal.CoastStackCalculator()

# 运行 RPN 表达式
calc.run("3 4 + 2 *")

# 查看结果
print(calc.stack)  # 输出: [14.0]
```

---

## 核心 API

### `CoastStackCalculator` 类

#### `__init__()`

初始化计算器实例，注册内置运算符。

#### `run(ins: str)`

执行 RPN 表达式。

| 参数 | 类型 | 说明 |
|------|------|------|
| `ins` | `str` | 空格分隔的 RPN 表达式字符串 |

**执行流程：**
1. 清空栈
2. 按空格分割表达式为 token 列表
3. 遍历每个 token：
   - 若是**运算符** → 执行对应运算
   - 若是**其他** → 作为操作数压入栈

#### `stack` 属性

列表类型，存储当前栈中的所有操作数和中间结果。

---

## 运算符说明

| 运算符 | 方法 | 描述 | 弹出顺序 |
|--------|------|------|----------|
| `+` | `add()` | 加法：弹出两数相加 | 先弹出 `a`，再弹出 `b`，计算 `b + a` |
| `-` | `sub()` | 减法：弹出两数相减 | 先弹出 `a`，再弹出 `b`，计算 `b - a` |
| `*` | `mul()` | 乘法：弹出两数相乘 | 先弹出 `a`，再弹出 `b`，计算 `b * a` |
| `/` | `true_div()` | 除法：弹出两数相除，**含除零检查** | 先弹出 `a`（除数），再弹出 `b`（被除数），计算 `b / a` |

> **注意：** 减法和除法的操作数顺序很重要。例如 `5 3 -` 计算的是 `5 - 3 = 2`，而非 `3 - 5`。

---

## 异常处理

CSCal 定义了四级异常体系：

```
BaseCSCException (基类)
├── StackManagement    — 栈操作越界
├── MathError          — 数学错误（如除零）
└── SyntaxFault        — 语法错误（token 无法参与运算）
```

### 异常详情

| 异常类 | 触发条件 | 示例 |
|--------|----------|------|
| `StackManagement` | 栈中元素不足时执行运算 | `"+"`（空栈执行加法） |
| `MathError` | 除数为零 | `"5 0 /"` |
| `SyntaxFault` | token 既非运算符也非有效操作数 | `"1 2 & +"` |
| `BaseCSCException` | 其他未知错误 | — |

### 异常处理示例

```python
from calc.base_csc import CoastStackCalculator
from calc.exceptions import StackManagement, MathError, SyntaxFault

calc = CoastStackCalculator()

try:
    calc.run("5 0 /")
except MathError as e:
    print(f"数学错误: {e}")     # 数学错误: 除数为零
except StackManagement as e:
    print(f"栈错误: {e}")
except SyntaxFault as e:
    print(f"语法错误: {e}")
```

---

## 完整示例

```python
from calc import base_csc as cscal

calc = cscal.CoastStackCalculator()

# 基本四则运算: (1 + 2) * 3 / 4
calc.run("1 2 + 3 * 4 /")
print(calc.stack)  # 输出: [2.25]

# 链式计算: 1 + 2 = 3, 3 * 3 = 9, 9 - 5 = 4
calc.run("1 2 + 3 * 5 -")
print(calc.stack)  # 输出: [4.0]

# 复杂表达式
calc.run("15 3 / 2 * 7 +")
print(calc.stack)  # 输出: [17.0]
# 计算过程:
#   15 入栈        → [15]
#   3 入栈         → [15, 3]
#   / → 15/3=5    → [5]
#   2 入栈         → [5, 2]
#   * → 5*2=10    → [10]
#   7 入栈         → [10, 7]
#   + → 10+7=17   → [17]
```

---

## 开发者须知

### 扩展运算符

你可以通过继承 `CoastStackCalculator` 并注册新运算符来扩展功能：

```python
from calc.base_csc import CoastStackCalculator
import operator as op

class MyCalculator(CoastStackCalculator):
    def __init__(self):
        super().__init__()
        # 注册取幂运算符
        self.ins_dict["^"] = self.pow
    
    def pow(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(op.pow(b, a))

calc = MyCalculator()
calc.run("2 3 ^")
print(calc.stack)  # 输出: [8.0]
```

### 项目结构

```
coast_stackcalculator/
├── __init__.py              # 包初始化
├── example.py               # 使用示例
├── readme.md                # 项目简介
├── calc/
│   ├── __init__.py           # 子包初始化
│   ├── base_csc.py           # 核心计算器实现
│   └── exceptions.py         # 自定义异常定义
└── doc/
    └── instructions.md       # 使用说明书（本文件）
```

---

## 许可证

请参阅项目根目录下的许可证文件。
