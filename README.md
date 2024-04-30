ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_cpp listener
ros2 run demo_nodes_cpp listener listsener_best_effort

sudo tcpdump -i any -w tmp.pcap

tshark -r tmp.pcap -Y "rtps.sm.id == 0x15" -T fields -e frame.time_epoch -e rtps.issueData

python3 script.py normal.pcap DoS_pub_100.pcap DoS_pub_200.pcap
python3 script.py normal.pcap DoS_sub_100.pcap DoS_sub_200.pcap

pkill -f "ros2 topic pub"
pkill -f "ros2 topic echo"


QoS - Reliable

0개 손실 normal
2개 손실 10Hz * 100pub
11개 손실 10Hz * 200pub
5개 손실 100sub
6개 손실 200sub

QoS - Best_Effort

0개 손실 normal
6개 손실 10Hz * 100pub
20개 손실 10Hz * 200pub
6개 손실 100sub
7개 손실 200sub
