#include <sys/types.h>
#include <dirent.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/sendfile.h>
#include <unistd.h>

#define RW_ADDR 0xdeadbeef // actually some bss address in exploit

int main() {
    read(0, RW_ADDR, 900); // write path of flag to address
    int fd = openat(0, "/path/to/flag.txt", O_RDONLY);
    sendfile(1, fd, 0, 0xffff);
    return 0;
}
