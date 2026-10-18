import math

class TensorOps:
    """Các phép toán ma trận và vector hóa siêu tốc thuần thư viện chuẩn"""
    @staticmethod
    def vector_dot(v1, v2):
        return sum(a * b for a, b in zip(v1, v2))

    @staticmethod
    def vector_normalize(v):
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        return [round(x / norm, 4) for x in v]

    @staticmethod
    def matrix_multiply(matrix, vector):
        return [TensorOps.vector_dot(row, vector) for row in matrix]

    @staticmethod
    def sigmoid_array(arr):
        return [round(1.0 / (1.0 + math.exp(-max(min(x, 500), -500))), 4) for x in arr]
