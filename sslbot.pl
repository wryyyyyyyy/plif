#!/usr/bin/env perl
# IRC SSL Bot

### default ###
use strict;
use warnings;
use IO::Socket::SSL;

### settings ###
my $server = "chat.freenode.net";
my $port = 6697;
my $channel = "#warbot";
my $nick = "sslbot_";
my $admin = "*!xbot\@*.telefonica.pool.de";

## init ##
my $sock = new IO::Socket::SSL(PeerAddr=>$server,PeerPort=>$port,Proto=>'tcp');

## check? ##
#if ($sock) {
#  print "\n+++ Connected!\r\n";
#} else {
#  print "\n+++ Unable to connect!\r\n";
#  exit 1;
#}

## connect ##
$sock->print("USER $nick $nick $nick $nick\n\r");
$sock->print("NICK $nick\n\r");

my $answer = undef;

while($answer = <$sock>) {
  print $answer;

  if($answer =~ m/^PING (.*?)$/gi) {
    $sock->print("PONG ".$1."\r\n");
  }

  if($answer =~ /^:(.+) 376/) { # :END OF MOTD
    $sock->print("JOIN $channel\n\r");

  ### can be used for join/part channel flood routine ###
    #$sock->print("PRIVMSG $channel $joinmessage\r\n");
    #$sock->print("PART $channel $partmessage\r\n");

  }

  if ($answer =~ /^:(.+)!(.+)\@(.+) PRIVMSG $channel :$nick,\s+?(.+)$/) {
    $sock->print("PRIVMSG $channel $1\r\n");
  }

  ## some useless shit ##
  #~ if($answer =~ /PRIVMSG/) { #START PRIVMSG
      #~ if($answer =~ /!id/i) {
        #~ my $id = `id`;chop $id;
        #~ print $sock "PRIVMSG $channel $id\r\n";
      #~ }

      #~ if($answer =~ /!uptime/i) {
        #~ my $uptime = `uptime`;
        #~ print $sock "PRIVMSG $channel $uptime\r\n";
      #~ }

      #~ if($answer =~ /!top/i) {
        #~ my $top = `top -b -n 1|head -n 4`;chop $top;
        #~ print $sock "PRIVMSG $channel $top\r\n";
      #~ }

  #~ } #END PRIVMSG

}
## end of main loop ##

#close $sock;
#print "\n++ DDisconnecting...\n\r";
