#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

void generate_secret(char *buffer, size_t len) {
    time_t now = time(NULL);
    time_t seed = (now / 60) ^ 0xBADC0DE;
    srand(seed);

    for (size_t i = 0; i < len - 1; i++) {
        buffer[i] = 'A' + (rand() % 26);
    }
    buffer[len - 1] = '\0';
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <secret>\n", argv[0]);
        return 1;
    }

    char expected[16]; // 15 chars + null
    generate_secret(expected, sizeof(expected));
    printf("[DEBUG] Expected secret: %s\n", expected);

    if (strcmp(argv[1], expected) == 0) {
        FILE *f = fopen("flag.txt", "r");
        if (!f) {
            perror("Could not open flag file");
            return 1;
        }
        char flag[128];
        fgets(flag, sizeof(flag), f);
        fclose(f);

        printf("Correct secret! Here's your flag: %s\n", flag);
    } else {
        printf("Wrong secret.\n");
    }

    return 0;
}

