import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import matplotlib.font_manager as fm

# 动态加载本地字体（确保仓库有 msyhl.ttc 文件）
font_path = "msyhl.ttc"  # 微软雅黑字体文件
my_font = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = my_font.get_name()
plt.rcParams['axes.unicode_minus'] = False

st.title("💖 恋爱脑风险评估器")

# 用session_state存储参数，方便重置
if "params" not in st.session_state:
    st.session_state.params = {
        "attraction": 0.9,
        "emotional_dependence": 0.8,
        "idealization": 0.85,
        "rationality": 0.4,
        "external_feedback": 0.6,
        "red_flag_1": True,
        "red_flag_2": False,
        "red_flag_3": False,
        "red_flag_4": True,
        "time_in_relationship": 3,
    }

def reset_inputs():
    st.session_state.params = {
        "attraction": 0.9,
        "emotional_dependence": 0.8,
        "idealization": 0.85,
        "rationality": 0.4,
        "external_feedback": 0.6,
        "red_flag_1": True,
        "red_flag_2": False,
        "red_flag_3": False,
        "red_flag_4": True,
        "time_in_relationship": 3,
    }
    st.experimental_rerun()  # 重置后刷新页面

with st.form("input_form"):
    st.header("📊 输入你的恋爱状态参数（0~1之间）")

    attraction = st.slider("被吸引程度", 0.0, 1.0, st.session_state.params["attraction"], key="attraction")
    emotional_dependence = st.slider("情感依赖", 0.0, 1.0, st.session_state.params["emotional_dependence"], key="emotional_dependence")
    idealization = st.slider("理想化滤镜", 0.0, 1.0, st.session_state.params["idealization"], key="idealization")
    rationality = st.slider("理性水平", 0.0, 1.0, st.session_state.params["rationality"], key="rationality")
    external_feedback = st.slider("家人朋友反馈", 0.0, 1.0, st.session_state.params["external_feedback"], key="external_feedback")

    st.header("🚩 红旗信号")
    red_flag_1 = st.checkbox("红旗 1：是否存在严重性格不合？", value=st.session_state.params["red_flag_1"], key="red_flag_1")
    red_flag_2 = st.checkbox("红旗 2：是否经常沟通不畅？", value=st.session_state.params["red_flag_2"], key="red_flag_2")
    red_flag_3 = st.checkbox("红旗 3：是否有经济纠纷？", value=st.session_state.params["red_flag_3"], key="red_flag_3")
    red_flag_4 = st.checkbox("红旗 4：是否有家庭反对？", value=st.session_state.params["red_flag_4"], key="red_flag_4")

    time_in_relationship = st.slider("交往时长（月）", 0, 24, st.session_state.params["time_in_relationship"], key="time_in_relationship")

    submitted = st.form_submit_button("计算风险")

# 重置按钮放form外，防止回调错误
st.button("重置参数", on_click=reset_inputs)

if submitted:
    # 计算部分
    red_flags = [red_flag_1, red_flag_2, red_flag_3, red_flag_4]
    red_flags_ratio = sum(red_flags) / len(red_flags)

    labels = ['被吸引程度', '情感依赖', '理想化滤镜', '理性水平', '外部反馈', '红旗反比']
    values = [attraction, emotional_dependence, idealization, rationality, external_feedback, 1 - red_flags_ratio]
    values += values[:1]  # 闭合雷达图

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # 绘制雷达图
    fig = plt.figure(figsize=(6, 6), dpi=100)
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles, values, color='magenta', linewidth=2, linestyle='solid', marker='o')
    ax.fill(angles, values, color='magenta', alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontproperties=my_font, fontsize=12)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontproperties=my_font)

    plt.figtext(0.5, 0.05, f"交往时长：{time_in_relationship} 个月", ha='center', fontsize=12, fontproperties=my_font)

    # 计算风险分数
    risk_score = (attraction + emotional_dependence + idealization + red_flags_ratio) / 4 - (rationality + external_feedback) / 2
    risk_score = np.clip(risk_score, 0, 1)

    # 风险指示器
    ax2 = fig.add_axes([0.75, 0.75, 0.15, 0.15], polar=True)
    ax2.axis('off')
    theta1 = 0
    theta2 = risk_score * 360
    color = 'red' if risk_score > 0.6 else 'orange' if risk_score > 0.3 else 'green'
    wedge = Wedge((0.5, 0.5), 0.5, theta1, theta2, facecolor=color)
    ax2.add_patch(wedge)
    ax2.text(0.5, 0.5, f"风险\n{risk_score:.2f}", ha='center', va='center', fontsize=10, color=color, fontproperties=my_font)

    st.pyplot(fig)

    # 风险分析结论
    st.header("📋 风险分析结论")
    if risk_score > 0.6:
        st.error("⚠️ 高风险！建议谨慎对待，注意理性判断和外部意见。")
    elif risk_score > 0.3:
        st.warning("⚠️ 中等风险，保持警惕，适度理性分析。")
    else:
        st.success("✅ 风险较低，恋爱状态较为健康。")

    st.write("""
    ---
    *本工具基于简单参数计算，仅供娱乐与自我反思，不能代替专业心理咨询。*
    """)
else:
    st.info("请调整参数并点击“计算风险”按钮查看结果。")
