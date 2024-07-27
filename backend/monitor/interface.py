"""
Util functions for listing interfaces and their stats on the system.
"""

import psutil

def get_network_interfaces() -> list:
    """
    Retrieves information about network interfaces.

    Returns:
        A list of dictionaries, where each dictionary represents an interface and contains the following keys:
        - 'name': The name of the interface.
        - 'addresses': A list of dictionaries representing the addresses associated with the interface.
            Each address dictionary contains the following keys:
            - 'family': The address family (2 for IPv4, 18 for UNIX domain socket, 30 for IPv6).
            - 'address': The IP address.
            - 'netmask': The network mask.
            - 'broadcast': The broadcast address.
        - 'is_up': A boolean indicating whether the interface is up or not.
        - 'speed': The speed of the interface in Mbps.
        - 'duplex': The duplex mode of the interface.
        - 'mtu': The maximum transmission unit (MTU) of the interface.
    """
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    
    result = []
    for interface_name, addrs in interfaces.items():
        interface_info = {
            'name': interface_name,
            'addresses': [{'family': str(addr.family), 'address': addr.address, 'netmask': addr.netmask, 'broadcast': addr.broadcast} for addr in addrs],
            'is_up': stats[interface_name].isup,
            'speed': stats[interface_name].speed,
            'duplex': stats[interface_name].duplex,
            'mtu': stats[interface_name].mtu
        }
        result.append(interface_info)
        
    return result

def filter_interface_and_ipv4(interfaces: list) -> list:
    result = []
    for interface in interfaces:
        addresses, is_up, name = interface['addresses'], interface['is_up'], interface['name']
        if is_up:
            for addr in addresses:
                if addr['family'] == '2':
                    result.append({'name': name, 'address': addr['address']})
    if len(result) != 0:
        # 按照接口的ip地址排序
        result = sorted(result, key=lambda x: int(x['address'].split('.')[0]))
    return result

# 输出启动的网络接口
def get_alive_interface() -> list:
    interfaces = get_network_interfaces()
    interfaces = filter_interface_and_ipv4(interfaces)
    return interfaces

# 调用函数并打印结果
if __name__ == "__main__":
    interfaces = get_alive_interface()
    print(interfaces)
