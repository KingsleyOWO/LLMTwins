from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from models import UserInput, AgentResponse
from pydantic import BaseModel
from typing import Optional
from datetime import date
import json
from dotenv import load_dotenv
# 載入環境變數
load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
async def health():
    return {"result": "Healthy Server!"}

# 業務邏輯函數
def get_holiday_suggestions(query_date: date) -> str:
    # 假設有一個函數可以根據日期返回節日建議
    holidays = {
        date(2025, 1, 1): "元旦快樂！適合與家人團聚。",
        date(2025, 2, 14): "情人節快樂！適合與愛人共度浪漫時光。",
        # 添加更多節日
    }
    return holidays.get(query_date, "今天沒有特別的節日。")

def get_horoscope(zodiac_sign: str, period: str) -> str:
    # 假設有一個函數可以根據星座和期間返回運勢
    horoscope_data = {
        "白羊座": {
            "daily": "今天你會有很多精力，適合開始新的項目。",
            "weekly": "本週運勢良好，適合人際交往。",
            "monthly": "本月有財運，但注意健康問題。"
        },
        "金牛座": {
            "daily": "今天需要注意財務管理，避免不必要的支出。",
            "weekly": "本週可能會遇到一些挑戰，但能夠克服。",
            "monthly": "本月運勢平穩，適合規劃長期目標。"
        },
        # 添加更多星座
    }
    return horoscope_data.get(zodiac_sign, {}).get(period, "運勢資料暫無。")

def process_user_input(user_input: UserInput) -> AgentResponse:
    role = user_input.role
    message = user_input.message
    suggestions = None
    horoscope = None

    # 處理節日或良辰吉時的詢問
    if "節日" in message or "良辰吉時" in message:
        if user_input.query_date:
            suggestions = get_holiday_suggestions(user_input.query_date)
        else:
            suggestions = "請提供具體的日期，以便我提供相關的建議。"

    # 處理星座運勢的詢問
    if "運勢" in message:
        if user_input.zodiac_sign:
            # 判斷查詢的期間
            if "今天" in message:
                period = "daily"
            elif "這週" in message:
                period = "weekly"
            elif "這月" in message:
                period = "monthly"
            else:
                period = "daily"  # 預設為每日運勢
            horoscope = get_horoscope(user_input.zodiac_sign, period)
        else:
            horoscope = "請提供你的星座，以便我提供運勢資訊。"

    response_message = ""
    if suggestions:
        response_message += suggestions + "\n"
    if horoscope:
        response_message += horoscope

    return AgentResponse(
        role=role,
        message=response_message.strip()
    )

# 定義 Agents
def self_introduction():
    return "我的名字叫做小明，我是一個 AI 聊天機器人，我可以幫助你進行自我介紹。"

self_intro_agent = Agent(
   name="Self-introduction Agent",
   role="自我介紹",
   tools=[self_introduction],
   show_tool_calls=True
)

def analyse_project():
    return "我是專案分析 Agent，我可以幫助你分析專案。"

analysis_project_agent = Agent(
   name="Project analysis Agent",
   role= "專案分析",
   tools=[analyse_project],
   show_tool_calls=True
)

# 更新 super_calendar_agent 的角色和工具
def super_calendar():
    return "我是超級行事曆幫手，我可以提供各式星座運勢的資訊和各種節日應該如何慶祝或祭祀。"

super_calendar_agent = Agent(
    name="Super Calendar Agent",
    role="行事曆和運勢大師",
    tools=[super_calendar],
    show_tool_calls=True
)

# 建立 Agent 團隊，包含所有 Agents
agent_team = Agent(
    model=OpenAIChat(
        id = "gpt-4o",
        temperature = 1,
        timeout = 30
    ),
    name="Agent Team",
    team=[self_intro_agent, analysis_project_agent, super_calendar_agent],
    add_history_to_messages=True,
    num_history_responses=3,
    show_tool_calls=False,
    tool_call_limit=1
)

# 更新 /prompt 端點以整合超級行事曆和運勢大師功能
@app.post("/prompt")
async def prompt_endpoint(user_input: UserInput):
    response = process_user_input(user_input)
    return {"result": True, "message": response.message}
