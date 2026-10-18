from concurrent.futures import ThreadPoolExecutor

class TaskSharder:
    """Bẻ nhỏ khối dữ liệu lớn thành các lát cắt tính toán song song"""
    @staticmethod
    def map_reduce(items, worker_func, max_workers=8):
        if not items:
            return []
        
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for res in executor.map(worker_func, items):
                if res is not None:
                    results.append(res)
        return results
