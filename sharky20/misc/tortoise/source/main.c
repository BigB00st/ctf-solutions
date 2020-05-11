#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/ipc.h>
#include "semaphores.h"

// The Hare and the Tortoise


#define handle_error(msg) \
    do { perror(msg); exit(EXIT_FAILURE); } while (0)


pid_t ppid;
int sem = -1;
char* sem_name;
char temp_dir[60] = {0};
char lock = 0;
char ppid_dir[30] = {0};

void cleanup(){
  if(sem != -1){
    SEM_DEL(sem);
  }
  rmdir(ppid_dir);
  rmdir(sem_name);
}

void sigint_handler(int signo){
  cleanup();
  exit(1);
}

void alarm_handler(int signo){
  cleanup();
  kill(ppid, SIGKILL);
  exit(1);
}


void random_string(){
  /* Only one execution should be allowed per term */
  sprintf(ppid_dir, "/tmp/%d", getppid());
  if(mkdir(ppid_dir, 0700) == -1){
    puts("There is no need for bruteforce");
    exit(1);
  }
  sprintf(temp_dir, "/tmp/%d/XXXXXX", getppid());
  sem_name = mkdtemp(temp_dir);
  if(sem_name == NULL){ perror("mkdtemp failed: "); exit(1); }
}

int main(int argc, char** argv){

  if(argc != 2){
    printf("Usage : %s <file to read>\n", argv[0]);
    exit(1);
  }
  atexit(cleanup);
  signal(SIGINT, sigint_handler);
  signal(SIGALRM, alarm_handler);
  random_string();
  sem = semget(ftok(sem_name, 1337 & 1), 1, IPC_CREAT | IPC_EXCL | 0600);

  if(sem == -1) handle_error("semget");

  SEM_SET(sem, 1);

  int hare = open (argv[1], O_RDONLY);
  int tortoise = open (argv[1], O_RDONLY);
  if(hare == -1 || tortoise == -1) handle_error("open");
  ppid = getpid();
  int pid;
  pid = fork();

  int cnt = 0;
  if(pid == 0) { // The hare
    puts("The hare says : \"Do you ever get anywhere?\"");
    char c;
    int y = 1;
    while(y == 1){
      SEM_WAIT(sem);
      y = read(hare, &c, sizeof(char));
      if(y == -1){ alarm(0.1);handle_error("read"); }
      usleep(100 * 750);
      SEM_POST(sem);
    }
    puts("The hare says : \"Hurry up tortoise !\"");
    alarm(5);
    sleep(10);

	} else { // The tortoise
    char c;
    int y = 1;
    while(y == 1){
      SEM_WAIT(sem);
      y = read(tortoise, &c, sizeof(char));
      printf("The tortoise, progressing slowly... : \"%c\"\n", c);
      if(y == -1){ handle_error("read"); }
      SEM_POST(sem);
      sleep(1);
    }
    puts("Slow but steady wins the race!");
  }
}
