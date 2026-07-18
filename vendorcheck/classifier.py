SHIMS = {
    "libbase_shim.so",
    "libgui_shim.so",
    "libcrypto_shim.so",
    "libcomparetf2_shim.so",
    "libinput_shim.so",
    "libcamera_metadata_shim.so",
    "libaudioclient_shim.so",
}

VENDORCOMPAT = {
    "libprotobuf-cpp-lite-3.9.1.so",
    "libprotobuf-cpp-full-3.9.1.so",
}

ROM_LIBS = {
    "libion.so",
    "libnl.so",
    "libwpa_client.so",
    "libstagefright_foundation.so",
    "libinput.so",
    "libmedia.so",
    "libaaudio.so",
    "libhwui.so",
    "libpiex.so",
    "libdng_sdk.so",
}


def classify(lib):

    if lib in SHIMS:
        return "shim"

    if lib in VENDORCOMPAT:
        return "vendorcompat"

    if lib in ROM_LIBS:
        return "rom"

    return "blob"
