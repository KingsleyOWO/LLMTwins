# LLMTwins
https://docs.phidata.com/agents/introduction

## Environment

#### Environment Variables:
- OPENAI_API_KEY: OpenAI API Key

## Installation
```bash=
python3.10 -m venv env
source env/bin/active
pip3 install -r requirements.txt
```

## Run
```bash=
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## AGENT TOOLS
```
描述一個AI助手(超級行事曆幫手)舉凡十二星座每日每周每月運勢幸運色到農民曆各式吉時(搬家,祭祀,嫁娶,開市等)都可以提醒你或幫你找好日子和好的時辰,然後也會提醒你甚麼節日快到了
有記憶功能可以讓你設定要提醒你的日子然後用最適合那個日子的話通知你.後續可以的話利用API去查找更準確的資訊可以的話開發AI的記憶功能增加更強大的客製化性
```
