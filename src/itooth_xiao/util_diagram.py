import dataclasses
import datetime
import pathlib

import matplotlib.dates as mdates
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


@dataclasses.dataclass(slots=True)
class Data:
    mono_s: list[float]
    I_SENSE_nA: list[float]
    I_SENSE_OVL: list[str]
    I_LEAK_nA: list[float]
    I_LEAK_OVL: list[str]
    U_CE_WE_V: list[float]
    U_CE_WE_OVL: list[str]
    temperature_C: list[float]
    U_CE_CONNECTOR_V: list[float]
    U_CE_CONNECTOR_connected: list[str]
    U_BATT_V: list[float]
    U_BATT_LOW: list[str]


NAMES_FLOAT = (
    "mono_s",
    "I_SENSE_nA",
    "I_LEAK_nA",
    "U_CE_WE_V",
    "temperature_C",
    "U_CE_CONNECTOR_V",
    "U_BATT_V",
)
NAMES_STR = (
    "I_SENSE_OVL",
    "I_LEAK_OVL",
    "U_CE_WE_OVL",
    "U_CE_CONNECTOR_connected",
    "U_BATT_LOW",
)


def diagram(
    data: Data, time_s: float, show: bool, filename: pathlib.Path | None, dpi=600
) -> None:
    # Plot
    fig, axs = plt.subplots(
        3,
        1,
        figsize=(10, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [5, 1, 1]},  # Verhältnis zueinander
    )

    ax_current = 0
    ax_voltage = ax_current + 1
    ax_temperature = ax_voltage + 1

    highlight_kwargs = {"color": "red", "linewidth": 2.0}

    list_time_s = [t + time_s for t in data.mono_s]
    error_marker = mlines.Line2D(
        [],
        [],
        color="red",
        marker="o",
        linestyle="None",
        markersize=4,
        label="overload or error",
    )

    # 1. Plot: Currents
    # electrochemistry engineers like it inverted
    I_SENSE_nA_inverted = [-x for x in data.I_SENSE_nA]

    axs[ax_current].plot(
        list_time_s,
        I_SENSE_nA_inverted,
        # label="-I_SENSE_nA",  # electrochemistry engineers like it this way, therefore -
        color="green",
        linewidth=2,
    )
    for i in range(len(list_time_s)):
        if data.I_SENSE_OVL[i] != "":
            axs[ax_current].plot(
                list_time_s[i],
                I_SENSE_nA_inverted[i],
                marker="o",
                markersize=4,
                **highlight_kwargs,
            )
    axs[ax_current].plot(
        list_time_s,
        data.I_LEAK_nA,
        label="I_LEAK_nA",
        linestyle="--",
        color="orange",
    )
    for i in range(len(list_time_s)):
        if data.I_LEAK_OVL[i] != "":
            axs[ax_current].plot(
                list_time_s[i],
                data.I_LEAK_nA[i],
                marker="o",
                markersize=4,
                **highlight_kwargs,
            )

    axs[ax_current].set_ylabel("Current [nA]")

    ymin_soft, ymax_soft = -100, 1000
    ymin = min(ymin_soft, min(I_SENSE_nA_inverted))
    ymax = max(ymax_soft, max(I_SENSE_nA_inverted))
    axs[ax_current].set_ylim(ymin, ymax)

    # axs[ax_current].set_ylim(-100, 1000)
    # axs[ax_current].legend()
    handles_current = [
        mlines.Line2D(
            [], [], color="green", label="- I_SENSE_nA"
        ),  # electrochemistry engineers like it this way, therefore -
        mlines.Line2D([], [], color="orange", linestyle="--", label="I_LEAK_nA"),
        error_marker,
    ]
    # axs[ax_current].legend(handles=handles_current)
    axs[ax_current].legend(
        handles=handles_current,
        loc="upper center",
        bbox_to_anchor=(0.5, 0),
        ncol=len(handles_current),
        frameon=False,
        bbox_transform=axs[ax_current].transAxes,
    )
    axs[ax_current].grid(True)

    # 2. Plot: Voltages
    axs[ax_voltage].plot(
        list_time_s, data.U_CE_WE_V, label="U_CE_WE_V", color="green", linewidth=2
    )
    for i in range(len(list_time_s)):
        if data.U_CE_WE_OVL[i] != "":
            axs[ax_voltage].plot(
                list_time_s[i],
                data.U_CE_WE_V[i],
                marker="o",
                markersize=4,
                **highlight_kwargs,
            )
    # axs[ax_voltage].plot(
    #     list_time_s,
    #     data.U_CE_CONNECTOR_V,
    #     label="U_CE_CONNECTOR_V",
    #     linestyle="--",
    #     color="orange",
    # )
    # for i in range(len(list_time_s)):
    #     if data.U_CE_CONNECTOR_connected[i] != "":
    #         axs[ax_voltage].plot(
    #             list_time_s[i],
    #             data.U_CE_CONNECTOR_V[i],
    #             marker="o",
    #             markersize=4,
    #             **highlight_kwargs,
    #        )

    axs[ax_voltage].plot(
        list_time_s,
        data.U_BATT_V,
        label="U_BATT_V",
        linestyle=":",
        color="orange",
    )
    for i in range(len(list_time_s)):
        if data.U_BATT_LOW[i] != "":
            axs[ax_voltage].plot(
                list_time_s[i],
                data.U_BATT_V[i],
                marker="o",
                markersize=4,
                **highlight_kwargs,
            )
    axs[ax_voltage].set_ylabel("Voltage [V]")
    # axs[ax_voltage].set_ylim(-2, 5)
    axs[ax_voltage].set_yticks(np.arange(-2, 5, 1.0))
    handles_voltage = [
        mlines.Line2D([], [], color="green", label="U_CE_WE_V"),
        # mlines.Line2D([], [], color="orange", linestyle="--", label="U_CE_CONNECTOR_V"),
        mlines.Line2D([], [], color="orange", linestyle=":", label="U_BATT_V"),
        error_marker,
    ]
    axs[ax_voltage].legend(
        handles=handles_voltage,
        loc="upper center",
        bbox_to_anchor=(0.5, 0),
        ncol=len(handles_voltage),
        frameon=False,
        bbox_transform=axs[ax_voltage].transAxes,
    )
    axs[ax_voltage].grid(True)

    # 2. Plot: Temperatur
    axs[ax_temperature].plot(
        list_time_s, data.temperature_C, linestyle="--", color="orange"
    )
    axs[ax_temperature].set_ylabel("Temperature [C]")
    # axs[ax_temperature].set_ylim(10, 40)
    # axs[ax_temperature].legend()
    axs[ax_temperature].grid(True)

    # # Gemeinsame Legende unten hinzufügen
    # fig.legend(
    #     handles=[error_marker],
    #     loc='lower center',
    #     bbox_to_anchor=(0.5, -0.015),  # x=0.5 zentriert, y etwas unter dem Plot
    #     ncol=1,
    #     frameon=False
    # )

    def auto_time_ticks(ax, time_data, max_ticks=30):
        time_range_s = max(time_data) - min(time_data)
        intervals = [
            60,
            300,
            600,
            900,
            1800,
            3600,
        ]  # 1min, 5min, 10min, 15min, 30min, 1h
        for interval_s in intervals:
            if time_range_s <= max_ticks * interval_s:
                break
        else:
            interval_s = intervals[-1]  # Fallback: größtes Intervall

        start = (min(time_data) // interval_s) * interval_s
        end = (max(time_data) // interval_s + 1) * interval_s
        ticks = range(int(start), int(end), interval_s)

        ax.set_xticks(ticks)
        ax.set_xticklabels(
            [datetime.datetime.fromtimestamp(t).strftime("%H:%M") for t in ticks],
            rotation=90,
            ha="center",
        )

    if time_s > 1.0:
        auto_time_ticks(axs[-1], list_time_s)

    if filename is not None:
        fig.suptitle(filename.stem, fontsize=10)

    # plt.tight_layout()
    plt.tight_layout()
    if show:
        plt.show()
    if filename is not None:
        print(f"Diagram: {filename}")
        fig.savefig(filename, dpi=dpi)
