from src.model.HSteelModel import HSteelModel


steelArgs = {
    'steelHeight': 100,
    'steelwidth': 50,
    'steelCThick': 10,
    'steelTBThick': 10,
    'steelRadio': 8,
    'steelLength': 1000,
    'paintHalfLineLength': 2.5,
    'totalPanelNum': 11
}


model = HSteelModel(steelArgs)

panelHeight = 8
panelWidth = 4
panelThickless = 0.8
paintHalfLength = 2
paintThickless = 0.8
model.getRoutePlanLength(panelHeight, panelWidth, panelThickless, paintHalfLength, paintThickless)