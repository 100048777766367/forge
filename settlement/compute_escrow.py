import os
import json

COMPUTE_LEDGER_FILE = "synapses/compute_ledger.json"

class ComputeEscrow:
    """Ký quỹ và phân phối tín dụng tính toán (Compute Credits)"""
    @staticmethod
    def log_compute(consumer_repo, flops_delivered):
        data = {"total_flops_mined": 0, "client_allocations": {}}
        if os.path.exists(COMPUTE_LEDGER_FILE):
            try:
                with open(COMPUTE_LEDGER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception: pass

        data["total_flops_mined"] += flops_delivered
        clients = data.setdefault("client_allocations", {})
        clients[consumer_repo] = clients.get(consumer_repo, 0) + flops_delivered

        os.makedirs(os.path.dirname(COMPUTE_LEDGER_FILE), exist_ok=True)
        with open(COMPUTE_LEDGER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # 1.000.000 FLOPS = 1 Compute Credit
        credits_earned = round(flops_delivered / 1000000.0, 4)
        print(f"💰 [THANH TOÁN NĂNG LƯỢNG] Nạp +{flops_delivered} FLOPS ({credits_earned} Credits) cho '{consumer_repo}'!")
        return credits_earned
