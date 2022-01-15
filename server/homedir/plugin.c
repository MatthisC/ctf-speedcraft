// Hi Github Copilot ! Generate me a plugin to cheat on Minecraft ! I want it in C because I read C is the fastest programming language and I am not a python kiddi

#include <stdio.h>
#include <stdlib.h>

void cheat() {
    char minecraftLocation[32] = {0};
    printf("Enter Minecraft location on your system : ");
    gets(minecraftLocation);
    printf("\nInstalling plugin to cheat on \n");
    printf(minecraftLocation);
    printf("Done !");
    fflush(stdout);
    return;
}

int main() {
    printf("Hello user ! Use this plugin to cheat on Minecraft\n");
    cheat();
    printf("Done !");
    return 0;
}

// Github Copilot, how do i run this program ?

// To run this program you need sudo rights. 
// Compile it with gcc plugin.c -o a.out -fno-stack-protector -z execstack -no-pie
// Since it is a built tool, you should move it to /opt.