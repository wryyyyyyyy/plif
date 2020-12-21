#!/bin/perl
###########

use strict;

my @iface = (`ip address show` =~ /(.*?)\:\s*(.*?)\:\s*\<BROADCAST(.*?)/g);
print "INTERFACE:\t".$2."\n"; # valid iface

my @ip = (`ip route show` =~ /(\S+)/g);
print "IP ADDRESS:\t".$1."\n";

my @mac = (`ip link show` =~ /link\/ether\s*(\S+)/g);
print "MAC ADDRESS:\t".$1."\n";
