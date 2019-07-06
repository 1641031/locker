# -*- coding: UTF-8 -*-
#!/usr/bin/python
#import Raspi_MotorHAT, Raspi_DCMotor, Raspi_Stepper 
from steppermotor.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor, Raspi_StepperMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(0x6F)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)   # 200 steps/rev, motor port #1
myStepper.setSpeed(30)          # 30 RPM



class CreateLocker():
    def begin(self,num):
        print("Microsteps")
        if num > 0:
                ward = Raspi_MotorHAT.FORWARD
        elif num < 0:
                ward = Raspi_MotorHAT.BACKWARD
                num = num * -1
        myStepper.step(num, ward, Raspi_MotorHAT.MICROSTEP)
        
    def move(self,mylockernum,targetlockernum,spacedistance,maxlockernum):
        #参数讲解
        # 1.mylockernum    当前储物柜步进机编号
        # 2.targetlockernum 将要达到储物柜步进机编号
        # 3.spacedistance   储物柜之间的共同间距
        # 4.maxlockernum    储物柜总数量
        disparity = abs(targetlockernum - mylockernum)
        average_angel = 360/maxlockernum
        stepperwork = disparity * average_angel
        if stepperwork <= 180:
            print("ok")
            return stepperwork / average_angel * spacedistance
        elif stepperwork > 180 and stepperwork <= 360:
            print("yes")
            print(360 % stepperwork * -1 / average_angel * spacedistance)
            return 360 % stepperwork * -1 / average_angel * spacedistance


# while (True):
    # print("Single coil steps")
    # myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.SINGLE)
    # myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.SINGLE)

    # print("Double coil steps")
    # myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.DOUBLE)
    # myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.DOUBLE)

    # print("Interleaved coil steps")
    # myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.INTERLEAVE)
    # myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.INTERLEAVE)

    # print("Microsteps")
    # myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.MICROSTEP)
    # myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.MICROSTEP)
