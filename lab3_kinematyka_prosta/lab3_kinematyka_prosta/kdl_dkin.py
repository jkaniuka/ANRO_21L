from PyKDL import *
import mathutils

position = [ -0.3445, -0.3943, 1.75]




print("Creating Robotic Chain")

chain = Chain()
base_link__link_1 = Joint(Joint.TransZ) 
frame1 = Frame(Rotation.RPY(0,0,0),Vector(0,0,1))
segment1 = Segment(base_link__link_1,frame1)
chain.addSegment(segment1) 


link_1__link_2 = Joint(Joint.TransY) 
frame2=Frame(Rotation.RPY(0.785398006439209 ,-1.5696700811386108  , 0.785398006439209),Vector(0.0,  -2.9999990463256836 , 0.002389180473983288  ))
segment2=Segment(link_1__link_2,frame2)
chain.addSegment(segment2)


link_2__link_3 = Joint(Joint.TransY) 
frame3=Frame(Rotation.RPY(0.785398006439209 ,-1.5696700811386108,   0.785398006439209),Vector( 0.0,    -1.9999994039535522  , 0.0015927869826555252   ))
segment3=Segment(link_2__link_3,frame3)
chain.addSegment(segment3)



print("Forward kinematics")

joint_positions=JntArray(3)
joint_positions[0]= position[0]
joint_positions[1]= -position[1]
joint_positions[2]= -position[2]


fk=ChainFkSolverPos_recursive(chain)
finalFrame=Frame()
fk.JntToCart(joint_positions,finalFrame)
print("Rotational Matrix of the final Frame: ")
print(finalFrame.M)  
print("End-effector position: ",finalFrame.p )