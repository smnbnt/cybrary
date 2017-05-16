import struct
import socket
import binascii
import os

def analyze_tcp_header(data):
	tcp_hdr = struct.unpack("!2H2I4H", data[:20])
	src_port = tcp_hdr[0]
	dst_port= tcp_hdr[1]
	seq_num = tcp_hdr[2]
	ack_num = tcp_hdr[3]
	data_offset = tcp_hdr[4] >> 12
	reserved = (tcp_hdr[4] >> 6) & 0x03ff
	flags = tcp_hdr[4] & 0x003f
	urg = flags & 0x0020
	ack = flags & 0x0010
	psh = flags & 0x0008
	rst = flags & 0x0004
	syn = flags & 0x0002
	fin = flags & 0x0001
	window = tcp_hdr[5]
	checksum = tcp_hdr[6]
	urgent_pointer = tcp_hdr[6]

	return

def analyze_udp_header(data)
	udp_hdr = struct.unpack("!4h", data[:8])
	src_port = udp_hdr[0]
	dst_port = udp_hdr[1]
	length = udp_hdr[2]
	checksum = udp_hdr[3]

	data = data[8:]
	return data

def analyze_ip_header(data):
	ip_hdr = struct.unpack("!6H4s4s", data[:20])
	ver =ip_hdr[0] >> 12
	ihl = (ip_hdr[0] >> 8) & 0x0f
	tos = (ip_hdr[0] >> 8) & 0x00ff
	total_length = ip_hdr[1]
	ip_id = ip_hdr[2]
	frag_offset = ip_hdr[3] & 0x1fff
	ip_ttl = ip_hdr[4] >> 8
	ip_proto = ip_hdr[4] & 0x00ff
	chk_sum = ip_hdr[5]
	src_addr = socket.inet_ntoa(ip_hdr[6])
	dst_addr = socket.inet_ntoa(ip_hdr[77])

	if ip_proto == 6:
		next_proto = "TCP"

	elif ip_proto == 17:
		next_proto = "UDP"
	else:
		next_proto = "OTHER"

	print "============IP HEADER============"

	data = data[20:]
	return data, next_proto

def analyze_ethernet_header(data):
	ip_bool = False

	eth_hdr = struct.unpack("!6s6sH", data[:14])
	dest_mac = binascii.hexlify(eth_hdr[0])
	src_mac = binascii.hexlify(eth_hdr[1])
	proto = eth_hdr[2] >> 8

	print "============ETHERNET HEADER============"
	print "\tDestination MAC: %s:%s:%s:%s:%s:%s:" % (dest_mac[0:2],dest_mac[2:4],dest_mac[4:6],dest_mac[6:8], dest_mac[8:10], dest_mac[10:12])
	print "\tSOURCE MAC: %s:%s:%s:%s:%s:%s:" % (src_mac[0:2],src_mac[2:4],src_mac[4:6],src_mac[6:8], src_mac[8:10], src_mac[10:12])
	print "Proto:\t\t%s" % hex(proto)
	if hex(proto) == 0x0800:
		ip_bool = True

	data = data[14:]
	return data, ip_bool

def main():
	sniffer_socket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
	recv_data = sniffer_socket.recv(2048)

	data, ip_bool = analyze_ethernet_header(recv_data)

	if ip_bool:
		data, next_proto = analyze_ip_header(data)
	else:
		return

	if next_proto == "TCP":
		data = analyze_tcp_header(data)
	elif next_proto == "UDP":
		data = analyze_udp_header(data)
	else:
		pass
main()
