function apply6StageBypass() {
    const sLib = OFFSETS.S_LIB;
    let xignBase = Module.findBaseAddress(sLib);

    while (!xignBase) {
        xignBase = Module.findBaseAddress(sLib);
        Thread.sleep(0.1);
    }

    const stages = [
        { id: 1, pattern: "FF 43 00 D1 F4 4F 01 A9" },
        { id: 2, symbol: "ZCWAVE_Notify" },
        { id: 3, pattern: "FD 7B BF A9 FD 03 00 91" },
        { id: 4, pattern: "F3 0F 1E F8 48 89 E5" },
        { id: 5, symbol: "ZCWAVE_CheckModule" },
        { id: 6, pattern: "08 00 80 D2 C0 03 5F D6" }
    ];

    stages.forEach(stage => {
        let targetAddr = null;

        if (stage.symbol) {
            targetAddr = Module.findExportByName(sLib, stage.symbol);
        } else if (stage.pattern) {
            const results = Memory.scanSync(xignBase, 0x200000, stage.pattern);
            if (results.length > 0) {
                targetAddr = results[0].address;
            }
        }

        if (targetAddr) {
            Memory.patchCode(targetAddr, 4, code => {
                const writer = new Arm64Writer(code);
                writer.putRet();
                writer.flush();
            });
        }
    });
}

// 자동 실행
apply6StageBypass();
