from send_data import SendVehicleData
v = SendVehicleData('http://127.0.0.1:5000/user/')
data = {"name": "redrover", "opcode": 1, "state": None}
v.post(data)
print(v.r)
print(v.get_status())

