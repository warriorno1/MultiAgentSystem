from agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # ==================================================
    # STEP 1 - SEARCH AGENT
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 1: Search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_result"] = search_result["messages"][-1].content

    print("\nSearch Result:\n")
    print(state["search_result"])


    # ==================================================
    # STEP 2 - READER AGENT
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 2: Reader agent is scraping top resources ...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about '{topic}',
pick the most relevant URL and scrape it for deeper content.

Search Results:
{state["search_result"][:800]}
"""
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n")
    print(state["scraped_content"])


    # ==================================================
    # STEP 3 - WRITER CHAIN
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 3: Writer is drafting the report ...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n"
        f"{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n"
        f"{state['scraped_content']}"
    )

    writer_result = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    # Handle AIMessage response
    if hasattr(writer_result, "content"):
        state["report"] = writer_result.content
    else:
        state["report"] = writer_result

    print("\nFinal Report:\n")
    print(state["report"])


    # ==================================================
    # STEP 4 - CRITIC CHAIN
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 4: Critic is reviewing the report ...")
    print("=" * 50)

    critic_result = critic_chain.invoke({
        "report": state["report"]
    })

    if hasattr(critic_result, "content"):
        state["feedback"] = critic_result.content
    else:
        state["feedback"] = critic_result

    print("\nCritic Report:\n")
    print(state["feedback"])


    return state


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")

    result = run_research_pipeline(topic)