# Task-2 Spec：兆易创新技术指标计算 Notebook

## 1. 任务概述

基于 `Task-1/兆易创新_近一年交易数据.csv`，在 Jupyter Notebook 中**从零实现**以下 5 个技术指标的计算过程，并配以可视化：

| 指标 | 类型 | 核心参数 |
|------|------|----------|
| RSI | 动量/超买超卖 | N=14 |
| MACD | 趋势/动能 | 快线 12，慢线 26，信号线 9 |
| 布林带 (Bollinger Bands) | 波动率/通道 | 均线 20，标准差倍数 2 |
| ATR | 波动率 | N=14 |
| KDJ | 动量/随机 | RSV 周期 9，D 平滑 3，J 系数 3 |

**要求**：不调用现成指标库（如 TA-Lib），用 pandas/numpy 手动实现每个公式，并在 Notebook 中逐步展示计算过程。

---

## 2. 数据说明

**文件**：`Task-1/兆易创新_近一年交易数据.csv`
**行数**：244 行（2025-07-02 ~ 2026-07-02，约一年）
**字段**：

| 字段名 | 含义 | 指标计算中的用途 |
|--------|------|----------------|
| `trade_date` | 交易日期 | 索引，按日期升序排列 |
| `open` | 开盘价 | — |
| `high` | 最高价 | MACD/布林带/ATR/KDJ |
| `low` | 最低价 | ATR/KDJ |
| `close` | 收盘价 | 所有指标的核心输入 |
| `vol` | 成交量（手） | OBV 扩展（可选） |
| `amount` | 成交额（元） | — |

**数据预处理步骤**：
1. 读取 CSV，将 `trade_date` 转为 datetime 类型
2. 按 `trade_date` 升序排列（CSV 当前是降序）
3. 重置索引，设为从 0 开始的顺序整数索引
4. 检查缺失值，如有则向前填充（ffill）

---

## 3. 各指标计算规格

### 3.1 RSI（相对强弱指数）

**公式**：
```
delta = close.diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
RS = avg_gain / avg_loss
RSI = 100 - (100 / (1 + RS))
```

**Notebook 展示步骤**：
- Cell 1：计算 `delta`，展示前 20 行
- Cell 2：分别计算 `gain` / `loss`，解释为何跌的日子 loss 为正
- Cell 3：计算 `avg_gain` / `avg_loss`（平滑处理）
- Cell 4：计算 RS 和 RSI
- Cell 5：绘制 RSI 折线图 + 超买线(70) / 超卖线(30)

**输出列**：`RSI_14`

---

### 3.2 MACD（指数平滑异同移动平均线）

**公式**：
```
EMA_fast = close.ewm(span=12, adjust=False).mean()
EMA_slow = close.ewm(span=26, adjust=False).mean()
DIF = EMA_fast - EMA_slow
DEA = DIF.ewm(span=9, adjust=False).mean()
MACD_hist = (DIF - DEA) * 2   # A股常用 ×2 放大
```

**Notebook 展示步骤**：
- Cell 1：手动实现 EMA 函数（递归公式），对比 `ewm()` 结果验证
- Cell 2：计算 DIF 和 DEA
- Cell 3：绘制 DIF/DEA 双线图 + MACD 柱状图
- Cell 4：标注金叉（DIF 上穿 DEA）/ 死叉（DIF 下穿 DEA）位置

**输出列**：`EMA_12`, `EMA_26`, `DIF`, `DEA`, `MACD_hist`

---

### 3.3 布林带（Bollinger Bands）

**公式**：
```
MB = close.rolling(window=20).mean()
std = close.rolling(window=20).std()
UP = MB + 2 * std
DN = MB - 2 * std
Bandwidth = (UP - DN) / MB   # 带宽比率
%B = (close - DN) / (UP - DN) # 价格在带内的相对位置
```

**Notebook 展示步骤**：
- Cell 1：计算中轨（MB）、上轨（UP）、下轨（DN）
- Cell 2：绘制价格 + 布林带三线图，带状区域用半透明填充
- Cell 3：计算并绘制 Bandwidth 和 %B，解释"挤压"信号
- Cell 4：标注价格触碰上轨/下轨的日期

**输出列**：`BB_middle`, `BB_upper`, `BB_lower`, `BB_bandwidth`, `BB_percentB`

---

### 3.4 ATR（平均真实波幅）

**公式**：
```
TR = max(H - L, abs(H - C_prev), abs(L - C_prev))
ATR = TR.rolling(window=14).mean()
# 更常用的是 Welles Wilder 平滑法：
ATR = TR.ewm(alpha=1/14, adjust=False).mean()
```

**Notebook 展示步骤**：
- Cell 1：计算三个候选值，取 max 得到 TR
- Cell 2：用 Wilder 平滑法计算 ATR（解释为何不用简单移动平均）
- Cell 3：绘制 ATR 折线图，标注高波动和低波动区间
- Cell 4：演示用 ATR 设置止损距（入场价 ± 2×ATR）

**输出列**：`TR`, `ATR_14`

---

### 3.5 KDJ（随机指标）

**公式**：
```
lowest_low = low.rolling(window=9).min()
highest_high = high.rolling(window=9).max()
RSV = (close - lowest_low) / (highest_high - lowest_low) * 100
K = RSV.ewm(com=2, adjust=False).mean()   # 或者 (2/3)*K_prev + (1/3)*RSV
D = K.ewm(com=2, adjust=False).mean()
J = 3 * K - 2 * D
```

**Notebook 展示步骤**：
- Cell 1：计算 `lowest_low` 和 `highest_high`，解释 RSV 的含义（收盘价在 N 日高低价范围内的相对位置）
- Cell 2：计算 K 值（RSV 的平滑）和 D 值（K 的平滑）
- Cell 3：计算 J 值，解释 J 为何会超出 0~100 范围
- Cell 4：绘制 K/D/J 三线图 + 超买线(80) / 超卖线(20)
- Cell 5：标注 K/D 金叉和死叉

**输出列**：`RSV_9`, `K`, `D`, `J`

---

## 4. Notebook 结构规划（完整 Cell 列表）

```
Cell 1  [Markdown]  # 技术指标计算 Notebook — 兆易创新 (603986)
                      ## 目标：从零实现 5 个经典技术指标
Cell 2  [Code]      # 环境准备：import pandas/numpy/matplotlib/seaborn
Cell 3  [Code]      # 数据加载与预处理（读取 CSV、排序、检查缺失值）
Cell 4  [Code]      # 数据预览：head()、describe()、绘制原始收盘价走势
Cell 5  [Markdown]  ## 一、RSI 相对强弱指数
Cell 6  [Code]      # RSI Step 1：计算 delta、gain、loss
Cell 7  [Code]      # RSI Step 2：计算 avg_gain/avg_loss（平滑处理）
Cell 8  [Code]      # RSI Step 3：计算 RSI 并绘图
Cell 9  [Markdown]  ## 二、MACD 指数平滑异同移动平均线
Cell 10 [Code]      # MACD Step 1：手动实现 EMA 函数并验证
Cell 11 [Code]      # MACD Step 2：计算 DIF、DEA、柱状图
Cell 12 [Code]      # MACD Step 3：绘图 + 标注金叉/死叉
Cell 13 [Markdown]  ## 三、布林带 Bollinger Bands
Cell 14 [Code]      # 布林带 Step 1：计算中轨、上轨、下轨
Cell 15 [Code]      # 布林带 Step 2：计算 Bandwidth 和 %B
Cell 16 [Code]      # 布林带 Step 3：绘图 + 标注触碰轨道的日期
Cell 17 [Markdown]  ## 四、ATR 平均真实波幅
Cell 18 [Code]      # ATR Step 1：计算 TR（真实波幅）
Cell 19 [Code]      # ATR Step 2：Wilder 平滑法计算 ATR
Cell 20 [Code]      # ATR Step 3：绘图 + 演示用 ATR 设置止损距
Cell 21 [Markdown]  ## 五、KDJ 随机指标
Cell 22 [Code]      # KDJ Step 1：计算 RSV
Cell 23 [Code]      # KDJ Step 2：计算 K、D、J 值
Cell 24 [Code]      # KDJ Step 3：绘图 + 标注金叉/死叉
Cell 25 [Markdown]  ## 六、综合信号分析
Cell 26 [Code]      # 将 5 个指标合并到同一 DataFrame
Cell 27 [Code]      # 统计各指标同时发出买入/卖出信号的日期
Cell 28 [Code]      # 综合信号热力图（日期 × 指标信号矩阵）
Cell 29 [Markdown]  ## 总结与反思
```

---

## 5. 综合信号分析（Cell 25~28 详细规格）

**目标**：将 5 个指标的信号整合，寻找"共振"日期

**买入信号定义**：
- RSI：RSI < 30
- MACD：DIF 上穿 DEA（金叉，且 DIF < 0 更佳）
- 布林带：收盘价 < 下轨（或 %B < 0）
- ATR：ATR 处于低位（波动缩小，即将变盘）
- KDJ：K 上穿 D（金叉，且 J < 20 更佳）

**卖出信号定义**：
- RSI：RSI > 70
- MACD：DIF 下穿 DEA（死叉，且 DIF > 0 更佳）
- 布林带：收盘价 > 上轨（或 %B > 1）
- KDJ：K 下穿 D（死叉，且 J > 80 更佳）

**输出**：信号矩阵 DataFrame + 热力图

---

## 6. 交付物

| 文件 | 路径 | 说明 |
|------|------|------|
| Notebook | `Task-2/兆易创新_技术指标计算.ipynb` | 主交付物，含完整代码和说明 |
| 数据（副本）| `Task-2/兆易创新_近一年交易数据.csv` | 数据副本，确保路径独立 |
| 图表输出 | `Task-2/charts/` | 各指标可视化 PNG 导出 |

---

## 7. 实施注意事项

1. **数据方向**：CSV 是降序（最新在前），计算前必须 `sort_values('trade_date')` 转为升序
2. **前 N 行 NaN**：所有滚动指标前 N-1 行都是 NaN，绘图时注意截断或标注
3. **中文显示**：matplotlib 需配置中文字体（`plt.rcParams['font.sans-serif'] = ['SimHei']`）
4. **A 股惯例**：MACD 柱状图通常 ×2 放大；KDJ 参数 (9,3,3) 是国内软件标准
5. **复现性**：设置随机种子（虽本任务无随机操作，养成习惯）

---

## 8. 验收标准

- [ ] 5 个指标均手动实现（无 TA-Lib 等现成指标库调用）
- [ ] 每个指标的计算步骤拆分到多个 Cell，逐步展示中间变量
- [ ] 每个指标均有配套可视化图表
- [ ] 综合信号分析 Cell 能输出共振日期列表
- [ ] Notebook 可完整运行（`Restart & Run All` 无报错）
- [ ] 图表中文字显示正常（无方框乱码）
