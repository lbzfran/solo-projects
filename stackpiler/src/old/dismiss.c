#include <stdio.h>
#include <stdlib.h>
#include "dismiss.h"

bool dismiss_flag = false;

void devour() {
    // sets dismiss_flag to true.
    // on next dismiss call, dismiss will not exit if condition fails.
    // defaults to false.
    if (!dismiss_flag) {
        dismiss_flag = true;
    }
};

void dismiss(bool condition, const char* message) {
    if (!condition) {
        fprintf(stderr, "%s\n", message);
        if (dismiss_flag) {
            dismiss_flag = false;
        } else {
            exit(1);
        };
    };
};
