import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import matplotlib.font_manager as fm

# 字体加载
font_path = "msyhl.ttc"  # 微软雅黑字体文件，确保路径正确
my_font = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = my_font.get_name()
plt.rcParams['axes.unicode_minus'] = False

# --- 函数定义 ---

def draw_radar(labels, values, font_prop):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), dpi=100)

    # 网格线
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontproperties=font_prop)

    # 标签
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontproperties=font_prop, fontsize=12)

    # 渐变色填充实现（简单版）
    ax.plot(angles, values, color='magenta', linewidth=2, linestyle='solid', marker='o')
    ax.fill(angles, values, color='magenta', alpha=0.3)

    return fig, ax

def draw_risk_indicator(ax, risk_score):
    ax.axis('off')
    theta = risk_score * 360
    color = 'red' if risk_score > 0.6 else 'orange' if risk_score > 0.3 else 'green'

    # 环形进度条
    wedge = Wedge((0.5, 0.5), 0.5, 0, theta, facecolor=color)
    circle = Circle((0.5, 0.5), 0.35, facecolor='white', edgecolor='none')
    ax.add_patch(wedge)
    ax.add_patch(circle)

    ax.text(0.5, 0.5, f"{risk_score:.2f}", ha='center', va='center', fontsize=14, color=color, fontproperties=my_font)

def calculate_risk_score(attraction, emotional_dependence, idealization, rationality, external_feedback, red_flags_ratio):
    # 可以调整权重，这里是示例
    score = (attraction + emotional_dependence + idealization + red_flags_ratio) / 4 - (rationality + external_feedback) / 2
    return np.clip(score, 0, 1)

def risk_description(risk_score):
    if risk_score > 0.6:
        return ("⚠️ 高风险！建议谨慎对待，注意理性判断和外部意见。", "error")
    elif risk_score > 0.3:
        return ("⚠️ 中等风险，保持警惕，适度理性分析。", "warning")
    else:
        return ("✅ 风险较低，恋爱状态较为健康。", "success")

def reset_inputs():
    st.session_state['attraction'] = 0.9
    st.session_state['emotional_dependence'] = 0.8
    st.session_state['idealization'] = 0.85
    st.session_state['rationality'] = 0.4
    st.session_state['external_feedback'] = 0.6
    st.session_state['red_flag_1'] = True
    st.session_state['red_flag_2'] = False
    st.session_state['red_flag_3'] = False
    st.session_state['red_flag_4'] = True
    st.session_state['time_in_relationship'] = 3

# --- 主程序 ---

st.title("💖 恋爱脑风险评估器")

if 'attraction' not in st.session_state:
    reset_inputs()

with st.form("input_form"):
    st.header("📊 输入你的恋爱状态参数（0~1之间）")
    step = 0.05
    attraction = st.slider("被吸引程度", 0.0, 1.0, st.session_state['attraction'], step=step, key='attraction')
    emotional_dependence = st.slider("情感依赖", 0.0, 1.0, st.session_state['emotional_dependence'], step=step, key='emotional_dependence')
    idealization = st.slider("理想化滤镜", 0.0, 1.0, st.session_state['idealization'], step=step, key='idealization')
    rationality = st.slider("理性水平", 0.0, 1.0, st.session_state['rationality'], step=step, key='rationality')
    external_feedback = st.slider("家人朋友反馈", 0.0, 1.0, st.session_state['external_feedback'], step=step, key='external_feedback')

    st.header("🚩 红旗信号")
    red_flag_1 = st.checkbox("红旗 1：是否存在严重性格不合？", st.session_state['red_flag_1'], key='red_flag_1')
    red_flag_2 = st.checkbox("红旗 2：是否经常沟通不畅？", st.session_state['red_flag_2'], key='red_flag_2')
    red_flag_3 = st.checkbox("红旗 3：是否有经济纠纷？", st.session_state['red_flag_3'], key='red_flag_3')
    red_flag_4 = st.checkbox("红旗 4：是否有家庭反对？", st.session_state['red_flag_4'], key='red_flag_4')

    time_in_relationship = st.slider("交往时长（月）", 0, 24, st.session_state['time_in_relationship'], key='time_in_relationship')

    submitted = st.form_submit_button("计算风险")

    st.button("重置参数", on_click=reset_inputs)

if submitted:
    red_flags = [red_flag_1, red_flag_2, red_flag_3, red_flag_4]
    red_flags_ratio = sum(red_flags) / len(red_flags)

    labels = ['被吸引程度', '情感依赖', '理想化滤镜', '理性水平', '外部反馈', '红旗反比']
    values = [attraction, emotional_dependence, idealization, rationality, external_feedback, 1 - red_flags_ratio]

    risk_score = calculate_risk_score(attraction, emotional_dependence, idealization, rationality, external_feedback, red_flags_ratio)

    fig, ax = draw_radar(labels, values.copy(), my_font)

    # 添加风险环形指示器
    ax2 = fig.add_axes([0.75, 0.75, 0.15, 0.15], polar=True)
    draw_risk_indicator(ax2, risk_score)

    plt.figtext(0.5, 0.05, f"交往时长：{time_in_relationship} 个月", ha='center', fontsize=12, fontproperties=my_font)

    st.pyplot(fig)

    desc, level = risk_description(risk_score)
    if level == "error":
        st.error(desc)
    elif level == "warning":
        st.warning(desc)
    else:
        st.success(desc)

    st.write("---")
    st.write("*本工具基于简单参数计算，仅供娱乐与自我反思，不能代替专业心理咨询。*")

else:
    st.info("请调整参数并点击“计算风险”按钮查看结果。")
