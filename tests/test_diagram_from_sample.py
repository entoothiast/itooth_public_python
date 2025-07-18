import numpy as np

from itooth_xiao.util_diagram import Data, diagram


def get_sample_data() -> Data:
    mono_s = np.array(range(0, 50, 5))
    I_SENSE_nA = np.linspace(-100, 1000, 10)
    I_SENSE_OVL = np.full(10, "", dtype=object)
    I_SENSE_OVL[7] = "ovl"

    I_LEAK_nA = np.linspace(-1, 10, 10)
    I_LEAK_OVL = np.full(10, "", dtype=object)
    I_LEAK_OVL[8] = "ovl"

    U_CE_WE_V = np.linspace(-1, 1, 10)
    U_CE_WE_OVL = np.full(10, "", dtype=object)
    U_CE_WE_OVL[5] = "ovl"

    temperature_C = np.linspace(23, 24, 10)

    U_CE_CONNECTOR_V = np.linspace(0.1, 0.09, 10)
    U_CE_CONNECTOR_V[2] = 0.4
    U_CE_CONNECTOR_connected = np.full(10, "", dtype=object)
    U_CE_CONNECTOR_connected[2] = "disconnected"
    U_CE_CONNECTOR_connected[3] = "disconnected"

    U_BATT_V = np.linspace(4.1, 2.3, 10)
    return Data(
        mono_s=mono_s.tolist(),
        I_SENSE_nA=I_SENSE_nA.tolist(),
        I_SENSE_OVL=I_SENSE_OVL.tolist(),
        I_LEAK_nA=I_LEAK_nA.tolist(),
        I_LEAK_OVL=I_LEAK_OVL.tolist(),
        U_CE_WE_V=U_CE_WE_V.tolist(),
        U_CE_WE_OVL=U_CE_WE_OVL.tolist(),
        temperature_C=temperature_C.tolist(),
        U_CE_CONNECTOR_V=U_CE_CONNECTOR_V.tolist(),
        U_CE_CONNECTOR_connected=U_CE_CONNECTOR_connected.tolist(),
        U_BATT_V=U_BATT_V.tolist(),
    )


def test_diagram():
    data = get_sample_data()
    diagram(data=data, show=True, filename=None)
    # main(data=data, show=False, filename=pathlib.Path(__file__).with_suffix(".png"))


if __name__ == "__main__":
    test_diagram()
