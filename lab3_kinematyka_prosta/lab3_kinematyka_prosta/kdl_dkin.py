from PyKDL import *

# Zarys/baza to pliku kdl_dkin.py
# Struktura drzewa podobna do urdf

# Dojdzie jeszcze czytanie z YAML

print("Creating Robotic Chain")

chain = Chain()
base_link__link_1 = Joint(Joint.TransZ) 
frame1 = Frame(Rotation.RPY(0,1,0),Vector(0.2,0.3,0))
segment1 = Segment(base_link__link_1,frame1)
chain.addSegment(segment1) 


link_1__link_2 = Joint(Joint.TransZ) 
frame2=Frame(Rotation.RPY(0,1,0),Vector(0.2,0.3,0))
segment2=Segment(link_1__link_2,frame2)
chain.addSegment(segment2)


link_2__link_3 = Joint(Joint.TransZ) 
frame3=Frame(Rotation.RPY(0,1,0),Vector(0.2,0.3,0))
segment3=Segment(link_2__link_3,frame3)
chain.addSegment(segment3)

# Tu jest bug, że nie akceptuje Joint.None
# https://github.com/ros/kdl_parser/issues/44
# link_3__tool = Joint(Joint.None) 
# frame4 = Frame(Rotation.RPY(0,1,0),Vector(0.2,0.3,0))
# segment4 = Segment(link_3__tool,frame4)
# chain.addSegment(segment4)

# Możemy to ominąć i dodać offset w postaci końcówki w osi z 
# do końcowego wyniku ( bo orientacja końcówki jest zgodna z orientacją
# ostatniego członu)



print("Forward kinematics")

joint_positions=JntArray(3)
joint_positions[0]=0.5236
joint_positions[1]=0.5236
joint_positions[2]=-1.5708
fk=ChainFkSolverPos_recursive(chain)
finalFrame=Frame()
fk.JntToCart(joint_positions,finalFrame)
print("Rotational Matrix of the final Frame: ")
print(finalFrame.M)
print("End-effector position: ",finalFrame.p)