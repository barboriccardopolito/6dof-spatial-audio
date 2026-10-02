import time
import math
from pythonosc import dispatcher, osc_server, udp_client
import numpy as np

PORTA_ZIGSIM = 8000
IP_REAPER = "172.20.10.14"
PORTA_REAPER = 9000

client = udp_client.SimpleUDPClient(IP_REAPER, PORTA_REAPER)

OFFSET_YAW_DEG = 0
OFFSET_PITCH_DEG = -89
OFFSET_ROLL_DEG = 0

INV_YAW = 1.0
INV_PITCH = 1.0
INV_ROLL = 1.0

SEND_INTERVAL = 0.04  # ~25 FPS
last_send_time = {"quaternion": 0.0}
ALPHA = 0.4
smoothed_data = {}

def apply_ema(sensor_key, current_values):
    if sensor_key not in smoothed_data:
        smoothed_data[sensor_key] = list(current_values)
        return current_values
    for i in range(len(current_values)):
        smoothed_data[sensor_key][i] = (ALPHA * current_values[i]) + ((1.0 - ALPHA) * smoothed_data[sensor_key][i])
    return smoothed_data[sensor_key]

def wrap_angle(angle):
    """Mantiene l'angolo strettamente tra -Pi e +Pi per evitare salti"""
    return (angle + math.pi) % (2 * math.pi) - math.pi

DAMPING = 0.92
MOVE_SPEED = 0.08
pos = np.array([0.0, 0.0, 0.0])
vel = np.array([0.0, 0.0, 0.0])

def gestisci_traslazione(address, *args):
    global pos, vel
    accel = np.array(args[:3])
    accel = np.where(np.abs(accel) < 0.2, 0, accel)
    
    vel = (vel + accel * MOVE_SPEED) * DAMPING
    pos += vel * 0.04
    
    pos = np.clip(pos, -3.0, 3.0) 
    
    client.send_message("/listener/x", pos[0])

def gestisci_sensori(address, *args):
    current_time = time.time()
    addr = address.lower()
    
    if "linearacceleration" in addr:
        gestisci_traslazione(address, *args)
        return

    try:
        if "quaternion" in addr:
            if (current_time - last_send_time["quaternion"]) >= SEND_INTERVAL:
                if len(args) >= 4:
                    q = apply_ema("quaternion", args[:4])
                    x, y, z, w = q[0], q[1], q[2], q[3]

                    t0 = +2.0 * (w * x + y * z)
                    t1 = +1.0 - 2.0 * (x * x + y * y)
                    raw_roll = math.atan2(t0, t1)

                    t2 = +2.0 * (w * y - z * x)
                    t2 = +1.0 if t2 > +1.0 else t2
                    t2 = -1.0 if t2 < -1.0 else t2
                    raw_pitch = math.asin(t2)

                    t3 = +2.0 * (w * z + x * y)
                    t4 = +1.0 - 2.0 * (y * y + z * z)
                    raw_yaw = math.atan2(t3, t4)

                    final_yaw = raw_yaw
                    final_pitch = raw_roll  
                    final_roll = raw_pitch  

                    final_yaw += math.radians(OFFSET_YAW_DEG)
                    final_pitch += math.radians(OFFSET_PITCH_DEG)
                    final_roll += math.radians(OFFSET_ROLL_DEG)

                    final_yaw = wrap_angle(final_yaw) * INV_YAW
                    final_pitch = wrap_angle(final_pitch) * INV_PITCH
                    final_roll = wrap_angle(final_roll) * INV_ROLL

                    norm_yaw = (final_yaw + math.pi) / (2 * math.pi)
                    norm_pitch = (final_pitch + math.pi) / (2 * math.pi)
                    norm_roll = (final_roll + math.pi) / (2 * math.pi)

                    client.send_message("/sparta/yaw", norm_yaw)
                    client.send_message("/sparta/pitch", norm_pitch)
                    client.send_message("/sparta/roll", norm_roll)

                last_send_time["quaternion"] = current_time

    except Exception as e:
        print(f"[ERROR] Pacchetto ignorato: {e}")

if __name__ == "__main__":
    disp = dispatcher.Dispatcher()
    disp.set_default_handler(gestisci_sensori)
    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", PORTA_ZIGSIM), disp)
    print("=====================================================")
    print("MIDDLEWARE 6DOF AVVIATO (Auto-Swap e Auto-Offset)")
    print("=====================================================")
    server.serve_forever()