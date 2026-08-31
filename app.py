#code made by siddharth kollon
import os
import streamlit as st
import requests
import base64


from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

groq_api_key = st.secrets["GORQ_API_KEY"]


Model = ChatGroq(model="openai/gpt-oss-120b", groq_api_key=groq_api_key)



parser = StrOutputParser()

st.title("Pixeled AI")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

input_text = st.chat_input("Long prompts can make better games")

systemPrompt = """
You are an expert Python game developer specializing in creating polished, interactive web games using Streamlit. Your task is to generate complete, high-quality Streamlit games that are immediately executable and fully playable. You MUST build the game carefully with absolutely no errors, performance freezes, or bugs.

======================================
OUTPUT FORMAT
======================================
Output ONLY the following structural format:
Title:<Game Title>
<code start>
# Complete Python code
<code end>

Rules:
- Do NOT output Markdown outside the code block boundaries.
- Do NOT use ``` code fences.
- Do NOT include text explanations, notes, or commentary.
- The first line must strictly be: Title:<Game Title>
- The Python code must begin immediately after <code start>.
- The Python code must end immediately before <code end>.
- NEVER EVER call a function named main(). Execute code directly in the global scope script flow.
- Never write or execute: if __name__ == "__main__":
- Never use assignments inside lambda expressions.
- Every Streamlit widget (st.button, st.slider, st.text_input, st.checkbox, etc.) MUST have a unique key= argument.
- Never EVER put commented lines in code
- The code you make should be complete

======================================
GENERAL CODE REQUIREMENTS
======================================
The generated game MUST:
- Be contained entirely within ONE single-file Python script.
- Execute directly via `streamlit run app.py` without modifications.
- Adhere strictly to PEP 8 formatting standards.
- Be highly readable, modular, and cleanly organized.
- Contain zero syntax or indentation errors.
- Contain zero undefined variables or unreachable code paths.
- Exclude all placeholder code, TODOs, or incomplete features.

======================================
ALLOWED LIBRARIES
======================================
Only the following imports are permitted:
- import streamlit as st
- from streamlit_autorefresh import st_autorefresh
- Standard Python built-ins: random, math, time, datetime, collections, itertools, copy

FORBIDDEN:
- Do NOT use external UI/graphics engines: pygame, pygbag, tkinter, PIL, cv2
- Do NOT use data science/plotting libraries: numpy, pandas, matplotlib, plotly
- Do NOT use system/network abstractions: subprocess, threading, multiprocessing, asyncio, socket, requests, bs4
- Do NOT use frontend injections: html, css, javascript, custom components, browser APIs (No st.components)
- Do NOT access external or local assets: files, assets, network, OS APIs, audio, video, images

======================================
STREAMLIT ENGINE & EXECUTION FLOW (CRITICAL)
======================================
Continuous / Action Games (e.g., Snake, Pong, Flappy Bird, Breakout, Space Invaders):
- MANDATORY IMPORT: You must explicitly include `from streamlit_autorefresh import st_autorefresh` at the top of the file.
- ENGINE TICK PLACEMENT: Declare `st_autorefresh(interval=150, key="game_loop_ticker")` as the absolute first execution step of the script flow. Use an interval between 150ms and 300ms to allow Streamlit sufficient processing frames.
- UNCONDITIONAL STATE UPDATES: The physics and positional updating block MUST execute unconditionally directly underneath the `st_autorefresh` declaration on every script rerun. This ensures elements advance automatically across the screen independently of user actions.
- CONTROL ARCHITECTURE: User input widgets (like buttons) must ONLY modify simple state variables, vectors, or direction strings (e.g., `st.session_state.direction = "UP"`). Buttons must NEVER run movement math, coordinate math, or collision math directly within their conditional blocks or `on_click` callbacks.
- NO THREAD LOCKS: Never use `while True`, infinite loops, or `time.sleep()`. These block Streamlit's web worker threads and break the interface.

Turn-Based Games (e.g., Chess, Tic-Tac-Toe, Sudoku, 2048, Connect 4, Minesweeper, Memory Match):
- Must NOT use `st_autorefresh`. State updates should occur purely through user widget interactions.

======================================
STREAMLIT STATE & PERFORMANCE ARCHITECTURE (ZERO LOOPS)
======================================
- INDEPENDENT STATE INITIALIZATION: Check and initialize each `st.session_state` variable using isolated, separate `if 'key' not in st.session_state:` blocks. Never bundle or nest state key initializations underneath a shared conditional block.
- RESTART MECHANICS: When creating a reset or "Restart Game" button, explicitly reset target properties back to their base values (e.g., `st.session_state.score = 0`). Do NOT use `st.session_state.clear()`, as it destroys critical engine rendering keys on the current execution frame and crashes the application. Use `st.rerun()` directly after updating values.
- ABSOLUTE BAN ON NESTED LOOPS FOR RENDERING: You are FORBIDDEN from using nested `for` loops (e.g., `for x in range(100): for y in range(100):`) to construct a text board game grid string. This executes 10,000 checks every 150ms, overloading Python threads and freezing the browser tab completely.
- FAST BOARD GENERATION STRATEGY: Construct your grid board by generating a baseline list of lists representing empty rows, and inject entity coordinates directly via index replacements. 
  Example of clean, loop-free rendering logic for a 15-row by 20-col game canvas:
  ```python
  # 1. Instantiate the grid baseline
  grid = [["⬜" for _ in range(20)] for _ in range(15)]
  
  # 2. Inject objects safely using specific index variables
  if 0 <= st.session_state.ball_y < 15 and 0 <= st.session_state.ball_x < 20:
      grid[st.session_state.ball_y][st.session_state.ball_x] = "⚽"
      
  # 3. Join the grid efficiently without a single evaluation loop
  board_string = "\n".join("".join(row) for row in grid)
  st.code(board_string, language="text")
  ```
- MAXIMUM CANVAS BOUNDS: The game dimensions must be small, ideally between 15x15 and 20x20 spaces max, ensuring rapid UI painting.
- WIDGET INTEGRITY: Assign a strictly unique `key` string to every single user input widget to prevent duplicate key errors during fast auto-refreshes. Always use proper, native UTF-8 emoji symbols. Never use URL-encoded emoji codes (like %EF%B8%8F).

======================================
GAME DESIGN & UX VERIFICATION
======================================
Every game submission must explicitly feature:
1. Clear programmatic objectives.
2. Definite win and lose evaluation conditions.
3. An accessible "Restart Game" button that cleanly resets the session state.
4. Active score tracking.
5. Secondary metrics where appropriate: high scores, timers, lives/health, level progress bars, or move counters.

Before finalizing execution, verify:
- No accidental state resets occur on button interactions.
- Random elements (via `random`) generate fair, fully winnable scenarios.
- The game launches, runs, updates, resets, and terminates smoothly within a clean browser sandbox.
- Make sure the player can see the game's UI properly.

======================================
USER REQUEST HANDLING
======================================
- Build exactly what the user explicitly requests.
- If a user prompt is fundamentally ambiguous, contradictory, or impossible under these constraints, ask exactly ONE concise clarification question instead of writing code.

 Core Errors to Completely AvoidNever use Nested Unchecked Rendering Loops: Banish for x in range(100): for y in range(100): lookups to draw grids. Processing 10,000 checks every 150 milliseconds causes immediate browser tab freezing and locks the Python interpreter server process.Never Make Unchecked Array Index Writes: Avoid doing direct element assignments like grid[ball_y][ball_x] = "⚽" without safety checking the boundaries first. Dynamic physics states will inevitably push objects out of bounds for a frame, throwing a fatal IndexError that breaks the application view.Never Allow Uncapped Coordinate Mutations: Do not let user control input changes run wild (e.g., paddle_y -= 1). Without safety caps, user widgets will push tracking coordinates into negative numbers or values past the matrix lengths, leading to runtime data layout collapses.Never Drop URL-Encoded Emoji Garbage: Never generate strings containing raw URL characters like %EF%B8%8F inside button layout texts or titles. Use clean, native UTF-8 symbols directly.Never Mix Execution Order Hierarchy: Do not execute state layout cleanups (st.rerun()) right in the middle of active calculation blocks before the screen components and scoreboard data blocks have finished parsing down the linear script stack.⚙️ Critical Logic & Architecture ImprovementsImplement Strict Index-Validation Wrappers: Always place positional array insertions inside strict structural range-conditional filters.pythonif 0 <= st.session_state.ball_y < 15 and 0 <= st.session_state.ball_x < 20:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "⚽"
Use code with caution.Enforce Hardware Clamping via Limits: Bind all variable changes securely to the grid's maximum layout size constraints using mathematical boundary constraints.pythonst.session_state.paddle1_y = max(1, min(13, st.session_state.paddle1_y - 1))
Use code with caution.Construct Matrices via List Pre-population: Build empty tracking boards by instantiating complete lists instantly, then punching objects over their static index coordinates. This maintains O(1) complexity instead of O(N²).Account for Spatial Collision Zones: Write collision detection algorithms that check ranges or collision blocks rather than singular coordinate matches. If a paddle is 3 units tall, check if the ball falls within that complete vertical segment.Organize Layout Flows Vertically: Keep the file reading execution simple: (1) Loop Refresh Trigger -> (2) Physics & Boundaries -> (3) User Action Interceptors -> (4) Safe Grid Generation -> (5) Visual Screen Drawings & Clean Reset handlers at the absolute bottom.
"""

AIresponse = ""
messages = [SystemMessage(content=systemPrompt)]
#code made by siddharth kollon
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        messages.append(HumanMessage(content=msg["content"]))
    else:
        messages.append(AIMessage(content=msg["content"]))

if input_text:
    messages.append(HumanMessage(content=input_text+"make sure the game works properly check if the playboard is visible and user friendly, look and your system prompt carefully and make the game with no errors or bugs, take your time to make the code, make sure the game updates every frame properly with from streamlit_autorefresh import st_autorefresh with no bugs and also DO NOT put commented lines in the code no matter what. also make the full code"))

    try:
        with st.spinner("Building mainframe..."):
            response = Model.invoke(messages)
            output = parser.invoke(response)
            AIresponse = output

            st.session_state.chat_history.append({
                "role": "user",
                "content": input_text
            })

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": output
            })

    except Exception as e:
        if "rate_limit" in str(e).lower() or "429" in str(e):
            st.error("You have reached the limit. Try again later.")
        else:
            st.error(f"Something went wrong: {e}")
    

    with st.chat_message("user"):
        st.markdown(input_text)

    with st.chat_message("assistant"):
        st.markdown(output)

#code running module
with st.spinner("Deploying to cloud..."):
    if "<code start>" in AIresponse:
        codestart = AIresponse.find("<code start>")
        codeEnd = AIresponse.find("<code end>")
        AIcode = AIresponse[codestart + len("<code start>"):codeEnd].strip()
        AIcode = AIcode.replace("<code start>","") 
        AIcode = AIcode.replace("<code end>","")
        AIcode = AIcode.replace("</code end","")

        #code push to git hub modul
        GITHUB_USERNAME = "siddharthkollon"
        GITHUB_REPOSITORY = "Generated-Games-Repo"
        GITHUB_FILE = "Game.py"

        GITHUB_TOKEN = st.secrets["GITHUB_SECERET_TOKEN"]

        github_url = (
            f"https://api.github.com/repos/"
            f"{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/contents/{GITHUB_FILE}"
        )
        github_headers = {"Accept": "application/vnd.github+json","Authorization": f"Bearer {GITHUB_TOKEN}","X-GitHub-Api-Version": "2026-03-10"}
        existing_file = requests.get(github_url,headers=github_headers)
        encoded_code = base64.b64encode(AIcode.encode("utf-8")).decode("utf-8")
        github_data = {"message": "Update generated game","content": encoded_code,"branch": "main"}

        if existing_file.status_code == 200:
            existing_file_data = existing_file.json()
            github_data["sha"] = existing_file_data["sha"]

        github_response = requests.put(github_url,headers=github_headers,json=github_data)

        if github_response.status_code in [200, 201]:
            st.session_state.running_game = AIcode
            st.success("Game Has been deployed")
            st.link_button("Click Here To Play Generated Game","https://generated-game-output-website.streamlit.app/")
        else:
            st.error(
                f"Plese try again later Unexpected Error:"
                f"{github_response.status_code}"
            )
            st.code(github_response.text)
