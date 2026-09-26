import streamlit as st

from src.pipeline import prepare_video


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="YouTube Video Analyzer",
    page_icon="🎥",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🎥 YouTube Video Analyzer")

st.caption(
    "Analyze English YouTube videos and ask questions "
    "using timestamp-aware RAG."
)


# ==================================================
# SIDEBAR — MODEL SETTINGS
# ==================================================

with st.sidebar:

    st.header("🤖 AI Model")

    provider = st.radio(
        "Choose AI provider",
        ["Google Gemini", "OpenAI"]
    )

    if provider == "Google Gemini":

        model = st.selectbox(
            "Gemini Model",
            [
                "gemini-3.5-flash-lite"
            ]
        )

        api_key = st.text_input(
            "Google API Key",
            type="password",
            placeholder="Enter your Gemini API key"
        )

    else:

        model = st.selectbox(
            "OpenAI Model",
            [
                "gpt-5.6-mini"
            ]
        )

        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Enter your OpenAI API key"
        )


# ==================================================
# YOUTUBE VIDEO
# ==================================================

st.header("📺 Video")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# ==================================================
# ANALYZE BUTTON
# ==================================================

if st.button(
    "🔍 Analyze Video",
    type="primary"
):

    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

    elif not api_key:

        st.warning(
            f"Please enter your {provider} API key."
        )

    else:

        with st.spinner(
            "Analyzing video... This may take a moment."
        ):

            try:

                result = prepare_video(
                    url=youtube_url,
                    provider=provider,
                    model=model,
                    api_key=api_key,
                    k=3
                )

                # Store everything needed for Q&A later
                st.session_state["video_result"] = result
                st.session_state["provider"] = provider
                st.session_state["model"] = model
                st.session_state["api_key"] = api_key

                st.success(
                    "Video analyzed successfully!"
                )

            except ValueError as e:

                st.error(str(e))

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# ==================================================
# VIDEO INFORMATION
# ==================================================

if "video_result" in st.session_state:

    result = st.session_state["video_result"]
    metadata = result["metadata"]

    st.divider()

    st.header("📋 Video Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Duration",
            metadata["duration"]
        )

    with col2:
        st.metric(
            "Published",
            metadata["published_at"]
        )

    with col3:
        st.metric(
            "Channel",
            metadata["channel"]
        )


    st.subheader("**Video Title**")
    st.subheader(metadata["title"])

    st.success(
        "English transcript available"
    )

    st.info(
        "Video is ready for questions."
    )
    

# ==================================================
# CHAT INTERFACE
# ==================================================

if "video_result" in st.session_state:

    st.divider()

    st.header("💬 Ask Questions")

    # ----------------------------------------------
    # Initialize UI chat history
    # ----------------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


    # ----------------------------------------------
    # Display previous UI messages
    # ----------------------------------------------

    for message in st.session_state["chat_history"]:

        if message["role"] == "user":

            with st.chat_message("user"):

                st.markdown(
                    message["content"]
                )

        else:

            with st.chat_message("assistant"):

                st.markdown(
                    message["content"]
                )

                # Display sources
                if message.get("sources"):

                    st.markdown(
                        "**📚 Sources**"
                    )

                    for i, source in enumerate(
                        message["sources"]
                    ):

                        start = source["start_timestamp"]
                        end = source["end_timestamp"]
                        source_url = source["url"]

                        st.markdown(
                            f"**Source {i + 1}** · "
                            f"🕐 {start} – {end}  \n"
                            f"[▶ Watch from {start}]"
                            f"({source_url})"
                        )


    # ----------------------------------------------
    # Chat input
    # ----------------------------------------------

    question = st.chat_input(
        "Ask anything about this video..."
    )


    # ----------------------------------------------
    # Process new question
    # ----------------------------------------------

    if question:

        # Show user's question immediately
        with st.chat_message("user"):

            st.markdown(question)


        result = st.session_state["video_result"]

        answer_question = result["answer_question"]


        # ------------------------------------------
        # Generate answer
        # ------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the video..."
            ):

                try:

                    qa_result = answer_question(
                        question
                    )

                    answer = qa_result["answer"]
                    sources = qa_result["sources"]

                    st.markdown(answer)


                    # ----------------------------------
                    # Sources
                    # ----------------------------------

                    st.markdown(
                        "**📚 Sources**"
                    )

                    for i, source in enumerate(
                        sources
                    ):

                        start = source["start_timestamp"]
                        end = source["end_timestamp"]
                        source_url = source["url"]

                        st.markdown(
                            f"**Source {i + 1}** · "
                            f"🕐 {start} – {end}  \n"
                            f"[▶ Watch from {start}]"
                            f"({source_url})"
                        )


                    # ----------------------------------
                    # Store ONLY for UI display
                    # ----------------------------------

                    st.session_state[
                        "chat_history"
                    ].append({
                        "role": "user",
                        "content": question
                    })

                    st.session_state[
                        "chat_history"
                    ].append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })


                except Exception as e:

                    st.error(
                        f"Something went wrong: {str(e)}"
                    )