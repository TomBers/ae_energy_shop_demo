import json


def json_res():
    return [
        {
            "annualCost": 1646.34,
            "annualSaving": -768.71,
            "annualSavingPercentage": -87.6,
            "annualStandingChargeElec": 13721.4,
            "annualStandingChargeGas": 7446.6,
            "contractLength": 12,
            "energySwitchGuarantee": False,
            "exitPenaltyAmount": 0.0,
            "saleable": False,
            "supplierName": "Outfox the Market",
            "tariffEndDatePeriodFixed": None,
            "tariffEndDatePeriodRolling": 12,
            "tariffEndDateType": "R",
            "tariffName": "Fix'd 24 4.0",
            "unitPriceElec": 25.866,
            "unitPriceGas": 5.705,
            "warmHomeDiscount": False
        },
        {
            "annualCost": 1678.45,
            "annualSaving": -800.82,
            "annualSavingPercentage": -91.2,
            "annualStandingChargeElec": 18679.5,
            "annualStandingChargeGas": 11539.5,
            "contractLength": 12,
            "energySwitchGuarantee": True,
            "exitPenaltyAmount": 150.0,
            "saleable": False,
            "supplierName": "EDF Energy",
            "tariffEndDatePeriodFixed": "2025-03-31",
            "tariffEndDatePeriodRolling": 0,
            "tariffEndDateType": "F",
            "tariffName": "EDF Essentials 1Yr Mar25v3",
            "unitPriceElec": 23.856,
            "unitPriceGas": 5.704,
            "warmHomeDiscount": True
        },
        {
            "annualCost": 1727.79,
            "annualSaving": -850.16,
            "annualSavingPercentage": -96.9,
            "annualStandingChargeElec": 18430.65,
            "annualStandingChargeGas": 11290.65,
            "contractLength": 12,
            "energySwitchGuarantee": True,
            "exitPenaltyAmount": 0.0,
            "saleable": False,
            "supplierName": "Octopus Energy",
            "tariffEndDatePeriodFixed": None,
            "tariffEndDatePeriodRolling": 12,
            "tariffEndDateType": "R",
            "tariffName": "Octopus 12M Fixed February 2024 v3",
            "unitPriceElec": 24.665,
            "unitPriceGas": 5.961,
            "warmHomeDiscount": True
        },
        {
            "annualCost": 1732.33,
            "annualSaving": -854.7,
            "annualSavingPercentage": -97.4,
            "annualStandingChargeElec": 18679.5,
            "annualStandingChargeGas": 11539.5,
            "contractLength": 24,
            "energySwitchGuarantee": True,
            "exitPenaltyAmount": 250.0,
            "saleable": False,
            "supplierName": "EDF Energy",
            "tariffEndDatePeriodFixed": "2026-03-31",
            "tariffEndDatePeriodRolling": 0,
            "tariffEndDateType": "F",
            "tariffName": "EDF Essentials 2Yr Mar26v3",
            "unitPriceElec": 24.654,
            "unitPriceGas": 5.96,
            "warmHomeDiscount": True
        },
        {
            "annualCost": 1743.21,
            "annualSaving": -865.58,
            "annualSavingPercentage": -98.6,
            "annualStandingChargeElec": 18851.7,
            "annualStandingChargeGas": 11682.3,
            "contractLength": 15,
            "energySwitchGuarantee": True,
            "exitPenaltyAmount": 150.0,
            "saleable": False,
            "supplierName": "British Gas",
            "tariffEndDatePeriodFixed": None,
            "tariffEndDatePeriodRolling": 15,
            "tariffEndDateType": "R",
            "tariffName": "Price Promise",
            "unitPriceElec": 25.12,
            "unitPriceGas": 5.912,
            "warmHomeDiscount": True
        },
        {
            "annualCost": 1759.12,
            "annualSaving": -881.49,
            "annualSavingPercentage": -100.4,
            "annualStandingChargeElec": 18905.25,
            "annualStandingChargeGas": 10800.3,
            "contractLength": 26,
            "energySwitchGuarantee": False,
            "exitPenaltyAmount": 150.0,
            "saleable": False,
            "supplierName": "ScottishPower",
            "tariffEndDatePeriodFixed": "2026-05-31",
            "tariffEndDatePeriodRolling": 0,
            "tariffEndDateType": "F",
            "tariffName": "Help Beat Cancer Green Flexi May 2026 CM1 Online",
            "unitPriceElec": 24.829,
            "unitPriceGas": 6.183,
            "warmHomeDiscount": True
        },
    ]


def get_tariffs():
    return json.dumps(json_res())


def tariffs_schema():
    return {
        "type": "function",
        "function": {
            "name": "get_tariffs",
            "description": "Get available energy tariffs",
            "parameters": {},
        },
    }
