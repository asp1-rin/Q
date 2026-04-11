Java.perform(function () {
    const moduleName = "libxigncode.so";
    
    // 1. 모듈 로드 상태
    let module = Process.findModuleByName(moduleName);
    if (!module) {
        console.log("[Status] Waiting for " + moduleName + "...");
    }

    // 2. dlopen 후킹을 통해 모듈 로드 시점
    const dlopenPtr = Module.findExportByName(null, "android_dlopen_ext") || 
                     Module.findExportByName(null, "dlopen");

    Interceptor.attach(dlopenPtr, {
        onLeave: function (retval) {
            if (module) return; // 이미 로드되어있으면 실행 안함
            
            const target = Process.findModuleByName(moduleName);
            if (target) {
                module = target;
                console.log("[Info] " + moduleName + " Loaded at: " + module.base);
                setupHooks(module.base);
            }
        }
    });

    // 3. 핵심 함수 후킹
    function setupHooks(base) {
        // ZCWAVE_InitializeEx (Offset: 0x182ec)
        const initExAddr = base.add(0x182ec);
        Interceptor.attach(initExAddr, {
            onEnter: function (args) {
                console.log("--- ZCWAVE_InitializeEx Called ---");
                try {
                    // 서버 주소, 경로, 라이선스 확인
                    console.log("Arg[2] String: " + Memory.readUtf8String(args[2]));
                    console.log("Arg[3] String: " + Memory.readUtf8String(args[3]));
                } catch (e) {
                    console.log("Arg Error: Data may be binary or encrypted.");
                }
            }
        });

        // ZCWAVE_Initialize (Offset: 0x186c8) (비정확)
        const initAddr = base.add(0x186c8);
        Interceptor.attach(initAddr, {
            onEnter: function (args) {
                console.log("--- ZCWAVE_Initialize Called ---");
            }
        });
    }
});
