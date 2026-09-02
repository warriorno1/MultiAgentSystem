import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Research Pipeline", page_icon="🔎", layout="wide")

st.title("🔎 Research Pipeline")
st.caption("Search → Read → Write → Critique, powered by your `pipeline.py`")

# --- Session state setup ---
if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False

# --- Input form ---
with st.form("topic_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of AI on renewable energy grids",
    )
    submitted = st.form_submit_button("Run Pipeline", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.running = True
        st.session_state.result = None

        status_box = st.status("Starting pipeline...", expanded=True)

        try:
            status_box.write("Step 1/4 — Search agent gathering sources...")
            status_box.write("Step 2/4 — Reader agent scraping content...")
            status_box.write("Step 3/4 — Writer drafting the report...")
            status_box.write("Step 4/4 — Critic reviewing the report...")

            # Runs the full pipeline synchronously (as defined in pipeline.py).
            # The individual step logs above are shown up front since the
            # underlying function does not yield intermediate progress.
            result = run_research_pipeline(topic.strip())

            st.session_state.result = result
            status_box.update(label="Pipeline complete ✅", state="complete", expanded=False)
        except Exception as e:
            status_box.update(label="Pipeline failed ❌", state="error", expanded=True)
            st.exception(e)
        finally:
            st.session_state.running = False

# --- Results display ---
result = st.session_state.result

if result:
    st.divider()
    st.subheader("Results")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(result.get("report", "_No report generated._"))
        if result.get("report"):
            st.download_button(
                "Download report (.md)",
                data=result["report"],
                file_name="report.md",
                mime="text/markdown",
            )

    with tab_feedback:
        st.markdown(result.get("feedback", "_No feedback generated._"))

    with tab_search:
        st.text(result.get("search_result", "_No search results._"))

    with tab_scraped:
        st.text(result.get("scraped_content", "_No scraped content._"))
elif not submitted:
    st.info("Enter a topic above and click **Run Pipeline** to get started.")