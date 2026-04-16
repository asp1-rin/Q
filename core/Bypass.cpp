#include "Offset.h"
#include "KittyInclude.hpp"
#include <unistd.h>

void ApplyBypass() {
    ProcMap xignMap;
    while (!xignMap.isValid()) {
        xignMap = KittyMemory::getLibraryMap(S_LIB);
        usleep(500);
    }

    // Stage 1: Syscall Table & Instruction Hooking Protection
    uintptr_t stage1 = KittyScanner::findIdaPattern(xignMap, "FF 43 00 D1 F4 4F 01 A9");
    if (stage1) KittyMemory::write32(stage1, 0xD65F03C0);

    // Stage 2: Memory Integrity Check Routine Bypass
    uintptr_t stage2 = KittyScanner::findSymbol(xignMap, "ZCWAVE_Notify");
    if (stage2) KittyMemory::write32(stage2, 0xD65F03C0);

    // Stage 3: Heartbeat Signal Nullification
    uintptr_t stage3 = KittyScanner::findIdaPattern(xignMap, "FD 7B BF A9 FD 03 00 91");
    if (stage3) KittyMemory::write32(stage3, 0xD65F03C0);

    // Stage 4: Anti-Debug & Tracer Flag Suppression
    uintptr_t stage4 = KittyScanner::findIdaPattern(xignMap, "F3 0F 1E F8 48 89 E5");
    if (stage4) KittyMemory::write32(stage4, 0xD65F03C0);

    // Stage 5: File System & Path Sandbox Bypass
    uintptr_t stage5 = KittyScanner::findSymbol(xignMap, "ZCWAVE_CheckModule");
    if (stage5) KittyMemory::write32(stage5, 0xD65F03C0);

    // Stage 6: Final Handshake & Authentication Fake-Return
    uintptr_t stage6 = KittyScanner::findIdaPattern(xignMap, "08 00 80 D2 C0 03 5F D6");
    if (stage6) KittyMemory::write32(stage6, 0xD65F03C0);
}
