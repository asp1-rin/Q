const OFFSETS = {
    // 라이브러리 명칭
    G_LIB: "libMyGame.so",
    S_LIB: "libxigncode.so",

    // 베이스 주소 (Base Addresses)
    ADDR_POSITION_BASE: 0x7ABE28,
    ADDR_CASH_BASE:     0x2D16FC,
    ADDR_CAMERA_BASE:   0x8B26DC,

    // 기능별 오프셋 (Function Offsets)
    OFFSET_GET_AIM_GAP:  0x25B5268,
    OFFSET_SHAKE_CAMERA: 0x28B6EB4,
    OFFSET_RECOIL_VALUE: 0x25B51D0,

    // 무기 패치 주소 (Weapon Patches)
    WEAPON_RECOIL_PATCH: 0x33BFAF0,
    WEAPON_SPREAD_PATCH: 0x35ADC9C,

    // 엔티티 오프셋 (Entity Offsets)
    OFF_HP:         0x2C,
    OFF_MAXHP:      0xEF4,
    OFF_NICKNAME:   0x88,
    OFF_STATE:      0x12C,
    OFF_X:          0x190,
    OFF_Y:          0x194,
    OFF_Z:          0x198,
    OFF_SKILL_COOL: 0xCC
};

// 다른 모듈에서 이 객체를 참조할 수 있도록 전역 선언 (Frida 환경용)
global.OFFSETS = OFFSETS;
