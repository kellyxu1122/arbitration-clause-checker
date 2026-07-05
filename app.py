"""
Arbitration Clause Checker — Bilingual Streamlit App
Run with: streamlit run app.py
"""

import re
import streamlit as st
import os
import joblib
import jieba

from detector import analyze_clause
from detector_cn import analyze_clause_cn

st.set_page_config(
    page_title="Arbitration Clause Checker",
    page_icon="⚖",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap');

/* ── reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #f8f7f4;
    color: #1c1c1e;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* narrow the content column — Apple-style centred column */
[data-testid="stAppViewContainer"] > .main > .block-container {
    max-width: 780px;
    margin: 0 auto;
    padding: 3.5rem 1.5rem 4rem;
}

/* ── typography ── */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif; }
p, label, .stMarkdown, .stRadio, .stSelectbox { font-family: 'Inter', system-ui, sans-serif; }

/* ── page title ── */
.acc-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2rem, 4vw, 2.75rem);
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.15;
    color: #1c1c1e;
    margin: 0 0 0.35rem;
}
.acc-subtitle {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin: 0 0 2rem;
}

/* ── description block ── */
.acc-desc {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.925rem;
    line-height: 1.75;
    color: #3a3a3c;
    border-left: 2px solid #d0cbc0;
    padding-left: 1.1rem;
    margin-bottom: 2.5rem;
}
.acc-desc strong { color: #1c1c1e; font-weight: 600; }
.acc-desc em { font-style: italic; }

/* ── thin rule ── */
.acc-rule {
    border: none;
    border-top: 1px solid #e0dbd2;
    margin: 2rem 0;
}

/* ── selectbox labels ── */
.acc-select-label {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.3rem;
}

/* ── text area ── */
textarea {
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.65 !important;
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    background: #ffffff !important;
    color: #1c1c1e !important;
}
textarea:focus { border-color: #888 !important; box-shadow: none !important; }

/* ── primary button ── */
.stButton > button[kind="primary"] {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    background: #1c1c1e;
    color: #f8f7f4;
    border: none;
    border-radius: 8px;
    padding: 0.55rem 1.6rem;
    letter-spacing: 0.01em;
    transition: opacity 0.15s;
}
.stButton > button[kind="primary"]:hover { opacity: 0.82; }

/* ── result summary pills ── */
.risk-pill {
    display: inline-block;
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    margin-bottom: 0.25rem;
}
.pill-red    { background: #fde8e6; color: #b91c1c; }
.pill-amber  { background: #fef3c7; color: #92400e; }
.pill-green  { background: #d1fae5; color: #065f46; }

.risk-count {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.85rem;
    color: #555;
    margin-top: 0.15rem;
}

/* ── probability bar ── */
.prob-track {
    background: #e5e0d8;
    border-radius: 3px;
    height: 5px;
    margin: 0.45rem 0 0.2rem;
    overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 3px; }

/* ── issue cards ── */
.issue-card {
    border-left: 2px solid #d0cbc0;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.6rem;
    background: #ffffff;
    border-radius: 0 8px 8px 0;
}
.issue-card.high   { border-left-color: #dc2626; }
.issue-card.medium { border-left-color: #d97706; }
.issue-card.low    { border-left-color: #a16207; }

.issue-badge {
    display: inline-block;
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    padding: 0.12rem 0.5rem;
    border-radius: 3px;
    margin-right: 0.5rem;
    vertical-align: middle;
}
.badge-high   { background: #fee2e2; color: #991b1b; }
.badge-medium { background: #fef3c7; color: #78350f; }
.badge-low    { background: #fefce8; color: #713f12; }

.issue-name {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    color: #1c1c1e;
    vertical-align: middle;
}
.issue-match {
    font-family: 'SF Mono', 'Fira Code', 'Courier New', monospace;
    font-size: 0.8rem;
    background: #f0ede6;
    color: #44403c;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
    margin: 0.4rem 0;
}
.issue-msg {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.855rem;
    line-height: 1.65;
    color: #3a3a3c;
    margin-top: 0.35rem;
}

/* ── caption / footnote ── */
.acc-note {
    font-family: 'Inter', system-ui, sans-serif;
    font-size: 0.75rem;
    color: #aaa;
    line-height: 1.6;
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ── sample data ──────────────────────────────────────────────────────────────

EN_GOOD = {
    "ICC — standard international clause": (
        "Any dispute arising out of or in connection with this Agreement, including any question regarding its "
        "existence, validity or termination, shall be referred to and finally resolved by arbitration administered "
        "by the International Chamber of Commerce in accordance with the ICC Rules of Arbitration. The seat of "
        "arbitration shall be Paris, France. The tribunal shall consist of three arbitrators. The language of the "
        "arbitration shall be English. This Agreement shall be governed by and construed in accordance with the "
        "laws of England and Wales."
    ),
    "LCIA — standard international clause": (
        "Any dispute, controversy or claim arising out of or relating to this contract shall be finally resolved by "
        "arbitration in accordance with the LCIA Arbitration Rules. The number of arbitrators shall be one. The "
        "seat of arbitration shall be London. The language of the arbitration shall be English. The governing law "
        "of this contract shall be the laws of England and Wales."
    ),
    "SIAC — standard international clause": (
        "Any dispute arising from or in connection with this Agreement shall be referred to and finally resolved by "
        "arbitration administered by the Singapore International Arbitration Centre in accordance with the "
        "Arbitration Rules of the Singapore International Arbitration Centre for the time being in force. The seat "
        "of arbitration shall be Singapore. The tribunal shall consist of one arbitrator. The language shall be "
        "English. This agreement shall be governed by the laws of Singapore."
    ),
    "HKIAC — standard international clause": (
        "Any dispute, controversy or claim arising out of or relating to this contract shall be settled by "
        "arbitration administered by the Hong Kong International Arbitration Centre under the HKIAC Administered "
        "Arbitration Rules. The seat of arbitration shall be Hong Kong. The number of arbitrators shall be three. "
        "The arbitration proceedings shall be conducted in English. This Agreement is governed by the laws of "
        "Hong Kong."
    ),
    "AAA/ICDR — international clause": (
        "Any dispute arising out of or in connection with this contract shall be finally resolved by arbitration "
        "administered by the International Centre for Dispute Resolution (ICDR) in accordance with its "
        "International Arbitration Rules. The seat of arbitration shall be New York, New York. The tribunal shall "
        "consist of three arbitrators. The language of arbitration shall be English. This Agreement shall be "
        "governed by the laws of the State of New York."
    ),
    "JAMS — standard international clause": (
        "Any dispute arising out of or in connection with this contract shall be finally settled by arbitration "
        "administered by JAMS in accordance with the JAMS International Arbitration Rules. The seat of arbitration "
        "shall be New York, New York. The tribunal shall consist of three arbitrators. The language of the "
        "arbitration shall be English. This Agreement is governed by the laws of England and Wales."
    ),
    "UNCITRAL Rules — PCA-administered ad hoc clause": (
        "Any dispute, controversy or claim arising out of or relating to this contract, or the breach, termination "
        "or invalidity thereof, shall be settled by arbitration in accordance with the UNCITRAL Arbitration Rules, "
        "administered by the Permanent Court of Arbitration. The seat of arbitration shall be The Hague, "
        "Netherlands. The number of arbitrators shall be three. The language of the arbitration shall be "
        "English. This Agreement shall be governed by the laws of the Netherlands."
    ),
    "AFA — standard French arbitration clause": (
        "Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration "
        "administered by the Association Française d'Arbitrage (AFA) in accordance with its Arbitration Rules. "
        "The seat of arbitration shall be Paris, France. The tribunal shall consist of three arbitrators. "
        "The language of the arbitration shall be English. This Agreement shall be governed by French law."
    ),
}

EN_BAD = {
    # Each defective example is drafted to be otherwise complete, so the
    # checker surfaces exactly the one defect the label describes.
    "Consent & Jurisdiction Conflict — ambiguous 'may' instead of 'shall'": (
        "In the event of any dispute arising out of or in connection with this Agreement, either party may submit "
        "the matter to arbitration administered by the International Chamber of Commerce in accordance with the "
        "ICC Rules of Arbitration. The seat of arbitration shall be Paris, France. The tribunal shall consist of "
        "three arbitrators. The language of the arbitration shall be English. This Agreement is governed by the "
        "laws of England and Wales."
    ),
    "Consent & Jurisdiction Conflict — arbitration and litigation both permitted": (
        "Any dispute arising out of or in connection with this Agreement shall be referred to arbitration "
        "administered by the ICC in accordance with the ICC Rules of Arbitration. Notwithstanding the foregoing, "
        "either party may also bring an action before a court of competent jurisdiction. The seat of arbitration "
        "shall be Paris. The tribunal shall consist of three arbitrators. The language of the arbitration shall "
        "be English. This Agreement is governed by French law."
    ),
    "Institutional Designation — unrecognized institution name": (
        "Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration "
        "administered by the International Arbitration Commission of Singapore in accordance with its rules. The "
        "seat of arbitration shall be Singapore. The tribunal shall consist of one arbitrator. The language of "
        "the arbitration shall be English. This Agreement is governed by Singapore law."
    ),
    "Institutional Designation — named institution and cited rules conflict": (
        "Any dispute arising out of or in connection with this Agreement shall be finally settled by arbitration "
        "administered by the Singapore International Arbitration Centre (SIAC) in accordance with the UNCITRAL "
        "Arbitration Rules. The seat of arbitration shall be Singapore. The tribunal shall consist of one "
        "arbitrator. The language of the arbitration shall be English. This Agreement is governed by Singapore law."
    ),
    "Defective Rule Selection — institutional rules not specified": (
        "Any dispute arising out of or in connection with this Agreement shall be submitted to binding "
        "arbitration before JAMS. The seat of arbitration shall be New York, New York. The tribunal shall "
        "consist of one arbitrator. The language of the arbitration shall be English. This Agreement is governed "
        "by New York law."
    ),
    "Defective Rule Selection — domestic rules incorrectly applied": (
        "Any dispute arising out of or in connection with this international Agreement shall be resolved by "
        "arbitration administered by the American Arbitration Association under its Commercial Arbitration "
        "Rules. The seat of arbitration shall be New York. The tribunal shall consist of three arbitrators. The "
        "language of the arbitration shall be English. This Agreement is governed by the laws of England and Wales."
    ),
    "Missing Procedural Elements — no seat of arbitration specified": (
        "Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration "
        "administered by the International Chamber of Commerce in accordance with the ICC Rules of Arbitration. "
        "The tribunal shall consist of three arbitrators. The language of the arbitration shall be English. This "
        "Agreement is governed by the laws of England and Wales."
    ),
    "Missing Procedural Elements — language of arbitration not specified": (
        "Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration "
        "administered by the ICC in accordance with the ICC Rules of Arbitration. The seat of arbitration shall "
        "be Paris. The tribunal shall consist of three arbitrators. This Agreement is governed by French law."
    ),
    "Missing Procedural Elements — unworkable tribunal composition (even number)": (
        "Any dispute arising out of or in connection with this Agreement shall be finally resolved by arbitration "
        "administered by the LCIA under the LCIA Rules. The seat of arbitration shall be London. The parties "
        "shall each appoint one arbitrator and the two arbitrators shall jointly render the award. The language "
        "of the arbitration shall be English. This Agreement is governed by English law."
    ),
    "Structural Defects — unilateral option clause": (
        "Any dispute arising out of or in connection with this Agreement shall be resolved by arbitration "
        "administered by the LCIA under the LCIA Rules, provided that only the Lender may elect to submit a "
        "dispute to arbitration; the Borrower\'s exclusive recourse shall be to the courts of England and Wales. "
        "The seat of arbitration shall be London. The tribunal shall consist of three arbitrators. The language "
        "of the arbitration shall be English. This Agreement is governed by English law."
    ),
    "Structural Defects — multi-tier clause without defined trigger": (
        "Any dispute arising out of or in connection with this Agreement shall first be referred to senior "
        "management of both parties for amicable resolution. If the dispute is not resolved, it shall be "
        "submitted to arbitration administered by the ICC under the ICC Rules. The seat of arbitration shall be "
        "Paris. The tribunal shall consist of three arbitrators. The language of the arbitration shall be "
        "English. This Agreement is governed by French law."
    ),
}

CN_GOOD = {
    "贸仲 CIETAC — 标准条款": (
        "因履行本合同所发生的一切争议，应提交中国国际经济贸易仲裁委员会，"
        "按照该会现行有效的仲裁规则进行仲裁。仲裁地为北京。仲裁裁决是终局的，"
        "对双方均有约束力。本合同适用中华人民共和国法律。"
    ),
    "北仲 BAC — 标准条款": (
        "凡因本合同引起的或与本合同有关的任何争议，均应提交北京仲裁委员会，"
        "按照申请仲裁时该会现行有效的仲裁规则进行仲裁。仲裁裁决是终局的，"
        "对双方均有约束力。仲裁地为北京。本合同适用中国法律。"
    ),
    "上国仲 SHIAC — 标准条款": (
        "凡因本合同引起的或与本合同有关的任何争议，均应提交上海国际经济贸易"
        "仲裁委员会（上海国际仲裁中心），按照申请仲裁时该会现行有效的仲裁规则"
        "进行仲裁。仲裁裁决是终局的，对双方均有约束力。仲裁地为上海。"
    ),
    "深国仲 SCIA — 标准条款": (
        "因本合同产生的或与本合同有关的任何争议，由深圳国际仲裁院按照其仲裁"
        "规则仲裁解决。仲裁地为深圳。仲裁庭由三名仲裁员组成。本合同适用中华"
        "人民共和国法律。"
    ),
}

CN_BAD = {
    # 每条无效示例的其余要素均已补齐，工具将精确展示标签所述的单一问题
    "或裁或诉 — 仲裁与诉讼并列": (
        "凡因本合同引起的或与本合同有关的任何争议，可以向北京仲裁委员会申请仲裁，"
        "也可以向人民法院起诉。仲裁地为北京。本合同适用中华人民共和国法律。"
    ),
    "仅约定仲裁规则 — 未明确仲裁机构": (
        "凡因本合同引起的或与本合同有关的任何争议，依照国际商会仲裁规则进行仲裁。"
        "仲裁地为北京。本合同适用中华人民共和国法律。"
    ),
    "仲裁机构约定不明 — 违约方所在地仲裁委": (
        "凡因本合同引起的或与本合同有关的任何争议，由双方协商解决；协商不成的，"
        "由违约方所在地仲裁委员会仲裁。仲裁地为合同签订地。本合同适用中华人民共和国法律。"
    ),
    "约定两个以上仲裁机构": (
        "凡因本合同引起的或与本合同有关的任何争议，提交中国国际经济贸易仲裁委员会"
        "或北京仲裁委员会仲裁。仲裁地为北京。本合同适用中华人民共和国法律。"
    ),
    "仲裁机构名称无法识别": (
        "凡因本合同引起的或与本合同有关的任何争议，提交环球商事仲裁联合会仲裁解决。"
        "仲裁地为上海。本合同适用中华人民共和国法律。"
    ),
}
MODEL_PATH = os.path.join(os.path.dirname(__file__), "clause_classifier_bilingual.joblib")

def contains_chinese(text):
    return bool(re.search(r"[\u4e00-\u9fa5]", text))

def tokenize_bilingual(text):
    if contains_chinese(text):
        tokens = jieba.lcut(text)
        return " ".join(t.strip() for t in tokens if t.strip() and not re.match(r"^[\s\W]+$", t)).lower()
    return text.lower()

@st.cache_resource
def load_classifier():
    if os.path.exists(MODEL_PATH):
        b = joblib.load(MODEL_PATH)
        return b["vectorizer"], b["classifier"]
    return None, None

vectorizer, classifier = load_classifier()

# ── header ───────────────────────────────────────────────────────────────────
st.markdown('<p class="acc-subtitle">Legal NLP · International Arbitration</p>', unsafe_allow_html=True)
st.markdown('<h1 class="acc-title">Arbitration Clause Checker</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="acc-desc">
Most jurisdictional challenges in international arbitration don&rsquo;t stem from complex legal
disputes; they trace back to flawed drafting. An inverted typo in an institution&rsquo;s name,
ambiguous &ldquo;may&rdquo; vs. &ldquo;shall&rdquo; language, or a single &ldquo;or&rdquo; can tie up a cross-border
transaction in years of jurisdictional fights.<br><br>
This tool systematizes the pattern recognition required to catch these flaws before execution.
It deploys two separate, hardcoded rule engines: one mapped to major international institutional
rules (ICC, AAA, LCIA, SIAC) and the other to PRC Arbitration Law and the 2006 Supreme Court
Judicial Interpretation. A bilingual ML classifier identifies initial language patterns; the
rule engines then process the jurisdiction-specific legal outcomes.<br><br>
Keeping these logic streams isolated is a deliberate architectural choice. A &ldquo;hybrid&rdquo; clause
permitting both arbitration and litigation is treated as an ambiguous, often salvageable defect
under many common-law frameworks. Under Article 7 of the PRC Judicial Interpretation, it is
strictly invalid. Conflating the two produces false confidence, not coverage.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="acc-rule">', unsafe_allow_html=True)

# ── language ─────────────────────────────────────────────────────────────────
lang = st.radio("Language / 条款语言", ["English", "中文"], horizontal=True, label_visibility="collapsed")

if lang == "English":
    good_dict, bad_dict = EN_GOOD, EN_BAD
    none_good, none_bad = "— or paste your own clause below —", "— or paste your own clause below —"
    good_label, bad_label = "✦ Well-drafted examples", "✦ Defective examples"
    input_placeholder = "Paste or type an arbitration clause here..."
    btn_label = "Check clause"
else:
    good_dict, bad_dict = CN_GOOD, CN_BAD
    none_good, none_bad = "— 或在下方自行输入条款 —", "— 或在下方自行输入条款 —"
    good_label, bad_label = "✦ 有效仲裁条款示例", "✦ 无效仲裁条款示例"
    input_placeholder = "在此粘贴或输入仲裁条款..."
    btn_label = "分析条款"

# session state init
for k, v in [("good_sel", none_good), ("bad_sel", none_bad)]:
    if k not in st.session_state:
        st.session_state[k] = v

def on_good():
    if st.session_state["good_sel"] != none_good:
        st.session_state["bad_sel"] = none_bad
        # 直接写入文本框的session state key，才能让文本框实际显示新内容
        st.session_state["clause_widget"] = good_dict[st.session_state["good_sel"]]

def on_bad():
    if st.session_state["bad_sel"] != none_bad:
        st.session_state["good_sel"] = none_good
        st.session_state["clause_widget"] = bad_dict[st.session_state["bad_sel"]]

col_g, col_b = st.columns(2)
with col_g:
    st.markdown(f'<div class="acc-select-label">{good_label}</div>', unsafe_allow_html=True)
    st.selectbox("g", [none_good] + list(good_dict.keys()),
                 key="good_sel", on_change=on_good, label_visibility="collapsed")
with col_b:
    st.markdown(f'<div class="acc-select-label">{bad_label}</div>', unsafe_allow_html=True)
    st.selectbox("b", [none_bad] + list(bad_dict.keys()),
                 key="bad_sel", on_change=on_bad, label_visibility="collapsed")

def on_clause_edit():
    # 用户手动编辑时，重置两个下拉为默认
    st.session_state["good_sel"] = none_good
    st.session_state["bad_sel"] = none_bad

clause_text = st.text_area(
    "clause",
    height=148,
    placeholder=input_placeholder,
    key="clause_widget",
    on_change=on_clause_edit,
    label_visibility="collapsed",
)

st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)
analyze_btn = st.button(btn_label, type="primary")

# ── results ───────────────────────────────────────────────────────────────────
if analyze_btn:
    if not clause_text.strip():
        st.warning("Please enter a clause. / 请输入仲裁条款。")
        st.stop()

    is_cn = contains_chinese(clause_text)
    result = analyze_clause_cn(clause_text) if is_cn else analyze_clause(clause_text)
    n = len(result.flags)

    st.markdown('<hr class="acc-rule">', unsafe_allow_html=True)

    col_r, col_m = st.columns(2)

    # risk level → pill class
    pill_cls = {
        "High risk": "pill-red", "Moderate risk": "pill-amber", "Low risk": "pill-green",
        "高风险": "pill-red",   "中等风险": "pill-amber",       "低风险": "pill-green",
    }.get(result.risk_level, "pill-green")

    with col_r:
        st.caption("Rule engine · 规则引擎")
        label_en = {0: "No issues found"}.get(n, f"{n} issue{'s' if n!=1 else ''} detected")
        label_cn = {0: "未发现问题"}.get(n, f"检测到 {n} 项问题")
        count_label = label_cn if is_cn else label_en
        st.markdown(f"""
        <div class="risk-pill {pill_cls}">{result.risk_level}</div>
        <div class="risk-count">{count_label}</div>
        """, unsafe_allow_html=True)

    with col_m:
        st.caption("ML classifier · 机器学习分类器")
        if classifier:
            prob = classifier.predict_proba(
                vectorizer.transform([tokenize_bilingual(clause_text)])
            )[0][1]
            bar_col = "#dc2626" if prob > 0.6 else "#d97706" if prob > 0.4 else "#16a34a"
            plabel = f"{prob:.0%} defect probability" if not is_cn else f"{prob:.0%} 无效风险概率"
            st.markdown(f"""
            <div style="font-size:0.9rem;font-weight:600;color:#1c1c1e">{plabel}</div>
            <div class="prob-track">
              <div class="prob-fill" style="width:{prob*100:.1f}%;background:{bar_col}"></div>
            </div>
            """, unsafe_allow_html=True)
            note = ("Trained on 183 labeled clauses · independent of rule engine"
                    if not is_cn else "基于183条标注数据训练 · 与规则引擎独立")
            st.markdown(f'<div class="acc-note">{note}</div>', unsafe_allow_html=True)
        else:
            st.caption("Model not found — run train_classifier_bilingual.py")

    detected = "Chinese · 中文" if is_cn else "English · 英文"
    st.markdown(f'<div class="acc-note" style="margin-top:0.8rem">Detected language: {detected}</div>',
                unsafe_allow_html=True)

    # ── issue cards ───────────────────────────────────────────────────────────
    if n == 0:
        st.markdown('<hr class="acc-rule">', unsafe_allow_html=True)
        ok_msg = ("No common drafting defects detected. This tool checks for known structural "
                  "patterns only and does not constitute legal advice."
                  if not is_cn else
                  "未检测到常见条款瑕疵。本工具仅检测已知结构性问题，不构成法律意见。")
        st.success(ok_msg)
    else:
        st.markdown('<hr class="acc-rule">', unsafe_allow_html=True)
        hdr = (f"{n} issue{'s' if n!=1 else ''} found, ordered by severity"
               if not is_cn else f"检测到 {n} 项问题，按严重程度排列")
        st.markdown(f"<p style='font-size:0.8rem;font-weight:600;letter-spacing:0.08em;"
                    f"text-transform:uppercase;color:#888;margin-bottom:0.75rem'>{hdr}</p>",
                    unsafe_allow_html=True)

        badges_en = {"high": ("Critical", "badge-high"),
                     "medium": ("Warning", "badge-medium"),
                     "low": ("Advisory", "badge-low")}
        badges_cn = {"high": ("严重缺陷", "badge-high"),
                     "medium": ("注意事项", "badge-medium"),
                     "low": ("建议改进", "badge-low")}

        for f in sorted(result.flags, key=lambda x: {"high":0,"medium":1,"low":2}[x.severity]):
            badge_text, badge_cls = (badges_cn if is_cn else badges_en)[f.severity]
            match_html = (f'<div class="issue-match">"{f.matched_text}"</div>'
                          if f.matched_text else "")
            st.markdown(f"""
            <div class="issue-card {f.severity}">
              <span class="issue-badge {badge_cls}">{badge_text}</span>
              <span class="issue-name">{f.category}</span>
              {match_html}
              <div class="issue-msg">{f.message}</div>
            </div>
            """, unsafe_allow_html=True)

    # disclaimer
    disc = ("Academic / portfolio project · not a substitute for legal advice."
            if not is_cn else
            "学术与作品集项目，不构成法律意见，不能替代专业律师审查。")
    st.markdown(f'<div class="acc-note" style="margin-top:1.5rem">{disc}</div>',
                unsafe_allow_html=True)
