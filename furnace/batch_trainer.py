from furnace.tensor_ops import TensorOps
from crucible.thermal_governor import ThermalGovernor

class BatchFurnaceTrainer:
    """Huấn luyện hàng loạt vector dữ liệu với tốc độ cao"""
    @staticmethod
    def train_batch(vectors, weights, bias, lr=0.05):
        updated_weights = list(weights)
        curr_bias = bias
        total_flops = 0

        for i, vec in enumerate(vectors):
            # Tính toán tiến (Forward pass)
            z = TensorOps.vector_dot(vec, updated_weights) + curr_bias
            pred = 1.0 / (1.0 + 2.71828 ** (-max(min(z, 500), -500)))
            
            # Tính toán lùi (Backward gradient)
            target = 1.0 if vec[0] > 0.5 else 0.0
            error = (target - pred)
            
            for j in range(len(updated_weights)):
                updated_weights[j] += lr * error * vec[j]
                updated_weights[j] = round(updated_weights[j] * 0.999, 4)
            curr_bias += lr * error

            total_flops += len(vec) * 4
            if i % 100 == 0:
                ThermalGovernor.pace_execution(len(vectors))

        return {
            "weights": [round(w, 4) for w in updated_weights],
            "bias": round(curr_bias, 4),
            "flops_spent": total_flops
        }
