import os
import platform
import time

class HardwareProfiler:
    """Đo đạc cấu hình phần cứng và ước tính năng lực tính toán"""
    @staticmethod
    def inspect():
        cpu_count = os.cpu_count() or 1
        system = platform.system()
        machine = platform.machine()
        
        # Benchmark tốc độ tính toán thô (FLOPS benchmark mini)
        t0 = time.time()
        acc = 0.0
        for i in range(100000):
            acc += (i * 0.0001) ** 0.5
        duration = max(time.time() - t0, 0.0001)
        estimated_mflops = round((100000 / duration) / 1000000.0, 2)

        return {
            "cpu_cores": cpu_count,
            "os": system,
            "architecture": machine,
            "estimated_mflops": estimated_mflops,
            "concurrency_limit": max(1, cpu_count * 2)
        }
