"""
阿里云百炼 LLM 客户端
调用 DashScope API（兼容 OpenAI 格式）
"""

import json
import os
import time
from typing import List, Dict, Any, Optional
import requests


DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
DEFAULT_MODEL = "qwen-max"  # 百炼最强模型
FALLBACK_MODELS = ["qwen-plus", "qwen-turbo"]


def get_api_key() -> str:
    """获取百炼 API Key"""
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            key = os.environ.get("DASHSCOPE_API_KEY", "")
        except ImportError:
            pass
    return key


class DashScopeClient:
    """阿里云百炼 API 客户端"""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.api_key = get_api_key()
        self.model = model

    def check_key(self) -> bool:
        """检查 API Key 是否有效"""
        if not self.api_key:
            return False
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            resp = requests.post(
                DASHSCOPE_URL,
                headers=headers,
                json={
                    "model": "qwen-turbo",
                    "messages": [{"role": "user", "content": "hi"}],
                    "max_tokens": 5,
                },
                timeout=10,
            )
            return resp.status_code == 200
        except Exception:
            return False

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
    ) -> str:
        """调用百炼 LLM 获取回复"""

        if not self.api_key:
            raise ValueError(
                "❌ DASHSCOPE_API_KEY 未配置\n"
                "  请设置环境变量或在 .env 中配置:\n"
                "  DASHSCOPE_API_KEY=sk-xxx\n"
                "  获取: https://bailian.console.aliyun.com/#/api-key"
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            data["response_format"] = response_format

        errors = []
        models_to_try = [self.model] + FALLBACK_MODELS

        for attempt, model in enumerate(models_to_try):
            data["model"] = model
            try:
                resp = requests.post(
                    DASHSCOPE_URL,
                    headers=headers,
                    json=data,
                    timeout=120,
                )

                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]

                body = resp.json()
                err_code = body.get("code", "")
                err_msg = body.get("message", resp.text)

                if resp.status_code == 401:
                    raise ValueError(f"API Key 无效: {err_msg}")
                elif "Throttling" in err_code or resp.status_code == 429:
                    wait = 5 * (attempt + 1)
                    print(f"  ⚠️ 限流，等待 {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    errors.append(f"{model}: [{err_code}] {err_msg[:80]}")
                    continue

            except requests.Timeout:
                errors.append(f"{model}: 超时")
                continue
            except ValueError:
                raise
            except Exception as e:
                errors.append(f"{model}: {str(e)[:60]}")
                continue

        raise RuntimeError("所有模型均失败:\n" + "\n".join(errors))

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096,
    ) -> Dict:
        """请求 JSON 格式输出"""
        content = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # 从 markdown 代码块中提取
        content = content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)


def create_client(model: Optional[str] = None) -> DashScopeClient:
    return DashScopeClient(model or DEFAULT_MODEL)


if __name__ == "__main__":
    client = create_client()
    key_valid = client.check_key()
    print(f"📋 百炼 API Key 状态: {'✅ 有效' if key_valid else '❌ 未配置'}")

    if key_valid:
        print("\n🔍 测试调用...")
        content = client.chat([
            {"role": "system", "content": "你是一个 AI 专家。用一句话介绍自己。"},
            {"role": "user", "content": "说你好"},
        ])
        print(f"🤖 {content}")
