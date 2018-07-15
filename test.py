mass = float(input("Enter the object's mass: "))
velocity = float(input("Enter the object's velocity: "))

momentum = mass * velocity
KE = float(1/2 * mass * (velocity ** 2))

print("The object's momentum is", momentum)
print("The object's kinetic energy is", KE)

