import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

direct = 23
step_pin = 22
not_sleep = 17
not_reset = 27
not_enable = 10

GPIO.setup(direct, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(not_reset, GPIO.OUT)
GPIO.setup(not_sleep, GPIO.OUT)
GPIO.setup(not_enable, GPIO.OUT)

mode0 = 14
mode1 = 15
mode2 = 18
GPIO.setup(mode0, GPIO.OUT)
GPIO.setup(mode1, GPIO.OUT)
GPIO.setup(mode2, GPIO.OUT)

mode = [[0,0,0,1],
        [1,0,0,2],
        [0,1,0,4],
        [1,1,0,8],
        [0,0,1,16],
        [1,0,1,32],
        [0,1,1,32],
        [1,1,1,32]]

Rot_Spd = 0.0
Rot_steps = 0
Rotate_Dir = 1
mot_deg = 0.0

def moveRezistenta(modein, deg, rot, dir, spd):
	global mode_in, mot_deg, RotateF, Rotate_Dir, Rot_Spd, direct, step_pin, not_sleep, not_reset, not_enable, mode0, mode1, mode2, mode

#	mode_in = int(input('ENTER: mode [0,1,2,3,4,5,6,7](default = 0): '))
#	mot_deg = float(input("ENTER: motor's degrees/step (default = 7.5): "))
#	RotateF = float(input('ENTER: Rotations (0.00041+, default = 1): '))
#	Rotate_Dir = int(input('ENTER: Direction (1=CW/0=CCW, default = 1): '))
#	Rot_Spd = int(input('ENTER: Rotation Speed (1-100, default = 50): '))
	mode_in = modein
	mot_deg = deg
	RotateF = rot
	Rotate_Dir = dir
	Rot_Spd = spd

#	if mode_in not in [0,1,2,3,4,5,6,7]: mode_in = 0
#	if mot_deg < 0.1: mot_deg = 7.5
#	if RotateF < .00041: RotateF = 1
	Rot_steps = int(RotateF * (360.0/float(mot_deg)))
	Rot_steps = int(Rot_steps * (mode[mode_in][3]))
#	if Rot_steps < 1: Rot_steps = 1
	Rotate_Dir = int(Rotate_Dir)
#	if Rotate_Dir not in [0,1]: Rotate_Dir = 1
#	if Rot_Spd not in range(1,101): Rot_Spd = 50
	Rot_Spd = 1/float((Rot_Spd * mode[mode_in][3]))
	print(mode_in, mot_deg, RotateF, Rot_steps, Rotate_Dir, Rot_Spd)

	GPIO.output(direct, Rotate_Dir)
	GPIO.output(not_sleep, True)
	GPIO.output(not_reset, True)
	GPIO.output(not_enable, False)
	GPIO.output(mode0, mode[mode_in][0])
	GPIO.output(mode1, mode[mode_in][1])
	GPIO.output(mode2, mode[mode_in][2])

	for x in range(0, (Rot_steps + 1)):
		GPIO.output(step_pin, True)
		time.sleep(Rot_Spd)
		GPIO.output(step_pin, False)

	GPIO.output(not_reset, False)

#moveRezistenta(5, 1.8, 1.5, 0, 100)