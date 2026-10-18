import time

class ThermalGovernor:
    """Điều hòa nhịp thở tính toán, bảo vệ CPU không bị treo đơ"""
    @staticmethod
    def pace_execution(batch_size):
        # Nghỉ nhẹ giữa các đợt tính toán lớn để giải phóng I/O và RAM
        if batch_size > 500:
            time.sleep(0.05)
