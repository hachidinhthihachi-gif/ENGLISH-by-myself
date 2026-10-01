"""
Học từ vựng Business English (New Business English 4-5-6)
Chạy:  pip install streamlit
       streamlit run business_english_app.py

Muốn thêm từ của sách: tạo file vocab.json cùng thư mục, dạng:
{
  "Book 4 | 01. Meetings": [
    {"en": "agenda", "pos": "n.", "vi": "chương trình họp", "ex": "Please check the agenda."}
  ]
}
(Chủ đề trùng tên sẽ ghi đè bản mẫu bên dưới.)
"""
import json
import pathlib
import random

import streamlit as st
import streamlit.components.v1 as components

PROGRESS_FILE = pathlib.Path("progress.json")
VOCAB_FILE = pathlib.Path("vocab.json")


def w(en, pos, vi, ex):
    return {"en": en, "pos": pos, "vi": vi, "ex": ex}


# ---- DỮ LIỆU MẪU (hãy thay bằng từ trong sách của bạn qua vocab.json) ----
DATA = {
    "Book 4 | 01. Meetings": [
        w("agenda", "n.", "chương trình họp", "Let's go through the agenda."),
        w("minutes", "n.", "biên bản họp", "Who will take the minutes?"),
        w("attend", "v.", "tham dự", "Will you attend the meeting?"),
        w("postpone", "v.", "hoãn lại", "We have to postpone the meeting."),
        w("deadline", "n.", "hạn chót", "The deadline is Friday."),
        w("propose", "v.", "đề xuất", "I'd like to propose a new plan."),
        w("approve", "v.", "phê duyệt", "The manager approved the budget."),
        w("follow up", "phr. v.", "theo dõi, tiếp tục xử lý", "I'll follow up by email."),
    ],
    "Book 4 | 02. Telephone & Email": [
        w("inquiry", "n.", "yêu cầu hỏi thông tin", "I'm calling about an inquiry."),
        w("put through", "phr. v.", "nối máy", "I'll put you through to sales."),
        w("leave a message", "phr.", "để lại lời nhắn", "Can I leave a message?"),
        w("attachment", "n.", "tệp đính kèm", "Please see the attachment."),
        w("forward", "v.", "chuyển tiếp", "I'll forward you the email."),
        w("reply", "v.", "trả lời", "Please reply by noon."),
        w("regarding", "prep.", "liên quan đến", "I'm writing regarding your order."),
        w("urgent", "adj.", "khẩn cấp", "This is an urgent matter."),
    ],
    "Book 5 | 03. Marketing & Sales": [
        w("target market", "n.", "thị trường mục tiêu", "Define your target market."),
        w("launch", "v.", "ra mắt", "We will launch the product in May."),
        w("brand awareness", "n.", "độ nhận diện thương hiệu", "Ads boost brand awareness."),
        w("revenue", "n.", "doanh thu", "Revenue rose by 10%."),
        w("competitor", "n.", "đối thủ cạnh tranh", "Our competitor cut prices."),
        w("promotion", "n.", "khuyến mãi", "There is a summer promotion."),
        w("customer base", "n.", "tệp khách hàng", "We expanded our customer base."),
        w("market share", "n.", "thị phần", "They hold a large market share."),
    ],
    "Book 5 | 04. Negotiation": [
        w("offer", "n.", "lời đề nghị", "That's a generous offer."),
        w("counteroffer", "n.", "đề nghị đối ứng", "They made a counteroffer."),
        w("compromise", "n.", "sự thỏa hiệp", "We reached a compromise."),
        w("terms", "n.", "điều khoản", "Let's discuss the terms."),
        w("discount", "n.", "chiết khấu", "Can you give us a discount?"),
        w("bargain", "v.", "mặc cả", "They tried to bargain."),
        w("deal", "n.", "thương vụ, thỏa thuận", "It's a done deal."),
        w("concession", "n.", "sự nhượng bộ", "We made a concession."),
    ],
    "Book 6 | 05. Finance & Reports": [
        w("budget", "n.", "ngân sách", "We're over budget."),
        w("profit", "n.", "lợi nhuận", "Profit fell last quarter."),
        w("expense", "n.", "chi phí", "Cut unnecessary expenses."),
        w("forecast", "n.", "dự báo", "The sales forecast looks good."),
        w("invoice", "n.", "hóa đơn", "Please send the invoice."),
        w("quarter", "n.", "quý", "Results for the first quarter."),
        w("investment", "n.", "khoản đầu tư", "It's a risky investment."),
        w("cash flow", "n.", "dòng tiền", "Cash flow is a problem."),
    ],
    "Book 6 | 06. Management & HR": [
        w("recruit", "v.", "tuyển dụng", "We plan to recruit ten staff."),
        w("promote", "v.", "thăng chức", "She was promoted to manager."),
        w("performance review", "n.", "đánh giá hiệu suất", "My review is next week."),
        w("delegate", "v.", "ủy quyền, giao việc", "Learn to delegate tasks."),
        w("resign", "v.", "từ chức", "He decided to resign."),
        w("workload", "n.", "khối lượng công việc", "My workload is heavy."),
        w("teamwork", "n.", "làm việc nhóm", "Teamwork is essential."),
        w("supervisor", "n.", "người giám sát", "Ask your supervisor."),
    ],
}

if VOCAB_FILE.exists():
    try:
        DATA.update(json.loads(VOCAB_FILE.read_text(encoding="utf-8")))
    except Exception as e:
        st.warning(f"Không đọc được vocab.json: {e}")

ALL_WORDS = [x for ws in DATA.values() for x in ws]


# ---------------- tiện ích ----------------
def load_progress():
    if PROGRESS_FILE.exists():
        try:
            return set(json.loads(PROGRESS_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return set()


def save_progress():
    PROGRESS_FILE.write_text(json.dumps(sorted(st.session_state.learned)), encoding="utf-8")


def mark(word, ok):
    if ok:
        st.session_state.learned.add(word["en"])
    else:
        st.session_state.learned.discard(word["en"])
    save_progress()


def speak_button(text, key):
    """Nút phát âm dùng giọng đọc có sẵn của trình duyệt (không cần internet/API)."""
    safe = json.dumps(text)
    components.html(
        f"""<button id="b{key}" style="background:#b91c1c;color:#fff;border:0;border-radius:50%;
        width:56px;height:56px;font-size:24px;cursor:pointer">🔊</button>
        <script>
        const speak=()=>{{const u=new SpeechSynthesisUtterance({safe});u.lang='en-US';u.rate=0.9;
        speechSynthesis.cancel();speechSynthesis.speak(u);}};
        document.getElementById('b{key}').onclick=speak;
        </script>""",
        height=70,
    )


def make_options(word, field):
    correct = word[field]
    others = list({x[field] for x in ALL_WORDS if x[field] != correct})
    rng = random.Random(word["en"] + field)
    opts = rng.sample(others, min(3, len(others))) + [correct]
    rng.shuffle(opts)
    return opts


def nav(total, tag):
    c1, c2 = st.columns(2)
    if c1.button("← Câu trước", disabled=st.session_state.i == 0, use_container_width=True, key=f"prev_{tag}"):
        st.session_state.i -= 1
        st.session_state.flip = False
        st.rerun()
    if c2.button("Câu tiếp →", disabled=st.session_state.i >= total - 1,
                 type="primary", use_container_width=True, key=f"next_{tag}"):
        st.session_state.i += 1
        st.session_state.flip = False
        st.rerun()


def choice_question(word, field, prompt, answer_field, mode_key):
    """Dùng chung cho Trắc nghiệm và Nghe."""
    st.caption(prompt)
    opts = make_options(word, answer_field)
    done = st.session_state.answers.get((mode_key, word["en"]))
    cols = st.columns(2)
    for n, opt in enumerate(opts):
        label = opt
        if done:
            if opt == word[answer_field]:
                label = "✅ " + opt
            elif opt == done:
                label = "❌ " + opt
        if cols[n % 2].button(label, key=f"{mode_key}{word['en']}{n}",
                              disabled=bool(done), use_container_width=True):
            st.session_state.answers[(mode_key, word["en"])] = opt
            mark(word, opt == word[answer_field])
            st.rerun()
    if done:
        st.info(f"**{word['en']}** ({word['pos']}) = {word['vi']}\n\n_{word['ex']}_")


# ---------------- giao diện ----------------
st.set_page_config(page_title="Business English", page_icon="💼", layout="wide")
st.markdown("<style>.big{font-size:3rem;font-weight:700;text-align:center;margin:.5rem 0}"
            ".sub{text-align:center;color:#64748b}</style>", unsafe_allow_html=True)

if "learned" not in st.session_state:
    st.session_state.learned = load_progress()
    st.session_state.answers = {}
    st.session_state.i = 0
    st.session_state.flip = False
    st.session_state.sig = None

with st.sidebar:
    st.title("💼 Business English")
    topic = st.radio("Chọn bộ từ", list(DATA.keys()),
                     format_func=lambda t: f"{t}  ({sum(x['en'] in st.session_state.learned for x in DATA[t])}/{len(DATA[t])})")
    only_new = st.checkbox("Chỉ học từ chưa thuộc", value=False)
    shuffle = st.checkbox("Xáo trộn thứ tự", value=False)
    if st.button("Xóa tiến độ"):
        st.session_state.learned = set()
        st.session_state.answers = {}
        save_progress()
        st.rerun()

words = [x for x in DATA[topic] if not (only_new and x["en"] in st.session_state.learned)]
if shuffle:
    words = random.Random(topic).sample(words, len(words))

sig = (topic, only_new, shuffle)
if st.session_state.sig != sig:
    st.session_state.sig, st.session_state.i, st.session_state.flip = sig, 0, False

total_topic = len(DATA[topic])
done_n = sum(x["en"] in st.session_state.learned for x in DATA[topic])
st.header(topic)
st.progress(done_n / total_topic, text=f"Đã học {done_n}/{total_topic} từ ({done_n * 100 // total_topic}%)")

if not words:
    st.success("🎉 Bạn đã thuộc hết bộ từ này!")
    st.stop()

st.session_state.i = min(st.session_state.i, len(words) - 1)
word = words[st.session_state.i]
st.caption(f"Từ {st.session_state.i + 1}/{len(words)}")

tabs = st.tabs(["🗂️ Thẻ ghi nhớ", "☑️ Trắc nghiệm", "🎧 Nghe & chọn nghĩa", "⌨️ Gõ từ"])

with tabs[0]:
    with st.container(border=True):
        st.markdown(f"<div class='big'>{word['en']}</div><div class='sub'>{word['pos']}</div>",
                    unsafe_allow_html=True)
        speak_button(word["en"], f"fc{st.session_state.i}")
        if st.button("👁️ Xem nghĩa / ẩn nghĩa", use_container_width=True):
            st.session_state.flip = not st.session_state.flip
            st.rerun()
        if st.session_state.flip:
            st.success(f"**{word['vi']}**\n\n_{word['ex']}_")
            a, b = st.columns(2)
            if a.button("✅ Đã thuộc", use_container_width=True):
                mark(word, True); st.rerun()
            if b.button("🔁 Chưa thuộc", use_container_width=True):
                mark(word, False); st.rerun()
    nav(len(words), "fc")

with tabs[1]:
    st.markdown(f"<div class='big'>{word['vi']}</div>", unsafe_allow_html=True)
    choice_question(word, "vi", "CHỌN TỪ TIẾNG ANH CÓ NGHĨA:", "en", "mc")
    nav(len(words), "mc")

with tabs[2]:
    st.caption("NGHE VÀ CHỌN NGHĨA")
    speak_button(word["en"], f"ls{st.session_state.i}")
    choice_question(word, "en", "Từ vừa nghe có nghĩa là:", "vi", "ls")
    nav(len(words), "ls")

with tabs[3]:
    st.markdown(f"<div class='big'>{word['vi']}</div>", unsafe_allow_html=True)
    st.caption(f"GÕ TỪ TIẾNG ANH CÓ NGHĨA · {len(word['en'])} ký tự")
    speak_button(word["en"], f"ty{st.session_state.i}")
    with st.form(f"f{word['en']}", clear_on_submit=False):
        ans = st.text_input("Gõ từ tiếng Anh...")
        sent = st.form_submit_button("✔ Kiểm tra", type="primary")
    if sent:
        ok = ans.strip().lower() == word["en"].lower()
        mark(word, ok)
        (st.success if ok else st.error)(
            f"{'Chính xác!' if ok else 'Chưa đúng.'} Đáp án: **{word['en']}** — _{word['ex']}_")
    nav(len(words), "ty")
