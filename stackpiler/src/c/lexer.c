#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dismiss.h"

char* line_tokenize(char* line) {
    // goal: split line into readable tokens.
    UNIMPLEMENTED;
};
// filetype must validate to *.stk
int file_read(char* filename) {
    FILE *file;
    fopen_s(&file, filename, "r");

    if (file == NULL) {
        fprintf(stderr, "ERROR: file %s could not be opened.", filename);
        return 1;
    }

    char *paragraph[10] = {};
    char line[80] = ""; // TODO might want to find a better size for line.
    int line_count = 0;
    while ((fgets(line, 80, file)) != NULL) {
            //paragraph[line_count++] = line_tokenize(line);
            memset(line, 0, sizeof(line));
            strncpy(paragraph[line_count],line, sizeof(line));
    }


    if (ferror(file)) {
        fprintf(stderr, "ERROR: I/O error when reading %s.", filename);
        return 1;
    }

    fclose(file);
    return 0;
};


int main(int argc, char** argv) {
    int err = file_read(argv[1]);
    if (err != 0) {
        exit(1);
    }


    return 0;
}
