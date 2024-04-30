import subprocess
import matplotlib.pyplot as plt
import sys
import seaborn as sns

def init():
    if len(sys.argv) == 1:
        print("Insufficient arguments")
        sys.exit()
    file_path = sys.argv[1:]
    return file_path

def read(f):
    # tshark 명령어 실행 및 출력 캡처
    result = subprocess.run(["tshark", "-r", f, "-Y", "rtps.sm.id == 0x15", "-T", "fields", "-e", "frame.time_epoch", "-e", "rtps.issueData"], capture_output=True, text=True)
    lines = result.stdout.split('\n')
    return lines

def decoding(lines):
    # 결과를 저장할 리스트
    decoded_lines = []
    hello_world_timestamps = []
    
    for line in lines:
        # 공백을 기준으로 분리하여 타임스탬프와 데이터 부분을 분리
        parts = line.split()
        if len(parts) == 2:
            timestamp, hex_data = parts
            # 16진수 데이터를 바이트 배열로 변환
            try:
                data_bytes = bytes.fromhex(hex_data)
                # 바이트 배열을 UTF-8 문자열로 디코딩
                decoded_str = data_bytes.decode('utf-8')
                decoded_lines.append(f"{timestamp}    {decoded_str}")
                # "Hello World"가 포함된 경우 타임스탬프 저장
                if "Hello World" in decoded_str:
                    print (decoded_str)
                    hello_world_timestamps.append(float(timestamp))
            except:
                # 디코딩 실패한 경우 원본 데이터를 그대로 사용
                decoded_lines.append(line.strip())
        #else:
            # 데이터 부분이 없는 경우 타임스탬프만 추가
            #decoded_lines.append(parts[0])
    
    # "Hello World" 메시지가 포함된 패킷 사이의 지연시간 계산
    delays = []
    for i in range(1, len(hello_world_timestamps)):
        delay = hello_world_timestamps[i] - hello_world_timestamps[i-1]
        delays.append(delay)
    return delays

# make data for plotting
def make_data(files):
    delays = []
    for f in files:
        lines = read(f)
        delay = decoding(lines)
        delays.append(delay)
    return delays

def plot(delays):

    palette = sns.color_palette("hsv", len(delays))

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    for i, delay in enumerate(delays):
        plt.plot(delay, marker='o', linestyle='-', color=palette[i], label=f'Dataset {i+1}')
    
    # 범례
    plt.legend()

    plt.title('Delay Between Hello World Packets')
    plt.xlabel('Packet Number')
    plt.ylabel('Delay (secs)')
    plt.ylim([0.990, 1.010])
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    files = init()
    delays = make_data(files)
    plot(delays)
