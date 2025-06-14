import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
# 设置matplotlib中文字体和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']

st.set_page_config(page_title="恋爱脑风险评估器 💖🧠", layout="centered")

# --- 标题 ---
st.title("恋爱脑风险评估器 💖🧠")
st.write("调整下面的参数，评估你的恋爱脑风险指数。")

# --- 1. 用户输入区 ---
st.header("请输入你的恋爱状态参数（0~1之间）")

attraction = st.slider("被吸引程度 (Attraction)", 0.0, 1.0, 0.9)
emotional_dependence = st.slider("情感依赖 (Emotional Dependence)", 0.0, 1.0, 0.8)
idealization = st.slider("理想化 (Idealization)", 0.0, 1.0, 0.85)
rationality = st.slider("理性水平 (Rationality)", 0.0, 1.0, 0.4)
external_feedback = st.slider("外部反馈 (External Feedback)", 0.0, 1.0, 0.6)

st.header("红旗信号（勾选存在的红旗）")
red_flag_1 = st.checkbox("严重性格不合", value=True)
red_flag_2 = st.checkbox("经常沟通不畅", value=False)
red_flag_3 = st.checkbox("经济纠纷", value=False)
red_flag_4 = st.checkbox("家庭反对", value=True)
red_flags = [red_flag_1, red_flag_2, red_flag_3, red_flag_4]

time_in_relationship = st.slider("交往时长（月）", 0, 24, 3)

# --- 2. 计算部分 ---
red_flags_ratio = sum(red_flags) / len(red_flags)

# 用于雷达图的数据和标签
labels = ['被吸引程度', '情感依赖', '理想化', '理性水平', '外部反馈', '红旗信号（反向）']
values = [attraction, emotional_dependence, idealization, rationality, external_feedback, 1 - red_flags_ratio]
values += values[:1]  # 封闭环
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

# --- 3. 绘图 ---
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, values, 'o-', linewidth=2, color='purple')
ax.fill(angles, values, alpha=0.25, color='violet')
ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=11)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)

plt.figtext(0.5, 0.05, f"交往时长：{time_in_relationship} 个月", ha='center', fontsize=12)

# --- 4. 计算风险评分 ---
# 风险评分综合公式：越高越危险
risk_score = (attraction + emotional_dependence + idealization + red_flags_ratio) / 4 - (rationality + external_feedback) / 2
risk_score = np.clip(risk_score, 0, 1)

# --- 5. 绘制环形风险评分条 ---
ax2 = fig.add_axes([0.75, 0.75, 0.18, 0.18], polar=True)
ax2.axis('off')

theta1 = 0
theta2 = risk_score * 360
if risk_score > 0.6:
    color = '#FF4B4B'  # 红
elif risk_score > 0.3:
    color = '#FFA500'  # 橙
else:
    color = '#4CAF50'  # 绿

wedge = Wedge((0.5, 0.5), 0.5, theta1, theta2, facecolor=color, alpha=0.8)
ax2.add_patch(wedge)
ax2.text(0.5, 0.5, f"{risk_score:.2f}", ha='center', va='center', fontsize=12, fontweight='bold', color=color)

# 显示雷达图
st.pyplot(fig)
plt.close(fig)  # 释放内存

# --- 6. 文字输出风险分析 ---
st.header("风险分析结论")
if risk_score > 0.6:
    st.error("⚠️ 高风险！建议谨慎对待，注意理性判断和外部意见。")
elif risk_score > 0.3:
    st.warning("⚠️ 中等风险，保持警惕，适度理性分析。")
else:
    st.success("✅ 风险较低，恋爱状态较为健康。")

st.markdown(
    """
    ---
    *本工具基于简单参数计算，不能代替专业心理咨询，仅供娱乐与自我反思。*
    """
)
