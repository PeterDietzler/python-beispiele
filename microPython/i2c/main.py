from machine import I2C, Pin
from time import sleep_ms

#
# https://micronote.tech/2020/07/I2C-Bus-with-a-NodeMCU-and-MicroPython/
#

i2c = I2C(scl=Pin(5), sda=Pin(4))

# i2c.scan()
# i2c.writeto_mem(0x68, 0x6B, bytes([0]))
# temp_h = i2c.readfrom_mem(0x68, 0x41, 1)
# temp_l = i2c.readfrom_mem(0x68, 0x42, 1)

MPU6050_ADDR = 0x68
MPU6050_TEMP_OUT_H = 0x41
MPU6050_TEMP_OUT_L = 0x42
MPU6050_PWR_MGMT_1 = 0x6B

MPU6050_LSBC = 340.0
MPU6050_TEMP_OFFSET = 36.53


def mpu6050_init(i2c):
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, bytes([0]))


def combine_register_values(h, l):
    if not h[0] & 0x80:
        return h[0] << 8 | l[0]
    return -((h[0] ^ 255) << 8) |  (l[0] ^ 255) + 1


def mpu6050_get_temp(i2c):
    temp_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_H, 1)
    temp_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_L, 1)
    
    return (combine_register_values(temp_h, temp_l) / MPU6050_LSBC) + MPU6050_TEMP_OFFSET


def temp_data_to_celsius(temp_h, temp_l):
    temp_h = temp_h[0]
    temp_l = temp_l[0]

    temp_h = temp_h << 8
    
    temp_data = temp_h | temp_l
    
    if temp_data & 0b1000000000000000:
        temp_data = -((temp_data ^ 0b1111111111111111) + 1)
    
    temp_c = (temp_data / 340.0) + 36.53
    return temp_c


if __name__ == "__main__":
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    mpu6050_init(i2c)
    
    while True:
        print(mpu6050_get_temp(i2c))
        sleep_ms(500)
