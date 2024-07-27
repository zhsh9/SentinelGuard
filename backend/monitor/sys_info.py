"""
Retrieves system resource usage information
"""

import psutil
import time

def get_system_usage():
    # 获取CPU使用率
    cpu_percent = psutil.cpu_percent(interval=1)

    # 获取物理内存使用情况
    memory_info = psutil.virtual_memory()

    # 获取硬盘使用情况
    disk_info = psutil.disk_usage('/')

    # 获取网络速率
    net_io_1 = psutil.net_io_counters()
    time.sleep(1)
    net_io_2 = psutil.net_io_counters()
    net_upload_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) / 1024  # KB/s
    net_download_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) / 1024  # KB/s

    return {
        "cpu_percent": cpu_percent,
        "memory_total_gb": memory_info.total / (1024 ** 3),
        "memory_used_gb": memory_info.used / (1024 ** 3),
        "memory_available_gb": memory_info.available / (1024 ** 3),
        "memory_percent": memory_info.percent,
        "disk_total_gb": disk_info.total / (1024 ** 3),
        "disk_used_gb": disk_info.used / (1024 ** 3),
        "disk_free_gb": disk_info.free / (1024 ** 3),
        "disk_percent": disk_info.percent,
        "net_upload_speed_kbps": net_upload_speed,
        "net_download_speed_kbps": net_download_speed
    }

# 测试函数
if __name__ == "__main__":
    usage = get_system_usage()
    print(f"CPU使用率: {usage['cpu_percent']}%")
    print(f"总内存: {usage['memory_total_gb']:.2f} GB")
    print(f"已用内存: {usage['memory_used_gb']:.2f} GB")
    print(f"可用内存: {usage['memory_available_gb']:.2f} GB")
    print(f"内存使用率: {usage['memory_percent']}%")
    print(f"总硬盘: {usage['disk_total_gb']:.2f} GB")
    print(f"已用硬盘: {usage['disk_used_gb']:.2f} GB")
    print(f"可用硬盘: {usage['disk_free_gb']:.2f} GB")
    print(f"硬盘使用率: {usage['disk_percent']}%")
    print(f"网络上行速率: {usage['net_upload_speed_kbps']:.2f} KB/s")
    print(f"网络下行速率: {usage['net_download_speed_kbps']:.2f} KB/s")
