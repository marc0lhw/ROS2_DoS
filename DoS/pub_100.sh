#!/bin/bash

# Loop to run 'ros2 topic pub' 100 times with different names.
for i in {1..100}
do
  ros2 topic pub -n "talker_$i" -r 10 /chatter std_msgs/msg/String "data: 'DoS!_$i'" &
done


