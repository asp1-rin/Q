var Weapon = {
    recoilOriginal: null,
    spreadOriginal: null,

    setNoRecoil: function(enable) {
        const addr = Module.findBaseAddress(OFFSETS.G_LIB).add(OFFSETS.WEAPON_RECOIL_PATCH);
        if (!addr) return;

        if (this.recoilOriginal === null) {
            this.recoilOriginal = addr.readByteArray(4);
        }

        Memory.patchCode(addr, 4, code => {
            const writer = new Arm64Writer(code);
            if (enable) {
                writer.putBytes(hexToBytes("0040201E"));
            } else {
                writer.putBytes(new Uint8Array(this.recoilOriginal));
            }
            writer.flush();
        });
    },

    setNoSpread: function(enable) {
        const addr = Module.findBaseAddress(OFFSETS.G_LIB).add(OFFSETS.WEAPON_SPREAD_PATCH);
        if (!addr) return;

        if (this.spreadOriginal === null) {
            this.spreadOriginal = addr.readByteArray(4);
        }

        Memory.patchCode(addr, 4, code => {
            const writer = new Arm64Writer(code);
            if (enable) {
                writer.putBytes(hexToBytes("0040201E"));
            } else {
                writer.putBytes(new Uint8Array(this.spreadOriginal));
            }
            writer.flush();
        });
    }
};

function hexToBytes(hex) {
    var bytes = [];
    for (var c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return new Uint8Array(bytes);
}

global.Weapon = Weapon;
