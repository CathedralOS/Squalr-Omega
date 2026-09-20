/* TARGETS-AND-THROUGHPUT controlled child process for the squalr-tests
 * native-read probe. It:
 *   1. mmap()s two private anonymous pages (4096 each, contiguous),
 *   2. fills page0 with "SQUALR42" + a deterministic index pattern
 *      (page[i] = 83 + (i & 63) past the magic, so offset 4080 holds 131 and
 *      offset 4095 holds 146),
 *   3. mprotect()s page1 PROT_NONE so reads there fail with EIO,
 *   4. prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY) so the probe may read
 *      /proc/<pid>/mem under Yama LSM,
 *   5. prints "READY <pid> <page_hex> <guard_hex>" on stdout and parks on
 *      stdin until the driver closes it.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <unistd.h>

#ifndef PR_SET_PTRACER
#define PR_SET_PTRACER 0x59616d61
#endif
#ifndef PR_SET_PTRACER_ANY
#define PR_SET_PTRACER_ANY ((unsigned long)-1)
#endif

int main(void) {
    const size_t page = 4096;
    unsigned char *base = mmap(NULL, 2 * page, PROT_READ | PROT_WRITE,
                               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (base == MAP_FAILED) {
        perror("mmap");
        return 2;
    }
    for (size_t i = 0; i < page; i++) {
        base[i] = (unsigned char)(83 + (i & 63));
    }
    memcpy(base, "SQUALR42", 8);
    unsigned char *guard = base + page;
    if (mprotect(guard, page, PROT_NONE) != 0) {
        perror("mprotect");
        return 3;
    }
    if (prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY, 0, 0, 0) != 0) {
        /* Not fatal on kernels without Yama; the probe's open fails plainly. */
        perror("prctl PR_SET_PTRACER");
    }
    printf("READY %ld %lx %lx\n", (long)getpid(),
           (unsigned long)(uintptr_t)base, (unsigned long)(uintptr_t)guard);
    fflush(stdout);
    /* Park: exit when the driver closes our stdin pipe. */
    int byte;
    while (read(STDIN_FILENO, &byte, 1) > 0) {
    }
    return 0;
}
