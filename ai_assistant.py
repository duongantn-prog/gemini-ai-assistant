import streamlit as st
from google import genai

# Cấu hình giao diện chatbot nhỏ gọn để nhúng vừa vào cột web
st.set_page_config(page_title="AI Sửa Lỗi", page_icon="🤖", layout="centered")
st.caption("🤖 Trợ Lý AI Sửa Lỗi Python")

# Streamlit sẽ tự động đọc API Key bảo mật từ phần Secrets mà bạn cấu hình ở phần sau
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = "CHƯA_CẤU_HÌNH"

if GEMINI_API_KEY == "CHƯA_CẤU_HÌNH":
    st.error("Vui lòng cấu hình API Key trong phần Settings > Secrets của Streamlit Cloud!")
else:
    # Khởi tạo client Gemini thế hệ mới
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Khởi tạo lịch sử chat nếu chưa có
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Chào bạn! Nếu code bên Binder bị lỗi, hãy copy đoạn code hoặc dòng thông báo lỗi dán vào đây, mình sẽ sửa và giải thích cho bạn bằng Tiếng Việt nhé!"}
        ]

    # Hiển thị các tin nhắn cũ
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Nhận câu hỏi từ người dùng
    if user_input := st.chat_input("Dán code lỗi vào đây..."):
        # Hiển thị câu hỏi của người dùng
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Gọi AI xử lý
        with st.chat_message("assistant"):
            with st.spinner("AI đang phân tích lỗi..."):
                try:
                    # Thiết lập vai trò hệ thống để Gemini tập trung sửa lỗi lập trình
                    prompt_vi = (
                        "Bạn là một trợ lý giảng dạy lập trình Python nhiệt tình. "
                        "Nhiệm vụ của bạn là kiểm tra đoạn code hoặc lỗi sau đây từ học viên. "
                        "Hãy chỉ ra lỗi sai ở đâu, giải thích ngắn gọn bằng Tiếng Việt và đưa ra đoạn code đã sửa đúng.\n\n"
                        f"Câu hỏi của học viên: {user_input}"
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt_vi
                    )
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Lỗi kết nối AI: {e}")
