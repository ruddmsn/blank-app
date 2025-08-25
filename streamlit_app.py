import streamlit as st

# -----------------------------
# MBTI 학습 유형 진단 (Streamlit)
# 파일명: streamlit_app.py
# -----------------------------

st.set_page_config(page_title="MBTI 학습 유형 진단", page_icon="🧭", layout="centered")
st.title("MBTI 학습 유형 진단")
st.caption("간단한 문항에 응답하면, 당신의 **MBTI 경향**과 **추천 학습 방식**을 알려드립니다. (체험용, 정확한 심리검사가 아닙니다)")

# Session State 초기화
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "result_type" not in st.session_state:
    st.session_state.result_type = None
if "scores" not in st.session_state:
    st.session_state.scores = {}

# 문항 정의 (8문항, 각 차원별 2문항)
questions = [
    # E vs I
    {
        "key": "E1",
        "text": "새로운 반(팀)에 들어가면 나는...",
        "options": {"E": "여러 사람에게 먼저 말을 걸며 분위기를 탄다",
                    "I": "한두 명과 조용히 깊은 대화를 나눈다"},
        "weight": 1
    },
    {
        "key": "E2",
        "text": "수업(회의) 후 에너지를 회복하는 방식은...",
        "options": {"E": "사람들과 어울리며 자연스럽게 충전된다",
                    "I": "혼자만의 시간으로 머리를 정리해야 충전된다"},
        "weight": 2
    },

    # S vs N
    {
        "key": "S1",
        "text": "새로운 개념을 배울 때 더 편한 방식은...",
        "options": {"S": "예시·절차처럼 구체적인 것부터 이해",
                    "N": "큰 그림·아이디어 흐름을 먼저 파악"},
        "weight": 1
    },
    {
        "key": "S2",
        "text": "노트 정리 스타일에 가까운 것은...",
        "options": {"S": "사실·정의·핵심 포인트를 체크리스트로 정리",
                    "N": "연결선·마인드맵으로 개념 간 관계를 표현"},
        "weight": 2
    },

    # T vs F
    {
        "key": "T1",
        "text": "답안을 검토할 때 나는...",
        "options": {"T": "논리·근거가 타당한지, 반례가 없는지 본다",
                    "F": "맥락과 사람(학습자/교사)의 관점을 함께 고려한다"},
        "weight": 1
    },
    {
        "key": "T2",
        "text": "어려운 내용을 설명받을 때 더 와닿는 방식은...",
        "options": {"T": "원리와 규칙을 단계적으로 풀어주는 설명",
                    "F": "스토리·비유로 공감되게 풀어주는 설명"},
        "weight": 2
    },

    # J vs P
    {
        "key": "J1",
        "text": "과제 마감이 주어지면 나는...",
        "options": {"J": "일정을 앞당겨 계획대로 차근차근 끝낸다",
                    "P": "유연하게 진행하다 막판 집중으로 마감 맞춘다"},
        "weight": 1
    },
    {
        "key": "J2",
        "text": "하루 학습 계획에 대해 더 가까운 태도는...",
        "options": {"J": "시간 블록·To-Do로 세부 계획을 확정",
                    "P": "우선순위만 정하고 흐름에 맞춰 조정"},
        "weight": 2
    },
]

st.subheader("문항")
st.write("아래 8개 문항에 가장 **가까운 선택지**를 고르세요.")

# 응답 라디오 위젯 렌더링 (항상 기본 옵션 포함)
for q in questions:
    st.radio(
        label=f"• {q['text']}",
        options=["(선택하세요)"] + list(q["options"].values()),
        key=q["key"],
        index=0,
    )

# 점수 계산 함수
def calculate_mbti():
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for q in questions:
        choice = st.session_state.get(q["key"], None)
        if choice is None or choice == "(선택하세요)":
            return None, None
        for letter, text in q["options"].items():
            if text == choice:
                scores[letter] += q["weight"]
                break

    ei = "E" if scores["E"] > scores["I"] else "I"
    sn = "S" if scores["S"] > scores["N"] else "N"
    tf = "T" if scores["T"] > scores["F"] else "F"
    jp = "J" if scores["J"] > scores["P"] else "P"
    mbti = f"{ei}{sn}{tf}{jp}"
    return mbti, scores

# 학습 유형 설명
def learning_tips(ei, sn, tf, jp):
    tips = []
    if ei == "E":
        tips.append("• **E(외향)**: 스터디·토론형 학습이 동기 부여에 좋습니다. 학습 내용을 말로 설명해 보세요.")
    else:
        tips.append("• **I(내향)**: 조용한 공간에서의 **몰입형 개인 학습**이 효율적입니다. 글로 정리해 보는 방법이 잘 맞습니다.")
    if sn == "S":
        tips.append("• **S(감각)**: **예시→정의→연습** 순으로 구체에서 일반으로 올라가면 이해가 빠릅니다. 체크리스트를 활용하세요.")
    else:
        tips.append("• **N(직관)**: **개념 지도/마인드맵**으로 큰 흐름을 먼저 잡고 사례를 붙이면 기억에 오래 남습니다.")
    if tf == "T":
        tips.append("• **T(사고)**: 오답노트에 **왜 틀렸는지(원인)**, **어떻게 수정할지(규칙)**를 명확히 쓰는 것이 효과적입니다.")
    else:
        tips.append("• **F(감정)**: **스토리, 사례, 비유**로 감정에 연결하면 이해·기억이 좋아집니다. 동료에게 설명하며 공감 피드백을 받아보세요.")
    if jp == "J":
        tips.append("• **J(판단)**: **시간 블록/마감 역산 계획**이 잘 맞습니다. 작은 성취 체크(✓)로 동기 유지하세요.")
    else:
        tips.append("• **P(인식)**: **유연한 타임박싱**과 **짧은 스프린트**(예: 25분 집중+5분 휴식)가 생산성을 올립니다.")
    return tips

# 제출/다시하기 버튼
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("제출", type="primary"):
        mbti, scores = calculate_mbti()
        if mbti is None:
            st.warning("모든 문항에 응답해 주세요.")
        else:
            st.session_state.submitted = True
            st.session_state.result_type = mbti
            st.session_state.scores = scores

with col2:
    if st.button("다시 하기"):
        for q in questions:
            st.session_state[q["key"]] = "(선택하세요)"
        st.session_state.submitted = False
        st.session_state.result_type = None
        st.session_state.scores = {}

# 결과 출력
st.markdown("---")
st.subheader("결과")

if st.session_state.submitted and st.session_state.result_type:
    mbti = st.session_state.result_type
    ei, sn, tf, jp = list(mbti)
    st.success(f"당신의 MBTI 경향(간이): **{mbti}**")

    with st.expander("세부 점수 보기", expanded=False):
        s = st.session_state.scores
        st.write(
            f"- E: {s.get('E',0)} / I: {s.get('I',0)}\n"
            f"- S: {s.get('S',0)} / N: {s.get('N',0)}\n"
            f"- T: {s.get('T',0)} / F: {s.get('F',0)}\n"
            f"- J: {s.get('J',0)} / P: {s.get('P',0)}"
        )

    st.markdown("### 추천 학습 방법")
    for tip in learning_tips(ei, sn, tf, jp):
        st.write(tip)

    st.info("※ 본 결과는 학습 선호 경향을 간단히 파악하기 위한 도구이며, 공식 성격검사가 아닙니다.")
else:
    st.write("제출 버튼을 누르면 결과가 표시됩니다.")
