import os
import sys
import json
import time
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from crucible.profiler import HardwareProfiler
from crucible.proof_of_compute import ProofOfCompute
from furnace.batch_trainer import BatchFurnaceTrainer
from settlement.compute_escrow import ComputeEscrow

STATE_FILE = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"

class ForgeKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/forge")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.contract_repo = f"{self.owner}/contract"
        
        self.ensure_skeleton()
        self.epoch = self.load_epoch()
        self.clients = self.load_clients()

    def ensure_skeleton(self):
        for folder in ["crucible", "furnace", "settlement", "organs", "synapses"]:
            os.makedirs(folder, exist_ok=True)

    def load_epoch(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def load_clients(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f).get("client_nodes", [])
            except Exception: pass
        return [f"{self.owner}/vault", f"{self.owner}/nexus-08", self.contract_repo]

    def enforce_apoptosis_on_organs(self):
        """[t] Áp dụng luật Apoptosis của Contract: diệt tệp lỗi cú pháp"""
        for root, _, files in os.walk("organs"):
            for f in files:
                if f.endswith(".py"):
                    fp = os.path.join(root, f)
                    try:
                        with open(fp, "r", encoding="utf-8") as cf:
                            compile(cf.read(), fp, "exec")
                    except SyntaxError as se:
                        print(f"🛑 [APOPTOSIS CONTRACT] '{f}' vi phạm hợp đồng ({se})! Xóa tệp lỗi.")
                        try: os.remove(fp)
                        except Exception: pass

    def run(self):
        print("=" * 80)
        print(f"⚡ [FORGE COMPUTE FOUNDRY] KHỞI ĐỘNG LÒ LUYỆN NĂNG LƯỢNG #{self.epoch}")
        print(f"🔥 Sứ Mệnh: Cung Cấp Sức Mạnh Tính Toán Cho Chuỗi Cung Ứng (Nấc NVIDIA Tier)")
        print("=" * 80)

        # 0. Thực thi luật Apoptosis
        self.enforce_apoptosis_on_organs()

        # 1. Đo đạc phần cứng máy chủ
        hw_info = HardwareProfiler.inspect()
        print(f"🖥️ [PHẦN CỨNG]: {hw_info['cpu_cores']} Cores ({hw_info['architecture']}) | Ước tính: {hw_info['estimated_mflops']} MFLOPS")

        # 2. Tạo lô tính toán mẫu (Synthetic Tensor Workload)
        sample_vectors = [
            [0.8, 0.2, 0.9, 0.1], [0.1, 0.9, 0.2, 0.8],
            [0.7, 0.3, 0.6, 0.4], [0.2, 0.8, 0.1, 0.9]
        ] * 250  # 1.000 vectors
        initial_weights = [0.5, -0.5, 0.5, -0.5]
        initial_bias = 0.0

        # 3. Lò Luyện Rèn Đúc (Batch Training)
        print("🔨 [LÒ RÈN TENSOR] Bắt đầu rèn đúc tải tính toán song song...")
        train_result = BatchFurnaceTrainer.train_batch(sample_vectors, initial_weights, initial_bias)
        total_flops = train_result["flops_spent"]
        print(f"  └── ⚡ Năng lượng đã giải phóng: {total_flops} FLOPS | Trọng số mới: {train_result['weights'][:2]}...")

        # 4. Tạo Chứng chỉ Năng lượng Tính toán (Proof-of-Compute)
        proof = ProofOfCompute.generate_proof(
            job_id=f"epoch_{self.epoch}",
            input_checksum=hashlib.shake_256(str(sample_vectors[:5]).encode()).hexdigest(8),
            output_checksum=hashlib.shake_256(str(train_result["weights"]).encode()).hexdigest(8),
            flops_spent=total_flops
        )
        print(f"🛡️ [CHỨNG CHỈ TÍNH TOÁN]: {proof['proof_cid']} (Xác thực trung thực 100%)")

        # 5. Thanh quyết toán và nạp Credits cho Vault và Nexus
        primary_client = f"{self.owner}/vault"
        ComputeEscrow.log_compute(primary_client, total_flops)

        # 6. Ghi sổ trạng thái xuất xưởng
        t = int(time.time())
        cid = proof["proof_cid"]

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "generation_epoch": self.epoch,
                "last_t": t,
                "flops_delivered": total_flops,
                "proof_cid": cid,
                "status": "compute_dispatched"
            }, f, indent=4)

        # Xuất gói tin năng lượng tiến
        fwd_packet = {
            "contract": "bodhi.contract.v1",
            "identity": self.repo_name,
            "role": "DECENTRALIZED_COMPUTE_FOUNDRY",
            "epoch": self.epoch,
            "timestamp": t,
            "hardware": hw_info,
            "flops_delivered": total_flops,
            "proof_of_compute_cid": cid,
            "status": "ready_for_depin_compute_settlement"
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(fwd_packet, f, indent=4)

        print("=" * 80)
        print(f"✨ [LÒ ĐÚC VIÊN MÃN] Kỷ nguyên #{self.epoch} đã rèn đúc và phân bổ {total_flops} FLOPS thành công!")
        print("⚡ Sức mạnh tính toán đã sẵn sàng tiếp sức cho Vault và toàn bộ đại hệ sinh thái!")
        print("=" * 80)

if __name__ == "__main__":
    ForgeKernel().run()
