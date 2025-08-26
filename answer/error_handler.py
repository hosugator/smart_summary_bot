import openai
import time
import logging
from typing import Optional
from usage_monitor import usage_monitor

logger = logging.getLogger(__name__)

class APIErrorHandler:
    """OpenAI API 에러 처리를 위한 클래스"""
    
    @staticmethod
    def handle_api_error(error: Exception, attempt: int = 1) -> bool:
        """
        API 에러 처리 및 재시도 여부 결정
        
        Args:
            error: 발생한 에러
            attempt: 현재 시도 횟수
            
        Returns:
            재시도 여부 (True면 재시도)
        """
        if isinstance(error, openai.RateLimitError):
            wait_time = min(60, 2 ** attempt)
            logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return attempt < 3
        
        elif isinstance(error, openai.APIConnectionError):
            wait_time = min(30, 2 ** attempt)
            logger.warning(f"API connection error. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return attempt < 3
            
        elif isinstance(error, openai.InternalServerError):
            wait_time = min(30, 2 ** attempt)
            logger.warning(f"Internal server error. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            return attempt < 2
            
        else:
            logger.error(f"Unhandled API error: {error}")
            return False

def robust_summarize(client: openai.OpenAI, text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    에러 처리 및 사용량 모니터링이 포함된 텍스트 요약
    
    Args:
        client: OpenAI 클라이언트
        text: 요약할 텍스트
        model: 사용할 모델
        
    Returns:
        요약된 텍스트
    """
    attempt = 1
    max_attempts = 3
    
    while attempt <= max_attempts:
        try:
            prompt = f"""
다음 뉴스 기사를 100자 내외로 간결하게 요약해주세요. 핵심 내용만 포함하여 한글로 작성해주세요:

"{text}"

요약:
"""
            
            with usage_monitor.track_request():
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "당신은 뉴스를 요약하는 전문가입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            if APIErrorHandler.handle_api_error(e, attempt):
                attempt += 1
                continue
            else:
                logger.error(f"Failed to summarize text after {attempt} attempts: {e}")
                return "요약 실패: API 에러"
    
    return "요약 실패: 최대 재시도 횟수 초과"