#include <fcntl.h>
#include <sys/sendfile.h>

int main() {
    // read(0, RW_ADDR, 900); // write path of flag to known address
    int fd = openat(0, "/path/to/flag.txt", O_RDONLY); // imagine that RW_ADDR points to the string "/path/to/flag.txt"
    sendfile(1, fd, 0, 0xffff);
    return 0;
}
