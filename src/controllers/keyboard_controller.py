import pygame
import numpy as np

class KeyboardController:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((200, 100))
        pygame.display.set_caption("BlueROV Keyboard Controller")

        self.cmd = np.zeros(8, dtype=float)
        self.speed = 12.0          # general speed (surge/lateral/up/down)
        self.yaw_speed = 0.8       # yaw rotation speed (Q/E)
        self.pitch_speed = 0.8     # pitch rotation speed (R/F)
        self.max_thrust = 12.0     # maximum thrust per motor

    def get_command(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        cmd = np.zeros(8, dtype=float)

        # --- Heave control (↑ / ↓) - vertical motion using thrusters 0..3 ---
        if keys[pygame.K_UP]:
            cmd[0:4] += self.speed      # ascend
        if keys[pygame.K_DOWN]:
            cmd[0:4] -= self.speed      # descend

        # --- Surge control (W / S) - forward/backward motion using thrusters 4..7 ---
        if keys[pygame.K_w]:
            cmd[4:8] += self.speed * 1.4    # move forward
        if keys[pygame.K_s]:
            cmd[4:8] -= self.speed * 1.4    # move backward

        # --- Strafe control (A / D) - lateral translation using thrusters 4..7 ---
        if keys[pygame.K_a]:
            cmd[4] += self.speed
            cmd[5] -= self.speed
            cmd[6] += self.speed
            cmd[7] -= self.speed          # move left
        if keys[pygame.K_d]:
            cmd[4] -= self.speed
            cmd[5] += self.speed
            cmd[6] -= self.speed
            cmd[7] += self.speed          # move right

        # --- Yaw control (Q / E) - horizontal rotation using thrusters 4..7 ---
        if keys[pygame.K_q]:
            cmd[4] -= self.yaw_speed
            cmd[5] += self.yaw_speed
            cmd[6] += self.yaw_speed
            cmd[7] -= self.yaw_speed      # rotate left (yaw)
        if keys[pygame.K_e]:
            cmd[4] += self.yaw_speed
            cmd[5] -= self.yaw_speed
            cmd[6] -= self.yaw_speed
            cmd[7] += self.yaw_speed      # rotate right (yaw)

        # --- Pitch control (R / F) - vertical rotation using thrusters 0..3 ---
        if keys[pygame.K_f]:
            cmd[0:2] += self.pitch_speed   # pitch down (nose down)
            cmd[2:4] -= self.pitch_speed
        if keys[pygame.K_r]:
            cmd[0:2] -= self.pitch_speed   # pitch up (nose up)
            cmd[2:4] += self.pitch_speed

        # --- Clamp values within allowed thrust range ---
        np.clip(cmd, -self.max_thrust, +self.max_thrust, out=cmd)

        # --- Handle window close event ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        self.cmd = cmd
        return self.cmd
