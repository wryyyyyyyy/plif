/*******************************************/
/* amp3 - Programmed by Martin Kluge, 2001 */
/*******************************************/
/* This code is under the GPL as provided  */
/* by the Free Software Foundation (FSF).  */
/* Have a look at the file COPYING for     */
/* more information.                       */
/*******************************************/

/* TODO: Implement the communication protocol */
/* TODO: Command line parsing */
/* TODO: Find the different MP3 player */
/* TODO: Write a configure script using autoconf/automake */
/* TODO: Signal handler */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <signal.h>

/* amp3 version */
#define VERSION "0.01"

/* Timeout in seconds */
#define __TIMEOUT 5

/* Serial device */
#define DEVICE "/dev/ttyS0"

void show_banner (void) {
	printf("\nAMP3 v%s - Programmed by Martin Kluge\n", VERSION);
	printf("---------------------------------------\n");
	printf("Warning: This code is not really usefull at the moment -\n");
	printf("         in fact it does only look for your MP3 player.\n\n");
	printf("Looking for a Grundig MP3 Player...");
	
	/* Flush stdout */
	fflush(stdout);
}

void time_out (int sig) {
	printf("failed.\n");
	fprintf(stderr, "\nError: Cannot find an MP3 player!\n\n");
	exit(EXIT_FAILURE);
}

int main (int argc, char **argv) {
	int fd;
	struct termios new_tio, old_tio;

	char *mp3_data;

	/* Install some signal handlers */
	signal(SIGALRM, time_out);
	
	/* Show banner :) */
	show_banner();
	
	mp3_data=malloc(1024);

	if((fd=open(DEVICE, O_RDWR|O_NONBLOCK|O_NOCTTY))<0) {
	  printf("Cannot open device %s!\n", DEVICE);
	  exit(EXIT_FAILURE);
	}

	if(tcgetattr(fd, &old_tio)<0) {
	  printf("Cannot get serial parameters for %s!\n", DEVICE);
	  exit(EXIT_FAILURE);
	}

	memcpy((char *)&new_tio,(char *)&old_tio, sizeof(struct termios));
	cfmakeraw(&new_tio);
	cfsetispeed(&new_tio, B115200);
	cfsetospeed(&new_tio, B115200);
	
	tcflush(fd, TCIOFLUSH);
	tcflush(fd, TCIFLUSH);

	/* Set alarm timer to __TIMEOUT secs */
	alarm(__TIMEOUT);

	write(fd, "2", 1);
	fcntl(fd, F_SETFL, O_RDONLY|O_NONBLOCK);
	usleep(1);
	
	/* Looking for MP3 Player */
        while(strcmp("H", mp3_data)) {
	  read(fd, mp3_data, 5);
	}

	alarm(0);
	printf("found!\n");
	
	tcflush(fd, TCIFLUSH);
	write(fd, "o", 1);

	while(strcmp("q", mp3_data)) {
	  read(fd, mp3_data, 5);
	}

	write(fd, "r\0\0\0\0mm", 8);
	fcntl(fd, F_SETFL, O_RDONLY|O_NONBLOCK);

	while(1) {
	  read(fd, mp3_data, 1024);
	  printf("%s\n", mp3_data);
	}

	printf("Test: %s\n", mp3_data);

	free(mp3_data);
	close(fd);

	return(0);
}

