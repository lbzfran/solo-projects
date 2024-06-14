#ifndef _DISMISS_H_
#define _DISMISS_H_


#define UNIMPLEMENTED \
    do { \
        fprintf(stderr, "%s:%d: %s not implemented yet\n", \
                __FILE__, __LINE__, __func__); \
        exit(1); \
    } while(0)
// basically my assert function
#include <stdbool.h>
extern bool dismiss_flag;
void devour();
void dismiss(bool condition, const char *msg);

#endif // _DISMISS_H_
