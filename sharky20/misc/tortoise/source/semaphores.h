#include <sys/sem.h>


union semun {
    int val;

    struct semid_ds * buf;

    unsigned short * array;

};


int SEM_SET(int sem_id, int sem_val) {
    union semun sem_union;

    sem_union.val = sem_val;

    return semctl(sem_id, 0, SETVAL, sem_union);
}

int SEM_DEL(int sem_id) {
    return semctl(sem_id, 0, IPC_RMID);
}

int SEM_WAIT(int sem_id) {
    struct sembuf sem_buf;

    sem_buf.sem_num = 0;
    sem_buf.sem_op = -1;
    sem_buf.sem_flg = SEM_UNDO;
    return semop(sem_id, &sem_buf, 1);
}

int SEM_POST(int sem_id) {
    struct sembuf sem_buf;

    sem_buf.sem_num = 0;
    sem_buf.sem_op = 1;
    sem_buf.sem_flg = SEM_UNDO;
    return semop(sem_id, &sem_buf, 1);
}
