#include <stdio.h>
#include <stdlib.h>

#define STACK_SIZE 1024
#define CMD_BUF 512

// a stack based 32-bit virtual machine

enum OP {
    PUSH = 0x0,
    ADD = 0x1,
    MUL = 0x2
};

struct op_code {
    enum OP op;
    int value;
};

int main(void){
    FILE *fp;

    fp = fopen("bytecode", "rb");
    if(fp == NULL){
        perror("Could not open bytecode file");
        return 1;
    }

    int stack[STACK_SIZE];
    int stack_ptr = -1;

    struct op_code cmd_buf[CMD_BUF];
    size_t read = 0;

    while(read = fread(&cmd_buf, sizeof(struct op_code), CMD_BUF, fp)){
        for(int i = 0; i < read; i++){
            switch(cmd_buf[i].op){
                case PUSH:
                    stack_ptr++;
                    stack[stack_ptr] = cmd_buf[i].value;
                    break;
                case ADD:
                    stack_ptr--;
                    stack[stack_ptr] = stack[stack_ptr] + stack[stack_ptr+1];
                    break;
                case MUL:
                    stack_ptr--;
                    stack[stack_ptr] = stack[stack_ptr] * stack[stack_ptr+1];
                    break;
            }
        }
    }
    printf("%d\n", stack[stack_ptr]);

    fclose(fp);
    return 0;
}
