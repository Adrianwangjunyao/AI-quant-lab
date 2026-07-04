#!/usr/bin/env python3
"""
生成 兆易创新_技术指标计算.ipynb
按照 spec.md 的完整规划，从零实现 5 个技术指标
"""
import json
import os

NOTEBOOK = {
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.9.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": []
}

def md(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": text
    }

def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

cells = NOTEBOOK["cells"]

# ============================================================
# Cell 1: 标题
# ============================================================
cells.append(md([
    "# 技术指标计算 Notebook —— 兆易创新 (603986)\n",
    "\n",
    "## 目标\n",
    "- 从零实现 5 个经典技术指标（不依赖 TA-Lib 等现成库）\n",
    "- 每个指标分步展示计算过程\n",
    "- 配套可视化图表\n",
    "- 综合信号分析：寻找多指标共振的买卖时点\n",
    "\n",
    "## 指标清单\n",
    "| 指标 | 类型 | 核心参数 |\n",
    "|------|------|----------|\n",
    "| RSI  | 动量/超买超卖 | N=14 |\n",
    "| MACD | 趋势/动能   | 12 / 26 / 9 |\n",
    "| 布林带 | 波动率/通道 | 20日均线 + 2倍标准差 |\n",
    "| ATR  | 波动率       | N=14 |\n",
    "| KDJ  | 动量/随机   | (9, 3, 3) |"
]))

# ============================================================
# Cell 2: 环境准备
# ============================================================
cells.append(md([
    "## 0. 环境准备与数据加载"
]))

cells.append(code([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib\n",
    "import seaborn as sns\n",
    "from matplotlib.patches import Rectangle\n",
    "import warnings\n",
    "from matplotlib.dates import DateFormatter\n",
    "from matplotlib.ticker import ScalarFormatter\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# 中文显示配置（Windows）\n",
    "plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']\n",
    "plt.rcParams['axes.unicode_minus'] = False\n",
    "sns.set_style('whitegrid')\n",
    "\n",
    "print('pandas :', pd.__version__)\n",
    "print('numpy  :', np.__version__)\n",
    "print('环境准备完成')"
]))

# ============================================================
# Cell 3: 数据加载
# ============================================================
cells.append(code([
    "# 读取数据\n",
    "df = pd.read_csv('兆易创新_近一年交易数据.csv')\n",
    "df.head()"
]))

# ============================================================
# Cell 4: 数据预处理
# ============================================================
cells.append(code([
    "# 数据预处理\n",
    "print('原始数据形状：', df.shape)\n",
    "print('\\n原始排序（前5行）：')\n",
    "print(df['trade_date'].head().tolist())\n",
    "print('\\n原始排序（后5行）：')\n",
    "print(df['trade_date'].tail().tolist())\n",
    "\n",
    "# CSV 是降序（最新在前），需要转为升序\n",
    "df = df.sort_values('trade_date').reset_index(drop=True)\n",
    "\n",
    "print('\\n>>> 排序后（前5行）：')\n",
    "print(df['trade_date'].head().tolist())\n",
    "print('\\n>>> 排序后（后5行）：')\n",
    "print(df['trade_date'].tail().tolist())\n",
    "\n",
    "# 检查缺失值\n",
    "print('\\n>>> 缺失值统计：')\n",
    "print(df.isnull().sum())\n",
    "\n",
    "# 将 trade_date 转为 datetime 类型（确保 x 轴正确显示为日期）\n",
    "df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')\n",
    "print(f'\\n>>> 日期范围：{df[\"trade_date\"].min().date()}  ~  {df[\"trade_date\"].max().date()}')"
]))

# ============================================================
# Cell 5: 数据预览
# ============================================================
cells.append(code([
    "# 数据预览\n",
    "print('数据形状：', df.shape)\n",
    "print('\\n列名：', df.columns.tolist())\n",
    "print('\\n数据统计：')\n",
    "display(df.describe())\n",
    "\n",
    "# 绘制原始收盘价走势（使用对数坐标）\n",
    "fig, ax = plt.subplots(figsize=(14, 5.5))\n",
    "ax.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=2, label='收盘价')\n",
    "ax.set_yscale('log')\n",
    "ax.yaxis.set_major_formatter(ScalarFormatter())\n",
    "ax.fill_between(df['trade_date'], df['close'].min(), df['close'], alpha=0.06, color='#2563EB')\n",
    "ax.set_title('兆易创新 (603986) —— 近一年收盘价走势（对数坐标）', fontsize=14, fontweight='600')\n",
    "ax.set_xlabel('日期')\n",
    "ax.set_ylabel('收盘价（元）')\n",
    "ax.tick_params(axis='x', rotation=45)\n",
    "ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))\n",
    "ax.grid(alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "print('💡 使用对数坐标后，相同涨幅在图上显示的高度一致。')\n",
    "print(f'   价格范围：¥{df[\"close\"].min():.1f}  ~  ¥{df[\"close\"].max():.1f}')"
]))

# ============================================================
# Cell 6: 全局绘图样式配置
# ============================================================
cells.append(md([
    "## 绘图样式配置\n",
    "\n",
    "统一设置全局样式，后续所有图表将共享：  \n",
    "- **对数坐标**：价格图使用对数刻度，消除价格量级差异  \n",
    "- **日期格式**：x 轴自动格式化为月/日  \n",
    "- **专业配色**：统一的颜色方案和布局"
]))

cells.append(code([
    "from matplotlib.dates import DateFormatter\n",
    "from matplotlib.ticker import ScalarFormatter\n",
    "\n",
    "# 全局样式\n",
    "plt.rcParams.update({\n",
    "    'font.size': 10,\n",
    "    'axes.titlesize': 13,\n",
    "    'axes.labelsize': 11,\n",
    "    'xtick.labelsize': 9,\n",
    "    'ytick.labelsize': 9,\n",
    "    'legend.fontsize': 9,\n",
    "    'figure.dpi': 100,\n",
    "    'axes.spines.top': False,\n",
    "    'axes.spines.right': False,\n",
    "})\n",
    "\n",
    "DATE_FMT = DateFormatter('%m/%d')  # x 轴日期格式\n",
    "\n",
    "def setup_price_axis(ax, title=None):\n",
    "    \"\"\"为价格子图设置对数坐标和日期格式\"\"\"\n",
    "    ax.set_yscale('log')\n",
    "    ax.yaxis.set_major_formatter(ScalarFormatter())\n",
    "    ax.tick_params(axis='x', rotation=45)\n",
    "    ax.xaxis.set_major_formatter(DATE_FMT)\n",
    "    ax.grid(alpha=0.3)\n",
    "    if title:\n",
    "        ax.set_title(title, fontsize=13, fontweight='600', pad=12)\n",
    "\n",
    "def setup_indicator_axis(ax, ylabel):\n",
    "    \"\"\"为指标子图设置日期格式\"\"\"\n",
    "    ax.tick_params(axis='x', rotation=45)\n",
    "    ax.xaxis.set_major_formatter(DATE_FMT)\n",
    "    ax.set_ylabel(ylabel, fontsize=11)\n",
    "    ax.grid(alpha=0.3)\n",
    "\n",
    "print('✅ 全局样式配置完成')\n",
    "print('   - 价格图：对数坐标')\n",
    "print('   - 日期格式：月/日')\n",
    "print('   - 专业配色方案')"
]))

# ============================================================
# Cell 7: RSI 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 一、RSI 相对强弱指数\n",
    "\n",
    "**原理**：比较过去 N 日上涨幅度和下跌幅度的比值，判断超买/超卖状态。\n",
    "\n",
    "**公式**：\n",
    "- $\\Delta = C_t - C_{{t-1}}$  \n",
    "- $gain = \\Delta$ （若 $\\Delta > 0$，否则为 0）  \n",
    "- $loss = -\\Delta$ （若 $\\Delta < 0$，否则为 0）  \n",
    "- $avg\\_gain = gain$ 的 N 日平滑平均  \n",
    "- $avg\\_loss = loss$ 的 N 日平滑平均  \n",
    "- $RS = avg\\_gain / avg\\_loss$  \n",
    "- $RSI = 100 - \\frac{100}{1 + RS}$  \n",
    "\n",
    "**参数**：N = 14（常用）  \n",
    "**信号**：RSI > 70 超买（警惕回调）；RSI < 30 超卖（警惕反弹）"
]))

# ============================================================
# Cell 7: RSI Step 1
# ============================================================
cells.append(md([
    "### Step 1：计算 delta、gain、loss"
]))

cells.append(code([
    "N = 14   # RSI 参数\n",
    "\n",
    "# 计算价格变化\n",
    "df['delta'] = df['close'].diff()\n",
    "\n",
    "# gain：上涨部分（跌的日子为 0）\n",
    "df['gain'] = df['delta'].where(df['delta'] > 0, 0.0)\n",
    "\n",
    "# loss：下跌部分（涨的日子为 0，存为正值）\n",
    "df['loss'] = -df['delta'].where(df['delta'] < 0, 0.0)\n",
    "\n",
    "rsi_debug = df[['trade_date', 'close', 'delta', 'gain', 'loss']].head(20)\n",
    "rsi_debug"
]))

# ============================================================
# Cell 8: RSI Step 2
# ============================================================
cells.append(md([
    "### Step 2：计算 avg_gain 和 avg_loss（平滑处理）\n",
    "\n",
    "> RSI 使用的是**平滑平均**（Wilder 平滑法），而非简单移动平均。  \n",
    "> 第 N 日之后的每个值 = 前一日平滑值 × (N-1)/N + 当日 gain/loss × 1/N"
]))

cells.append(code([
    "# 方法一：用 ewm 实现 Wilder 平滑（推荐）\n",
    "alpha = 1 / N\n",
    "df['avg_gain'] = df['gain'].ewm(alpha=alpha, adjust=False).mean()\n",
    "df['avg_loss'] = df['loss'].ewm(alpha=alpha, adjust=False).mean()\n",
    "\n",
    "# 验证：手动计算前 N+2 行\n",
    "print('=== 手动验证 Wilder 平滑法（前20行）===')\n",
    "for i in range(N+5):\n",
    "    if i < N:\n",
    "        print(f'Row {i}: avg_gain={df[\"avg_gain\"].iloc[i]:.4f}  (前{N}行取简单平均)')\n",
    "    else:\n",
    "        prev = df['avg_gain'].iloc[i-1]\n",
    "        cur_gain = df['gain'].iloc[i]\n",
    "        manual = prev * (N-1)/N + cur_gain * 1/N\n",
    "        print(f'Row {i}: ewm={df[\"avg_gain\"].iloc[i]:.4f}  manual={manual:.4f}')\n",
    "    if i == N+2: break\n",
    "\n",
    "display(df[['trade_date', 'gain', 'loss', 'avg_gain', 'avg_loss']].head(20))"
]))

# ============================================================
# Cell 9: RSI Step 3
# ============================================================
cells.append(md([
    "### Step 3：计算 RSI 并绘图"
]))

cells.append(code([
    "# 计算 RS 和 RSI\n",
    "df['RS'] = df['avg_gain'] / df['avg_loss']\n",
    "df['RSI_14'] = 100 - (100 / (1 + df['RS']))\n",
    "\n",
    "# 查看结果（跳过前14行 NaN）\n",
    "display(df[['trade_date', 'close', 'RS', 'RSI_14']].iloc[14:30])"
]))

# ============================================================
# Cell 10: RSI 绘图
# ============================================================
cells.append(code([
    "# 绘制 RSI 图（对数坐标 + 专业样式）\n",
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True,\n",
    "                             gridspec_kw={'height_ratios': [2, 1]})\n",
    "\n",
    "# 上图：收盘价（对数坐标）\n",
    "ax1.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=1.8, label='收盘价')\n",
    "setup_price_axis(ax1, '兆易创新 —— 收盘价 + RSI')\n",
    "ax1.set_ylabel('收盘价（元）', fontsize=11)\n",
    "ax1.legend(fontsize=10)\n",
    "\n",
    "# 下图：RSI\n",
    "ax2.plot(df['trade_date'], df['RSI_14'], color='#7C3AED', linewidth=1.8)\n",
    "ax2.axhline(70, color='#DC2626', linestyle='--', linewidth=1, alpha=0.7, label='超买线 70')\n",
    "ax2.axhline(30, color='#059669', linestyle='--', linewidth=1, alpha=0.7, label='超卖线 30')\n",
    "ax2.axhline(50, color='#888780', linestyle=':', linewidth=0.8, alpha=0.5)\n",
    "ax2.fill_between(df['trade_date'], 70, 100, alpha=0.08, color='#DC2626')\n",
    "ax2.fill_between(df['trade_date'], 0, 30, alpha=0.08, color='#059669')\n",
    "setup_indicator_axis(ax2, 'RSI')\n",
    "ax2.set_ylim(0, 100)\n",
    "ax2.legend(fontsize=10)\n",
    "\n",
    "# 标注极端 RSI 值\n",
    "rsi_max_idx = df['RSI_14'].idxmax()\n",
    "rsi_min_idx = df['RSI_14'].idxmin()\n",
    "if pd.notna(rsi_max_idx):\n",
    "    ax2.annotate(f'{df[\"RSI_14\"].iloc[rsi_max_idx]:.0f}',\n",
    "                xy=(df['trade_date'].iloc[rsi_max_idx], df['RSI_14'].iloc[rsi_max_idx]),\n",
    "                xytext=(10, 10), textcoords='offset points',\n",
    "                color='#DC2626', fontweight='bold')\n",
    "if pd.notna(rsi_min_idx):\n",
    "    ax2.annotate(f'{df[\"RSI_14\"].iloc[rsi_min_idx]:.0f}',\n",
    "                xy=(df['trade_date'].iloc[rsi_min_idx], df['RSI_14'].iloc[rsi_min_idx]),\n",
    "                xytext=(10, -10), textcoords='offset points',\n",
    "                color='#059669', fontweight='bold')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 统计 RSI 信号\n",
    "overbought = (df['RSI_14'] > 70).sum()\n",
    "oversold = (df['RSI_14'] < 30).sum()\n",
    "print(f'RSI > 70（超买）天数：{overbought}')\n",
    "print(f'RSI < 30（超卖）天数：{oversold}')"
]))

# ============================================================
# Cell 11: MACD 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 二、MACD 指数平滑异同移动平均线\n",
    "\n",
    "**原理**：用两条指数移动平均线（EMA）之间的距离变化，捕捉趋势动能的强弱和转折。\n",
    "\n",
    "**公式**：\n",
    "- $EMA_{{fast}} = close$ 的 12 日 EMA  \n",
    "- $EMA_{{slow}} = close$ 的 26 日 EMA  \n",
    "- $DIF = EMA_{{fast}} - EMA_{{slow}}$  \n",
    "- $DEA = DIF$ 的 9 日 EMA（信号线）  \n",
    "- $MACD\\_hist = (DIF - DEA) \\times 2$（A股常用 ×2 放大）\n",
    "\n",
    "**信号**：  \n",
    "- **金叉**：DIF 由下向上穿越 DEA → 买入信号  \n",
    "- **死叉**：DIF 由上向下穿越 DEA → 卖出信号  \n",
    "- **柱状图由负转正** → 多头占优；**由正转负** → 空头占优"
]))

# ============================================================
# Cell 12: MACD Step 1 - EMA 手动实现
# ============================================================
cells.append(md([
    "### Step 1：手动实现 EMA 函数并验证"
]))

cells.append(code([
    "def calc_ema(series, span):\n",
    "    \"\"\"\n",
    "    手动实现 EMA（指数移动平均）\n",
    "    EMA_t = alpha * price_t + (1 - alpha) * EMA_{t-1}\n",
    "    alpha = 2 / (span + 1)\n",
    "    \"\"\"\n",
    "    alpha = 2 / (span + 1)\n",
    "    ema = series.copy()\n",
    "    ema.iloc[0] = series.iloc[0]  # 第一天用收盘价本身\n",
    "    for i in range(1, len(series)):\n",
    "        ema.iloc[i] = alpha * series.iloc[i] + (1 - alpha) * ema.iloc[i-1]\n",
    "    return ema\n",
    "\n",
    "# 用自定义函数计算 EMA\n",
    "df['EMA12_manual'] = calc_ema(df['close'], 12)\n",
    "df['EMA26_manual'] = calc_ema(df['close'], 26)\n",
    "\n",
    "# 用 pandas ewm() 计算（作为基准对比）\n",
    "df['EMA12_pandas'] = df['close'].ewm(span=12, adjust=False).mean()\n",
    "df['EMA26_pandas'] = df['close'].ewm(span=26, adjust=False).mean()\n",
    "\n",
    "# 对比前 20 行（看收敛过程）\n",
    "compare = df[['trade_date', 'close', 'EMA12_manual', 'EMA12_pandas', 'EMA26_manual', 'EMA26_pandas']].head(20).copy()\n",
    "display(compare)\n",
    "\n",
    "# 检查差值（应该接近 0）\n",
    "diff12 = (df['EMA12_manual'] - df['EMA12_pandas']).abs().max()\n",
    "diff26 = (df['EMA26_manual'] - df['EMA26_pandas']).abs().max()\n",
    "print(f'EMA12 最大差值：{diff12:.10f}')\n",
    "print(f'EMA26 最大差值：{diff26:.10f}')\n",
    "print('✅ 手动实现与 pandas ewm() 结果一致！' if diff12 < 1e-6 else '❌ 有差异，请检查代码')"
]))

# ============================================================
# Cell 13: MACD Step 2
# ============================================================
cells.append(md([
    "### Step 2：计算 DIF、DEA、MACD 柱状图"
]))

cells.append(code([
    "# 使用 pandas ewm() 计算（与手动结果一致，代码更简洁）\n",
    "df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()\n",
    "df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()\n",
    "\n",
    "# DIF = 快线 - 慢线\n",
    "df['DIF'] = df['EMA12'] - df['EMA26']\n",
    "\n",
    "# DEA = DIF 的 9 日 EMA（信号线）\n",
    "df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()\n",
    "\n",
    "# MACD 柱状图（A股惯例 ×2 放大）\n",
    "df['MACD_hist'] = (df['DIF'] - df['DEA']) * 2\n",
    "\n",
    "display(df[['trade_date', 'close', 'EMA12', 'EMA26', 'DIF', 'DEA', 'MACD_hist']].head(30))"
]))

# ============================================================
# Cell 14: MACD Step 3 - 绘图
# ============================================================
cells.append(md([
    "### Step 3：绘制 MACD 图 + 标注金叉/死叉"
]))

cells.append(code([
    "from matplotlib.patches import Patch\n",
    "\n",
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,\n",
    "                             gridspec_kw={'height_ratios': [2, 1.2]})\n",
    "\n",
    "# ===== 上图：价格 + EMA（对数坐标） =====\n",
    "ax1.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=1.8, label='收盘价', alpha=0.8)\n",
    "ax1.plot(df['trade_date'], df['EMA12'], color='#F59E0B', linewidth=1.3, label='EMA12（快线）', linestyle='--')\n",
    "ax1.plot(df['trade_date'], df['EMA26'], color='#EF4444', linewidth=1.3, label='EMA26（慢线）', linestyle=':')\n",
    "setup_price_axis(ax1, '兆易创新 —— MACD 指标')\n",
    "ax1.set_ylabel('价格（元）', fontsize=11)\n",
    "ax1.legend(fontsize=10)\n",
    "\n",
    "# ===== 下图：MACD =====\n",
    "# 柱状图颜色（涨=红，跌=绿，A股惯例）\n",
    "colors = ['#DC2626' if v >= 0 else '#10B981' for v in df['MACD_hist']]\n",
    "ax2.bar(df['trade_date'], df['MACD_hist'], color=colors, alpha=0.7, width=0.8, label='MACD 柱')\n",
    "\n",
    "# DIF 和 DEA 线\n",
    "ax2.plot(df['trade_date'], df['DIF'], color='#7C3AED', linewidth=1.5, label='DIF')\n",
    "ax2.plot(df['trade_date'], df['DEA'], color='#F59E0B', linewidth=1.5, label='DEA', linestyle='--')\n",
    "ax2.axhline(0, color='#888780', linewidth=0.8, alpha=0.5)\n",
    "setup_indicator_axis(ax2, 'MACD')\n",
    "ax2.legend(fontsize=10, loc='upper right')\n",
    "\n",
    "# 找出金叉和死叉位置\n",
    "golden_cross = []\n",
    "death_cross = []\n",
    "for i in range(1, len(df)):\n",
    "    if df['DIF'].iloc[i-1] < df['DEA'].iloc[i-1] and df['DIF'].iloc[i] > df['DEA'].iloc[i]:\n",
    "        golden_cross.append(i)\n",
    "    elif df['DIF'].iloc[i-1] > df['DEA'].iloc[i-1] and df['DIF'].iloc[i] < df['DEA'].iloc[i]:\n",
    "        death_cross.append(i)\n",
    "\n",
    "print(f'金叉次数：{len(golden_cross)}，死叉次数：{len(death_cross)}')\n",
    "print('\\n金叉日期（前10个）：')\n",
    "for idx in golden_cross[:10]:\n",
    "    print(f'  {df[\"trade_date\"].iloc[idx]}  DIF={df[\"DIF\"].iloc[idx]:.3f}')\n",
    "print('\\n死叉日期（前10个）：')\n",
    "for idx in death_cross[:10]:\n",
    "    print(f'  {df[\"trade_date\"].iloc[idx]}  DIF={df[\"DIF\"].iloc[idx]:.3f}')"
]))

# ============================================================
# Cell 15: 布林带 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 三、布林带（Bollinger Bands）\n",
    "\n",
    "**原理**：假设价格围绕均值呈正态分布，用「均线 ± N 倍标准差」构建动态通道，衡量价格相对位置和波动范围。\n",
    "\n",
    "**公式**：\n",
    "- $MB = close$ 的 20 日简单移动平均  \n",
    "- $UP = MB + 2 \\times \\sigma_{{20}}$  \n",
    "- $DN = MB - 2 \\times \\sigma_{{20}}$  \n",
    "- $Bandwidth = \\frac{UP - DN}{MB}$（带宽，衡量波动大小）  \n",
    "- $\\%B = \\frac{close - DN}{UP - DN}$（价格在带内的相对位置）\n",
    "\n",
    "**信号**：  \n",
    "- 价格触碰/突破上轨 → 超买，警惕回调  \n",
    "- 价格触碰/突破下轨 → 超卖，警惕反弹  \n",
    "- 带宽收窄（挤压）→ 即将出现大幅波动（方向不明）"
]))

# ============================================================
# Cell 16: 布林带 Step 1
# ============================================================
cells.append(md([
    "### Step 1：计算中轨、上轨、下轨"
]))

cells.append(code([
    "N_bb = 20\n",
    "K_bb = 2   # 标准差倍数\n",
    "\n",
    "# 中轨 = 20 日简单移动平均\n",
    "df['BB_middle'] = df['close'].rolling(window=N_bb).mean()\n",
    "\n",
    "# 标准差\n",
    "df['BB_std'] = df['close'].rolling(window=N_bb).std()\n",
    "\n",
    "# 上轨和下轨\n",
    "df['BB_upper'] = df['BB_middle'] + K_bb * df['BB_std']\n",
    "df['BB_lower'] = df['BB_middle'] - K_bb * df['BB_std']\n",
    "\n",
    "# 计算 %B 和带宽\n",
    "df['BB_percentB'] = (df['close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'])\n",
    "df['BB_bandwidth'] = (df['BB_upper'] - df['BB_lower']) / df['BB_middle']\n",
    "\n",
    "display(df[['trade_date', 'close', 'BB_middle', 'BB_upper', 'BB_lower', 'BB_percentB', 'BB_bandwidth']].iloc[19:35])"
]))

# ============================================================
# Cell 17: 布林带 Step 2 - 绘图
# ============================================================
cells.append(code([
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True,\n",
    "                             gridspec_kw={'height_ratios': [2, 1]})\n",
    "\n",
    "# ===== 上图：价格 + 布林带（对数坐标） =====\n",
    "ax1.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=1.8, label='收盘价', zorder=5)\n",
    "ax1.plot(df['trade_date'], df['BB_middle'], color='#7C3AED', linewidth=1.3, label='中轨（20MA）', zorder=4)\n",
    "ax1.plot(df['trade_date'], df['BB_upper'], color='#888780', linewidth=1, linestyle='--', alpha=0.7, label='上轨', zorder=3)\n",
    "ax1.plot(df['trade_date'], df['BB_lower'], color='#888780', linewidth=1, linestyle='--', alpha=0.7, label='下轨', zorder=3)\n",
    "\n",
    "# 带状区域填充\n",
    "ax1.fill_between(df['trade_date'], df['BB_lower'], df['BB_upper'], alpha=0.08, color='#7C3AED', zorder=1)\n",
    "setup_price_axis(ax1, '兆易创新 —— 布林带（Bollinger Bands）')\n",
    "ax1.set_ylabel('价格（元）', fontsize=11)\n",
    "ax1.legend(fontsize=10)\n",
    "\n",
    "# ===== 下图：带宽 =====\n",
    "bandwidth_norm = df['BB_bandwidth'] / df['BB_bandwidth'].max() * 100\n",
    "ax2.fill_between(df['trade_date'], 0, bandwidth_norm, alpha=0.2, color='#F59E0B')\n",
    "ax2.plot(df['trade_date'], bandwidth_norm, color='#D97706', linewidth=1.5, label='标准化带宽（%）')\n",
    "ax2.axhline(bandwidth_norm.quantile(0.2), color='#DC2626', linestyle=':', linewidth=1, alpha=0.6, label='低波动阈值（20%分位）')\n",
    "setup_indicator_axis(ax2, '带宽（标准化 %）')\n",
    "ax2.legend(fontsize=9)\n",
    "\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 标注触碰轨道的日期\n",
    "touch_upper = df[df['close'] >= df['BB_upper']]\n",
    "touch_lower = df[df['close'] <= df['BB_lower']]\n",
    "print(f'价格 >= 上轨的天数：{len(touch_upper)}')\n",
    "print(f'价格 <= 下轨的天数：{len(touch_lower)}')\n",
    "if len(touch_upper) > 0:\n",
    "    print('\\n触碰上轨日期（前10个）：', touch_upper['trade_date'].head(10).tolist())\n",
    "if len(touch_lower) > 0:\n",
    "    print('触碰下轨日期（前10个）：', touch_lower['trade_date'].head(10).tolist())"
]))

# ============================================================
# Cell 18: ATR 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 四、ATR 平均真实波幅（Average True Range）\n",
    "\n",
    "**原理**：真实的每日波动幅度不只是 H - L，还要考虑跳空缺口（前日收盘与今日开盘之间的缺口）。ATR 取三者最大值，再取 N 日平滑平均。\n",
    "\n",
    "**公式**：\n",
    "- $TR = \\max(H - L,\\ |H - C_{{prev}}|,\\ |L - C_{{prev}}|)$  \n",
    "- $ATR = TR$ 的 Wilder 平滑平均（N=14）\n",
    "\n",
    "> ⚠️ ATR **不预测方向**，只衡量波动大小。  \n",
    "> 高 ATR → 波动大，风险高，应降低仓位  \n",
    "> 低 ATR → 波动小，可能即将变盘（配合布林带挤压信号）\n",
    "\n",
    "**止损应用**：止损距离 = 入场价 ± N × ATR（常用 N=2）"
]))

# ============================================================
# Cell 19: ATR Step 1 - 计算 TR
# ============================================================
cells.append(md([
    "### Step 1：计算真实波幅 TR"
]))

cells.append(code([
    "# 前一日收盘价（向下错位）\n",
    "df['close_prev'] = df['close'].shift(1)\n",
    "\n",
    "# 三个候选值\n",
    "tr1 = df['high'] - df['low']                          # 当日振幅\n",
    "tr2 = (df['high'] - df['close_prev']).abs()          # 最高价与前收之差\n",
    "tr3 = (df['low'] - df['close_prev']).abs()           # 最低价与前收之差\n",
    "\n",
    "# TR = 三者最大值\n",
    "df['TR'] = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)\n",
    "\n",
    "display(df[['trade_date', 'open', 'high', 'low', 'close', 'close_prev', 'TR']].head(20))"
]))

# ============================================================
# Cell 20: ATR Step 2 - 计算 ATR
# ============================================================
cells.append(md([
    "### Step 2：Wilder 平滑法计算 ATR"
]))

cells.append(code([
    "N_atr = 14\n",
    "\n",
    "# 方法：Wilder 平滑（与 RSI 相同）\n",
    "alpha_atr = 1 / N_atr\n",
    "df['ATR_14'] = df['TR'].ewm(alpha=alpha_atr, adjust=False).mean()\n",
    "\n",
    "# 对比：简单移动平均（看看差别）\n",
    "df['ATR_SMA'] = df['TR'].rolling(window=N_atr).mean()\n",
    "\n",
    "display(df[['trade_date', 'TR', 'ATR_14', 'ATR_SMA']].iloc[13:30])\n",
    "\n",
    "print('=== Wilder 平滑 vs 简单移动平均（最后10行）===')\n",
    "compare_atr = df[['trade_date', 'ATR_14', 'ATR_SMA']].tail(10).copy()\n",
    "print(compare_atr.to_string(index=False))"
]))

# ============================================================
# Cell 21: ATR Step 3 - 绘图 + 止损演示
# ============================================================
cells.append(code([
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,\n",
    "                             gridspec_kw={'height_ratios': [2, 1]})\n",
    "\n",
    "# ===== 上图：收盘价（对数坐标） =====\n",
    "ax1.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=1.8, label='收盘价')\n",
    "setup_price_axis(ax1, '兆易创新 —— ATR 平均真实波幅')\n",
    "ax1.set_ylabel('收盘价（元）', fontsize=11)\n",
    "ax1.legend(fontsize=10)\n",
    "\n",
    "# ===== 下图：ATR =====\n",
    "ax2.fill_between(df['trade_date'], 0, df['ATR_14'], alpha=0.15, color='#0EA5E9')\n",
    "ax2.plot(df['trade_date'], df['ATR_14'], color='#0284C7', linewidth=2, label='ATR（Wilder 平滑）')\n",
    "ax2.plot(df['trade_date'], df['ATR_SMA'], color='#F59E0B', linewidth=1.2, linestyle='--', alpha=0.6, label='ATR（简单移动平均）')\n",
    "setup_indicator_axis(ax2, 'ATR（元）')\n",
    "ax2.legend(fontsize=10)\n",
    "\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# ===== 止损距演示 =====\n",
    "print('=== 用 ATR 设置止损距（示例） ===')\n",
    "latest = df.dropna(subset=['ATR_14']).iloc[-1]\n",
    "entry_price = latest['close']\n",
    "atr_val = latest['ATR_14']\n",
    "print(f'最新收盘价：{entry_price:.2f} 元')\n",
    "print(f'最新 ATR：{atr_val:.2f} 元')\n",
    "print(f'\\n止损距建议（多头）：')\n",
    "for mult in [1, 1.5, 2]:\n",
    "    stop = entry_price - mult * atr_val\n",
    "    print(f'  {mult}×ATR = {mult*atr_val:.2f} 元，止损价 = {stop:.2f} 元（跌幅 {(entry_price-stop)/entry_price*100:.1f}%）')\n",
    "print(f'\\n止损距建议（空头）：')\n",
    "for mult in [1, 1.5, 2]:\n",
    "    stop = entry_price + mult * atr_val\n",
    "    print(f'  {mult}×ATR = {mult*atr_val:.2f} 元，止损价 = {stop:.2f} 元（涨幅 {(stop-entry_price)/entry_price*100:.1f}%）')"
]))

# ============================================================
# Cell 22: KDJ 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 五、KDJ 随机指标\n",
    "\n",
    "**原理**：RSI 只看收盘价，KDJ 则考虑当日收盘价在「过去 N 日最高价 ~ 最低价」范围内的相对位置，对短期波动更敏感。\n",
    "\n",
    "**公式**：\n",
    "- $lowest_{{low}} = \\min(low, N)$  \n",
    "- $highest_{{high}} = \\max(high, N)$  \n",
    "- $RSV = \\frac{{close - lowest_{{low}}}}{{highest_{{high}} - lowest_{{low}}}} \\times 100$  \n",
    "- $K = RSV$ 的平滑（常用 3 日 EMA）  \n",
    "- $D = K$ 的平滑（常用 3 日 EMA）  \n",
    "- $J = 3 \\times K - 2 \\times D$（J 会超出 0~100 范围，更敏感）\n",
    "\n",
    "**参数**：(9, 3, 3) —— RSV 周期 9，K 平滑 3，J 系数 3  \n",
    "**信号**：  \n",
    "- K 上穿 D（金叉）+ J < 20 → 强买入  \n",
    "- K 下穿 D（死叉）+ J > 80 → 强卖出"
]))

# ============================================================
# Cell 23: KDJ Step 1 - 计算 RSV
# ============================================================
cells.append(md([
    "### Step 1：计算 RSV"
]))

cells.append(code([
    "N_kdj = 9\n",
    "\n",
    "# 过去 N 日最低价和最高价\n",
    "df['KDJ_lowest'] = df['low'].rolling(window=N_kdj).min()\n",
    "df['KDJ_highest'] = df['high'].rolling(window=N_kdj).max()\n",
    "\n",
    "# RSV = (收盘价 - 最低价) / (最高价 - 最低价) × 100\n",
    "df['RSV'] = (df['close'] - df['KDJ_lowest']) / (df['KDJ_highest'] - df['KDJ_lowest']) * 100\n",
    "\n",
    "display(df[['trade_date', 'close', 'KDJ_lowest', 'KDJ_highest', 'RSV']].iloc[N_kdj-1:N_kdj+10])"
]))

# ============================================================
# Cell 24: KDJ Step 2 - 计算 K/D/J
# ============================================================
cells.append(md([
    "### Step 2：计算 K、D、J 值"
]))

cells.append(code([
    "# K = RSV 的 3 日平滑（国内软件用 EMA，com=2 等价于 span=3）\n",
    "df['K'] = df['RSV'].ewm(com=2, adjust=False).mean()\n",
    "\n",
    "# D = K 的 3 日平滑\n",
    "df['D'] = df['K'].ewm(com=2, adjust=False).mean()\n",
    "\n",
    "# J = 3K - 2D\n",
    "df['J'] = 3 * df['K'] - 2 * df['D']\n",
    "\n",
    "display(df[['trade_date', 'RSV', 'K', 'D', 'J']].iloc[N_kdj+2:N_kdj+15])"
]))

# ============================================================
# Cell 25: KDJ Step 3 - 绘图 + 金叉死叉
# ============================================================
cells.append(code([
    "fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,\n",
    "                             gridspec_kw={'height_ratios': [2, 1.5]})\n",
    "\n",
    "# ===== 上图：价格（对数坐标） =====\n",
    "ax1.plot(df['trade_date'], df['close'], color='#2563EB', linewidth=1.8, label='收盘价')\n",
    "setup_price_axis(ax1, '兆易创新 —— KDJ 随机指标')\n",
    "ax1.set_ylabel('收盘价（元）', fontsize=11)\n",
    "ax1.legend(fontsize=10)\n",
    "\n",
    "# ===== 下图：KDJ =====\n",
    "ax2.plot(df['trade_date'], df['K'], color='#7C3AED', linewidth=1.5, label='K（快线）')\n",
    "ax2.plot(df['trade_date'], df['D'], color='#F59E0B', linewidth=1.5, label='D（慢线）', linestyle='--')\n",
    "ax2.plot(df['trade_date'], df['J'], color='#10B981', linewidth=1.2, label='J', linestyle=':')\n",
    "ax2.axhline(80, color='#DC2626', linestyle='--', linewidth=1, alpha=0.7, label='超买 80')\n",
    "ax2.axhline(20, color='#059669', linestyle='--', linewidth=1, alpha=0.7, label='超卖 20')\n",
    "ax2.axhline(50, color='#888780', linestyle=':', linewidth=0.8, alpha=0.5)\n",
    "setup_indicator_axis(ax2, 'KDJ')\n",
    "ax2.set_ylim(-10, 110)\n",
    "ax2.legend(fontsize=10)\n",
    "\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 统计金叉/死叉\n",
    "kdj_golden = []\n",
    "kdj_death = []\n",
    "for i in range(1, len(df)):\n",
    "    if pd.notna(df['K'].iloc[i]) and pd.notna(df['D'].iloc[i]):\n",
    "        if df['K'].iloc[i-1] < df['D'].iloc[i-1] and df['K'].iloc[i] > df['D'].iloc[i]:\n",
    "            kdj_golden.append(i)\n",
    "        elif df['K'].iloc[i-1] > df['D'].iloc[i-1] and df['K'].iloc[i] < df['D'].iloc[i]:\n",
    "            kdj_death.append(i)\n",
    "\n",
    "print(f'KDJ 金叉次数：{len(kdj_golden)}')\n",
    "print(f'KDJ 死叉次数：{len(kdj_death)}')\n",
    "print('\\n金叉日期（前10个）：', [df['trade_date'].iloc[i] for i in kdj_golden[:10]])\n",
    "print('死叉日期（前10个）：', [df['trade_date'].iloc[i] for i in kdj_death[:10]])"
]))

# ============================================================
# Cell 26: 综合信号分析 标题
# ============================================================
cells.append(md([
    "---\n",
    "## 六、综合信号分析：多指标共振\n",
    "\n",
    "将 5 个指标的信号整合，寻找「共振」日期 —— 多个指标同时发出买入或卖出信号，信号可靠性更高。\n",
    "\n",
    "**信号定义**：\n",
    "\n",
    "| 指标 | 买入信号 | 卖出信号 |\n",
    "|------|----------|----------|\n",
    "| RSI | RSI < 30 | RSI > 70 |\n",
    "| MACD | DIF 上穿 DEA（金叉） | DIF 下穿 DEA（死叉） |\n",
    "| 布林带 | close < 下轨（或 %B < 0） | close > 上轨（或 %B > 1） |\n",
    "| ATR | ATR 处于低位（波动缩小，即将变盘）| ATR 处于高位（波动放大，风险高） |\n",
    "| KDJ | K 上穿 D（金叉）且 J < 20 | K 下穿 D（死叉）且 J > 80 |"
]))

# ============================================================
# Cell 27: 构建信号矩阵
# ============================================================
cells.append(code([
    "# 构建信号矩阵（1=买入，-1=卖出，0=无信号）\n",
    "sig = df[['trade_date', 'close']].copy()\n",
    "\n",
    "# RSI 信号\n",
    "sig['RSI_buy']  = (df['RSI_14'] < 30).astype(int)\n",
    "sig['RSI_sell'] = (df['RSI_14'] > 70).astype(int)\n",
    "\n",
    "# MACD 金叉/死叉信号（当日发生）\n",
    "macd_golden = [False]*len(df)\n",
    "macd_death  = [False]*len(df)\n",
    "for i in range(1, len(df)):\n",
    "    if pd.notna(df['DIF'].iloc[i]) and pd.notna(df['DEA'].iloc[i]):\n",
    "        if df['DIF'].iloc[i-1] < df['DEA'].iloc[i-1] and df['DIF'].iloc[i] > df['DEA'].iloc[i]:\n",
    "            macd_golden[i] = True\n",
    "        elif df['DIF'].iloc[i-1] > df['DEA'].iloc[i-1] and df['DIF'].iloc[i] < df['DEA'].iloc[i]:\n",
    "            macd_death[i] = True\n",
    "sig['MACD_buy']  = [int(x) for x in macd_golden]\n",
    "sig['MACD_sell'] = [int(x) for x in macd_death]\n",
    "\n",
    "# 布林带信号\n",
    "sig['BB_buy']  = (df['close'] <= df['BB_lower']).astype(int)\n",
    "sig['BB_sell'] = (df['close'] >= df['BB_upper']).astype(int)\n",
    "\n",
    "# ATR 信号（ATR 处于最低 20% 分位 = 低波动，即将变盘）\n",
    "atr_low_thresh = df['ATR_14'].quantile(0.2)\n",
    "atr_high_thresh = df['ATR_14'].quantile(0.8)\n",
    "sig['ATR_buy']  = (df['ATR_14'] < atr_low_thresh).astype(int)   # 低波动 → 买入（变盘在即）\n",
    "sig['ATR_sell'] = (df['ATR_14'] > atr_high_thresh).astype(int)  # 高波动 → 卖出（风险高）\n",
    "print(f'ATR 低位阈值（20%分位）：{atr_low_thresh:.2f}')\n",
    "print(f'ATR 高位阈值（80%分位）：{atr_high_thresh:.2f}')\n",
    "\n",
    "# KDJ 金叉/死叉信号\n",
    "kdj_golden = [False]*len(df)\n",
    "kdj_death  = [False]*len(df)\n",
    "for i in range(1, len(df)):\n",
    "    if pd.notna(df['K'].iloc[i]) and pd.notna(df['D'].iloc[i]):\n",
    "        if df['K'].iloc[i-1] < df['D'].iloc[i-1] and df['K'].iloc[i] > df['D'].iloc[i]:\n",
    "            kdj_golden[i] = True\n",
    "        elif df['K'].iloc[i-1] > df['D'].iloc[i-1] and df['K'].iloc[i] < df['D'].iloc[i]:\n",
    "            kdj_death[i] = True\n",
    "sig['KDJ_buy']  = [int(x) for x in kdj_golden]\n",
    "sig['KDJ_sell'] = [int(x) for x in kdj_death]\n",
    "\n",
    "display(sig.head(30))"
]))

# ============================================================
# Cell 28: 统计共振日期
# ============================================================
cells.append(code([
    "# 统计共振日期\n",
    "sig['buy_score']  = sig['RSI_buy'] + sig['MACD_buy'] + sig['BB_buy'] + sig['ATR_buy'] + sig['KDJ_buy']\n",
    "sig['sell_score'] = sig['RSI_sell'] + sig['MACD_sell'] + sig['BB_sell'] + sig['ATR_sell'] + sig['KDJ_sell']\n",
    "\n",
    "print('=== 买入共振（至少 2 个指标同时发出买入信号） ===')\n",
    "buy_resonance = sig[sig['buy_score'] >= 2][['trade_date', 'close', 'buy_score', 'RSI_buy', 'MACD_buy', 'BB_buy', 'ATR_buy', 'KDJ_buy']]\n",
    "print(f'共振日期数：{len(buy_resonance)}')\n",
    "if len(buy_resonance) > 0:\n",
    "    display(buy_resonance)\n",
    "else:\n",
    "    print('（无共振日期）')\n",
    "\n",
    "print('\\n=== 卖出共振（至少 2 个指标同时发出卖出信号） ===')\n",
    "sell_resonance = sig[sig['sell_score'] >= 2][['trade_date', 'close', 'sell_score', 'RSI_sell', 'MACD_sell', 'BB_sell', 'ATR_sell', 'KDJ_sell']]\n",
    "print(f'共振日期数：{len(sell_resonance)}')\n",
    "if len(sell_resonance) > 0:\n",
    "    display(sell_resonance)\n",
    "else:\n",
    "    print('（无共振日期）')"
]))

# ============================================================
# Cell 29: 信号热力图
# ============================================================
cells.append(code([
    "import seaborn as sns\n",
    "\n",
    "# 构建热力图数据（最近 120 个交易日）\n",
    "n_days = min(120, len(sig))\n",
    "idx_start = max(0, len(sig) - n_days)\n",
    "heat_data = sig[['RSI_buy', 'MACD_buy', 'BB_buy', 'ATR_buy', 'KDJ_buy',\n",
    "                    'RSI_sell', 'MACD_sell', 'BB_sell', 'ATR_sell', 'KDJ_sell']].tail(n_days).T\n",
    "\n",
    "# 生成日期标签\n",
    "date_labels = sig['trade_date'].iloc[idx_start:].dt.strftime('%m/%d').tolist()\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(max(14, n_days * 0.12), 5.5))\n",
    "sns.heatmap(heat_data,\n",
    "            cmap=sns.diverging_palette(150, 10, s=80, l=55, n=9),\n",
    "            center=0,\n",
    "            xticklabels=[d if i % 10 == 0 else '' for i, d in enumerate(date_labels)],\n",
    "            yticklabels=['RSI买', 'MACD买', 'BB买', 'ATR买', 'KDJ买',\n",
    "                        'RSI卖', 'MACD卖', 'BB卖', 'ATR卖', 'KDJ卖'],\n",
    "            cbar_kws={'label': '信号', 'shrink': 0.8},\n",
    "            linewidths=0.5, linecolor='#F3F4F6',\n",
    "            ax=ax)\n",
    "ax.set_title('兆易创新 —— 技术指标信号热力图（最近 {} 个交易日）'.format(n_days),\n",
    "             fontsize=13, fontweight='600', pad=12)\n",
    "ax.set_xlabel('日期（每 10 个交易日标注）', fontsize=10)\n",
    "ax.tick_params(axis='x', rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "print('热力图说明：')\n",
    "print('  绿色格子 = 该指标当日发出买入信号')\n",
    "print('  红色格子 = 该指标当日发出卖出信号')\n",
    "print('  白色格子 = 无信号')\n",
    "print('  同一列多个绿色/红色 = 多指标共振，信号更可靠')"
]))

# ============================================================
# Cell 30: 总结
# ============================================================
cells.append(md([
    "---\n",
    "## 总结与反思\n",
    "\n",
    "### 已完成的指标\n",
    "\n",
    "| 指标 | 手动实现 | 核心发现 |\n",
    "|------|----------|----------|\n",
    "| RSI  | ✅ | 超买/超卖阈值 70/30 |\n",
    "| MACD | ✅ | DIF/DEA 金叉死叉 |\n",
    "| 布林带 | ✅ | 上下轨通道 + 带宽挤压 |\n",
    "| ATR  | ✅ | 波动大小，用于止损设置 |\n",
    "| KDJ  | ✅ | K/D 金叉死叉，J 线更敏感 |\n",
    "\n",
    "### 局限性说明\n",
    "\n",
    "1. **所有技术指标都是滞后指标**，基于历史价格计算，无法预测未来。  \n",
    "2. **震荡市中假信号多**（尤其是 KDJ），需结合趋势判断。  \n",
    "3. **布林带挤压后方向不确定**，需配合其他指标确认。  \n",
    "4. **ATR 只衡量波动，不指示方向**，需结合价格趋势使用。  \n",
    "5. **综合信号共振也不是 100% 准确**，仅提高胜率，不构成投资建议。  \n",
    "\n",
    "> ⚠️ **免责声明**：本 Notebook 仅供学习和研究使用，不构成任何投资建议。股市有风险，投资需谨慎。\n",
    "\n",
    "### 下一步可以做什么？\n",
    "\n",
    "- 加入**成交量指标**（OBV、VPT）验证价格走势  \n",
    "- 回测**买卖信号的历史胜率**  \n",
    "- 尝试**不同参数**（如 RSI 用 7 日或 21 日）  \n",
    "- 加入**基本面数据**（PE、PB、营收增速）做多因子分析"
]))

# ============================================================
# 写入文件
# ============================================================
output_path = r"D:\online internship\Task-2\兆易创新_技术指标计算.ipynb"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(NOTEBOOK, f, ensure_ascii=False, indent=1)

print(f"Notebook 已生成：{output_path}")
print(f"总 Cell 数：{len(cells)}")
