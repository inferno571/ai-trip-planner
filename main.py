from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
from fastapi.responses import StreamingResponse
import json
import traceback
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    async def event_generator():
        try:
            graph = GraphBuilder(model_provider="gemini")
            react_app = graph()
            messages = {"messages": [query.question]}
            
            async for event in react_app.astream(messages, stream_mode="updates"):
                if "agent" in event:
                    agent_messages = event["agent"].get("messages", [])
                    if agent_messages:
                        last_msg = agent_messages[-1]
                        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                            for tc in last_msg.tool_calls:
                                yield json.dumps({"type": "tool_call", "tool": tc["name"]}) + "\n"
                        else:
                            raw_content = last_msg.content
                            if isinstance(raw_content, list):
                                final_output = "\n".join(
                                    part.get("text", "") if isinstance(part, dict) else str(part)
                                    for part in raw_content
                                )
                            else:
                                final_output = str(raw_content)
                            yield json.dumps({"type": "final_answer", "content": final_output}) + "\n"
                elif "tools" in event:
                    yield json.dumps({"type": "system_status", "content": "Synthesizing final travel plan..."}) + "\n"
        except Exception as e:
            traceback.print_exc()
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"
            
    return StreamingResponse(event_generator(), media_type="application/x-ndjson")