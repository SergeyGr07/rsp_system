import json
import matplotlib.pyplot as plt
import time
import os


def create_plots():
    print("Starting visualization service...")
    print(f"Contents of /shared directory: {os.listdir('/shared')}")

    # Ждем появления файла с результатами
    while True:
        try:
            print("Trying to open results.json...")
            with open('/shared/results.json', 'r') as f:
                results = json.load(f)
            print("Successfully loaded results.json")
            break
        except FileNotFoundError:
            print("results.json not found, waiting...")
            time.sleep(1)

    print("Creating plots...")
    test_numbers = [r['test_number'] for r in results]
    speeds = [r['speed_mbps'] for r in results]
    durations = [r['duration'] for r in results]

    # График скорости передачи
    plt.figure(figsize=(10, 5))
    plt.plot(test_numbers, speeds, 'b-o')
    plt.title('gRPC Transfer Speed')
    plt.xlabel('Test Number')
    plt.ylabel('Speed (Mbps)')
    plt.grid(True)
    plt.savefig('/shared/speed_plot.png')
    print("Saved speed_plot.png")
    plt.close()

    # График времени передачи
    plt.figure(figsize=(10, 5))
    plt.plot(test_numbers, durations, 'r-o')
    plt.title('gRPC Transfer Duration')
    plt.xlabel('Test Number')
    plt.ylabel('Duration (seconds)')
    plt.grid(True)
    plt.savefig('/shared/duration_plot.png')
    print("Saved duration_plot.png")
    plt.close()


if __name__ == '__main__':
    print("Waiting for client to complete...")
    time.sleep(10)  # Ждем завершения тестов
    create_plots()
