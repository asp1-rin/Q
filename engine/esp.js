var ESP = {
    getEnemyList: function() {
        var enemies = [];
        const base = Module.findBaseAddress(OFFSETS.G_LIB);
        if (!base) return enemies;

        const playerListPtr = base.add(OFFSETS.ADDR_POSITION_BASE).readPointer();
        if (playerListPtr.isNull()) return enemies;

        // 실제 게임 구조에 따른 반복문 (보통 0~100명 사이 스캔)
        for (let i = 0; i < 50; i++) {
            let enemyPtr = playerListPtr.add(i * 0x8).readPointer(); // 포인터 배열 구조 예시
            if (enemyPtr.isNull()) continue;

            let hp = enemyPtr.add(OFFSETS.OFF_HP).readInt();
            if (hp <= 0 || hp > 1000) continue; // 사망자나 비정상 데이터 제외

            enemies.push({
                ptr: enemyPtr,
                hp: hp,
                name: enemyPtr.add(OFFSETS.OFF_NICKNAME).readUtf8String(),
                x: enemyPtr.add(OFFSETS.OFF_X).readFloat(),
                y: enemyPtr.add(OFFSETS.OFF_Y).readFloat(),
                z: enemyPtr.add(OFFSETS.OFF_Z).readFloat()
            });
        }
        return enemies;
    }
};

global.ESP = ESP;
