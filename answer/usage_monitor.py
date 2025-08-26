import time
from contextlib import contextmanager
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class UsageMonitor:
    """API 사용량 모니터링을 위한 클래스"""
    
    def __init__(self):
        self.total_requests = 0
        self.total_time = 0.0
        self.error_count = 0
        self.start_times = {}
    
    @contextmanager
    def track_request(self):
        """API 요청을 추적하는 컨텍스트 매니저"""
        request_id = id(self)
        start_time = time.time()
        self.start_times[request_id] = start_time
        self.total_requests += 1
        
        try:
            yield
        except Exception as e:
            self.error_count += 1
            logger.error(f"API request failed: {e}")
            raise
        finally:
            end_time = time.time()
            if request_id in self.start_times:
                request_time = end_time - self.start_times[request_id]
                self.total_time += request_time
                del self.start_times[request_id]
    
    def print_usage_report(self):
        """사용량 리포트 출력"""
        avg_time = self.total_time / self.total_requests if self.total_requests > 0 else 0
        success_rate = (self.total_requests - self.error_count) / self.total_requests * 100 if self.total_requests > 0 else 0
        
        print(f"\n=== API 사용량 리포트 ===")
        print(f"총 요청 수: {self.total_requests}")
        print(f"성공 요청 수: {self.total_requests - self.error_count}")
        print(f"실패 요청 수: {self.error_count}")
        print(f"성공률: {success_rate:.1f}%")
        print(f"총 소요 시간: {self.total_time:.2f}초")
        print(f"평균 응답 시간: {avg_time:.2f}초")
        print(f"========================\n")
    
    def reset(self):
        """통계 초기화"""
        self.total_requests = 0
        self.total_time = 0.0
        self.error_count = 0
        self.start_times.clear()

# 전역 인스턴스 생성
usage_monitor = UsageMonitor()