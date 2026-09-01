"""
build_zooom_lens_full_3config_fresh.py

Fresh ZOS-API reconstruction of the complete visible day-channel zoom lens.

This script starts from a brand-new Sequential OpticStudio file. A fresh file
contains exactly three rows by default:

    S0  OBJECT
    S1  STOP
    S2  IMAGE

The script preserves that original STOP and moves it to S29 by inserting the
front prescription before it, then inserts the rear prescription between the
STOP and IMAGE. Final structure:

    G1      S1-S18
    G2      S19-S25
    G3      S26-S28
    STOP    S29
    G4      S29-S48
    IMAGE   S49

Three Multi-Configuration Editor states are created:

    Config 1  WIDE
    Config 2  MID
    Config 3  TELE

Only the physical zoom air spaces are configuration dependent:

    THIC S18
    THIC S25
    THIC S28

YFIE rows change only the object-space field angles so that the same physical
IMX530-class detector radii are sampled in every zoom state.

System setup:
    * Ansys Zemax OpticStudio 2024 R1 ZOS-API / pythonnet
    * Sequential mode, millimetres
    * Float By Stop Size
    * fixed physical stop at S29, radius 13.7785 mm
    * standard F/d/C visible wavelength preset only
    * d-line primary
    * Angle fields
    * Paraxial Ray Aiming with cache
    * OHARA and HIKARI catalog glasses where defensible
    * MODEL glass retained at S17 and S22
    * Even Asphere at S1, S9, S19
    * nine MCE zoom-gap cells made Variable
    * no Merit Function and no optimization

The prescription topology is inspired by the Canon 5x four-group zoom family,
then adapted to the IMX530-class day-channel model used in this project.

USER-EDITABLE LOCATIONS
-----------------------
ZOS-API data root:
    %USERPROFILE%\\Documents\\Zemax

Output:
    %USERPROFILE%\\Downloads\\ZOOOM_LENS_FULL_3CONFIG.ZOS

Change only ZEMAX_DATA_ROOT or OUTPUT_ZOS below if your installation differs.
"""

from __future__ import annotations

import math
import os


# =============================================================================
# USER-EDITABLE PATHS
# =============================================================================

# ZOS-API VERSION / LOCATION:
# Written for Ansys Zemax OpticStudio 2024 R1. The initializer normally finds
# the OpticStudio program installation automatically. Change this path only if
# your Zemax DATA folder is not under Documents\\Zemax.
ZEMAX_DATA_ROOT = os.path.expandvars(
    r"%USERPROFILE%\Documents\Zemax"
)

# Generated ZOS file.
OUTPUT_ZOS = os.path.expandvars(
    r"%USERPROFILE%\Downloads\ZOOOM_LENS_FULL_3CONFIG.ZOS"
)

ALLOW_OVERWRITE = True


# =============================================================================
# SENSOR / SYSTEM CONSTANTS
# =============================================================================

SENSOR_NAME = "Sony IMX530 AAMJ class"
SENSOR_NX = 5328
SENSOR_NY = 4608
PIXEL_PITCH_UM = 2.74
SENSOR_X_MM = 14.59872
SENSOR_Y_MM = 12.62592

# Current image-row aperture used in the working model.
IMAGE_CLEAR_DIAMETER_MM = 19.30484
IMAGE_SEMI_DIAMETER_MM = IMAGE_CLEAR_DIAMETER_MM / 2.0

STOP_SURFACE = 29
STOP_SEMI_DIAMETER_MM = 13.7785

# Expected first-order readbacks for the clean pre-optimization configuration.
EXPECTED_EFL_MM = (
    15.10957,
    34.99207,
    74.97292,
)

EXPECTED_EPD_MM = (
    5.186662,
    12.01319,
    25.73824,
)

EXPECTED_WORKING_FNO = (
    2.985311,
    2.984968,
    2.983426,
)


# =============================================================================
# THREE ZOOM STATES
# =============================================================================
#
# These are the clean three-state values used before the later Stage-A trial.
# Only these three physical air spaces change between configurations.

ZOOM_CONFIGS = (
    {
        "name": "WIDE",
        "d18": 1.200000,
        "d25": 32.214700,
        "d28": 2.735301,
    },
    {
        "name": "MID",
        "d18": 21.340000,
        "d25": 9.590000,
        "d28": 5.230000,
    },
    {
        "name": "TELE",
        "d18": 32.890000,
        "d25": 1.980000,
        "d28": 1.280000,
    },
)


# =============================================================================
# FIELD TABLE
# =============================================================================
#
# Exact Angle-field values used in the present three-configuration model.
# X = 0 for all fields.
#
# IMPORTANT ZOS-API 2024 R1 DETAIL:
# YFIE Param1 is zero-based in this Python/.NET workflow:
#     human Field 2 -> Param1 = 1
#     human Field 3 -> Param1 = 2
#     ...
#     human Field 6 -> Param1 = 5

FIELD_WEIGHTS = (
    1.0,
    1.0,
    1.0,
    1.5,
    1.5,
    2.0,
)

FIELD_Y_DEG = (
    # Config 1: WIDE
    (
        0.000000,
        11.804651,
        17.715973,
        22.684499,
        25.789303,
        32.574339,
    ),
    # Config 2: MID
    (
        0.000000,
        5.154943,
        7.851103,
        10.227757,
        11.781363,
        15.417975,
    ),
    # Config 3: TELE
    (
        0.000000,
        2.410729,
        3.681877,
        4.812952,
        5.559278,
        7.333594,
    ),
)


# =============================================================================
# FULL 48-SURFACE PRESCRIPTION
# =============================================================================
#
# Each tuple is:
#   (surface, radius_mm, nominal_thickness_mm, clear_diameter_mm)
#
# S18/S25/S28 are overwritten by the MCE for every configuration.
# S29 is the physical aperture stop.

SURFACES = (
    ( 1,   86.96069,  2.80000, 99.506),
    ( 2,   37.19554, 28.65314, 72.568),
    ( 3,  287.18991,  2.20000, 71.378),
    ( 4,   82.96532,  9.79457, 68.012),
    ( 5,  233.30951,  2.20000, 67.303),
    ( 6,   49.32285,  9.90654, 64.827),
    ( 7,  122.07948,  4.11145, 64.165),
    ( 8,  174.57379,  7.40358, 63.832),
    ( 9, -162.88781, 10.55549, 63.329),
    (10,  219.22560, 11.10101, 61.797),
    (11,  -70.29224,  0.51997, 61.501),
    (12,  -90.66362,  2.00000, 58.344),
    (13,   77.98219,  9.18481, 56.765),
    (14, -228.82556,  0.21692, 57.161),
    (15,  229.51464, 10.00000, 57.792),
    (16,  -68.94195,  0.20000, 57.805),
    (17,   57.54531,  5.56934, 50.901),
    (18,  174.06610,  1.20000, 50.045),

    (19,  222.99988,  1.30000, 29.397),
    (20,   22.07423,  8.73811, 24.622),
    (21,  -46.00024,  0.90000, 21.288),
    (22,   26.14240,  4.04203, 21.985),
    (23,  -96.70044,  2.91044, 22.088),
    (24,  -20.39226,  0.90000, 22.088),
    (25,  -29.02640, 32.21470, 23.053),

    (26,  -33.53567,  0.90000, 23.727),
    (27,   62.00299,  2.73134, 25.908),
    (28, 5426.95120,  2.735301, 26.494),

    (29, math.inf,    1.04258, 27.557),

    (30,  144.60763,  5.80564, 29.049),
    (31,  -40.31316,  0.20000, 29.778),
    (32,  140.01330,  2.90947, 29.573),
    (33, -127.51474,  0.20000, 29.431),
    (34,   62.82013,  7.44444, 28.583),
    (35,  -31.93064,  1.20000, 27.614),
    (36, 1097.65571,  0.20000, 27.561),
    (37,   27.33320,  3.43062, 27.568),
    (38,   42.89669, 17.98679, 26.842),
    (39,  -77.25420,  4.44564, 23.060),
    (40,  -51.93660, 20.78154, 22.786),
    (41,   72.70188,  7.72582, 25.172),
    (42,  -18.39119,  0.85000, 25.094),
    (43, -145.10189,  2.61020, 27.091),
    (44,  837.85153,  6.19253, 29.071),
    (45,  -37.66305,  0.85000, 29.817),
    (46,  136.96902,  0.19086, 30.863),
    (47,   42.04543,  7.61002, 32.756),
    (48,  -61.55333, 33.54000, 33.050),
)


# =============================================================================
# MATERIAL ASSIGNMENTS
# =============================================================================
#
# Every listed surface carries the catalog glass from that surface to the next.
# S17 and S22 intentionally remain MODEL glasses because their required
# dispersion data are not safely represented by the available catalog choices.

REAL_MATERIALS = {
     1: ("OHARA",  "S-LAH66"),
     3: ("OHARA",  "S-LAH66"),
     5: ("OHARA",  "S-LAH66"),
     6: ("OHARA",  "S-NPH2"),
     8: ("OHARA",  "S-FPL51"),
    10: ("OHARA",  "S-PHM52"),
    12: ("OHARA",  "S-TIH6"),
    13: ("OHARA",  "S-FPL51"),
    15: ("OHARA",  "S-FPM2"),
    19: ("OHARA",  "S-LAH66"),
    21: ("OHARA",  "S-LAH66"),
    24: ("OHARA",  "S-LAM66"),
    26: ("OHARA",  "S-LAL18"),
    27: ("OHARA",  "S-TIH53"),
    30: ("OHARA",  "S-LAH55"),
    32: ("OHARA",  "S-BAL2"),
    34: ("OHARA",  "S-FPL51"),
    35: ("HIKARI", "J-LASFH17"),
    37: ("OHARA",  "S-TIL6"),
    39: ("OHARA",  "S-FSL5"),
    41: ("OHARA",  "S-FSL5"),
    42: ("OHARA",  "S-LAH98"),
    44: ("OHARA",  "L-BBH1"),
    45: ("HIKARI", "J-LASFH17"),
    47: ("OHARA",  "S-FSL5"),
}

MODEL_MATERIALS = {
    17: {
        "nd": 1.730000,
        "vd": 49.00,
        "theta_gf": 0.5575,
    },
    22: {
        "nd": 1.846660,
        "vd": 23.78,
        "theta_gf": 0.6034,
    },
}


# =============================================================================
# EVEN ASPHERES
# =============================================================================
#
# Patent coefficients are A4/A6/A8. OpticStudio Even Asphere mapping:
#   Par1 = A2
#   Par2 = A4
#   Par3 = A6
#   Par4 = A8

ASPHERES = {
    1: {
        "K": +1.16599,
        "A4": +2.14949e-7,
        "A6": -3.88534e-11,
        "A8": +1.50332e-14,
    },
    9: {
        "K": -9.49193,
        "A4": +5.68085e-7,
        "A6": +2.51185e-10,
        "A8": +5.19688e-14,
    },
    19: {
        "K": -437.435,
        "A4": +1.00143e-5,
        "A6": -1.61464e-8,
        "A8": +2.99969e-11,
    },
}


# =============================================================================
# GENERIC ENUM HELPER
# =============================================================================

def _enum_value(enum_type, preferred_names, required_fragments=()):
    import System

    available = [
        str(name)
        for name in System.Enum.GetNames(enum_type)
    ]

    lookup = {
        name.lower(): name
        for name in available
    }

    for preferred in preferred_names:
        actual = lookup.get(preferred.lower())
        if actual is not None:
            return System.Enum.Parse(enum_type, actual)

    fragments = tuple(x.lower() for x in required_fragments)

    for actual in available:
        lower = actual.lower()
        if all(fragment in lower for fragment in fragments):
            return System.Enum.Parse(enum_type, actual)

    raise RuntimeError(
        f"Could not resolve enum {enum_type}. Available: {', '.join(available)}"
    )


# =============================================================================
# ZOS-API CONNECTION
# =============================================================================

def connect_to_opticstudio():
    try:
        import clr
    except ImportError as exc:
        raise RuntimeError(
            "pythonnet is unavailable. Run this from the Python environment "
            "configured for OpticStudio ZOS-API."
        ) from exc

    net_helper = os.path.join(
        ZEMAX_DATA_ROOT,
        "ZOS-API",
        "Libraries",
        "ZOSAPI_NetHelper.dll",
    )

    if not os.path.isfile(net_helper):
        raise FileNotFoundError(
            "ZOSAPI_NetHelper.dll not found. Change ZEMAX_DATA_ROOT if needed:\n"
            + net_helper
        )

    clr.AddReference(net_helper)
    import ZOSAPI_NetHelper

    initializer = ZOSAPI_NetHelper.ZOSAPI_Initializer

    try:
        opticstudio_directory = initializer.GetZemaxDirectory()
    except Exception:
        opticstudio_directory = ""

    if not opticstudio_directory:
        if not initializer.Initialize():
            raise RuntimeError("Could not initialize OpticStudio ZOS-API.")
        opticstudio_directory = initializer.GetZemaxDirectory()

    zosapi_dll = os.path.join(opticstudio_directory, "ZOSAPI.dll")
    zosapi_interfaces_dll = os.path.join(
        opticstudio_directory,
        "ZOSAPI_Interfaces.dll",
    )

    if not os.path.isfile(zosapi_dll):
        raise FileNotFoundError(zosapi_dll)
    if not os.path.isfile(zosapi_interfaces_dll):
        raise FileNotFoundError(zosapi_interfaces_dll)

    clr.AddReference(zosapi_dll)
    clr.AddReference(zosapi_interfaces_dll)

    import ZOSAPI

    connection = ZOSAPI.ZOSAPI_Connection()
    application = connection.CreateNewApplication()

    if application is None:
        raise RuntimeError("Could not create a new OpticStudio application.")

    if not application.IsValidLicenseForAPI:
        application.CloseApplication()
        raise RuntimeError("OpticStudio license is not valid for ZOS-API.")

    system = application.PrimarySystem

    if system is None:
        application.CloseApplication()
        raise RuntimeError("OpticStudio did not return a PrimarySystem.")

    return ZOSAPI, application, system


# =============================================================================
# SYSTEM DATA
# =============================================================================

def configure_wavelengths(ZOSAPI, system_data):
    waves = system_data.Wavelengths

    ok = waves.SelectWavelengthPreset(
        ZOSAPI.SystemData.WavelengthPreset.FdC_Visible
    )

    if not ok:
        raise RuntimeError("Could not select the F/d/C visible preset.")

    if waves.NumberOfWavelengths != 3:
        raise RuntimeError(
            f"Expected 3 F/d/C wavelengths, found {waves.NumberOfWavelengths}."
        )

    # F = wave 1, d = wave 2, C = wave 3.
    waves.GetWavelength(2).MakePrimary()


def configure_fields(ZOSAPI, system_data):
    fields = system_data.Fields

    field_type = _enum_value(
        ZOSAPI.SystemData.FieldType,
        ("Angle",),
        ("angle",),
    )
    fields.SetFieldType(field_type)

    while fields.NumberOfFields > 1:
        if not fields.RemoveField(fields.NumberOfFields):
            raise RuntimeError("Could not remove an existing field point.")

    wide = FIELD_Y_DEG[0]

    field_1 = fields.GetField(1)
    field_1.X = 0.0
    field_1.Y = float(wide[0])
    field_1.Weight = float(FIELD_WEIGHTS[0])

    for index in range(1, 6):
        fields.AddField(
            0.0,
            float(wide[index]),
            float(FIELD_WEIGHTS[index]),
        )

    fields.ClearVignetting()


def configure_ray_aiming(ZOSAPI, system):
    aiming = system.SystemData.RayAiming

    try:
        aiming.RayAiming = ZOSAPI.SystemData.RayAimingMethod.Paraxial
    except Exception:
        # Retain compatibility with API builds that expose this differently.
        pass

    try:
        aiming.UseRayAimingCache = True
    except Exception:
        pass

    try:
        aiming.UseRobustRayAiming = False
    except Exception:
        pass


def ensure_catalogs_in_use(system):
    catalogs = system.SystemData.MaterialCatalogs

    required = ("OHARA", "HIKARI", "SCHOTT")

    available = {
        str(name).upper(): str(name)
        for name in catalogs.GetAvailableCatalogs()
    }

    in_use = {
        str(name).upper()
        for name in catalogs.GetCatalogsInUse()
    }

    for required_name in required:
        if required_name in in_use:
            continue

        actual = available.get(required_name)
        if actual is None:
            # SCHOTT is not currently used by the prescription, so do not fail
            # only because it is unavailable. OHARA and HIKARI are required.
            if required_name == "SCHOTT":
                continue
            raise RuntimeError(
                f"Required glass catalog {required_name} is unavailable."
            )

        if not catalogs.AddCatalog(actual):
            raise RuntimeError(f"Could not activate glass catalog {actual}.")


def configure_system(ZOSAPI, system):
    # IMPORTANT: start from a genuinely fresh file.
    system.New(False)

    system_data = system.SystemData

    system_data.Units.LensUnits = _enum_value(
        ZOSAPI.SystemData.ZemaxSystemUnits,
        ("Millimeters", "Millimeter"),
        ("mill",),
    )

    aperture = system_data.Aperture
    aperture.ApertureType = _enum_value(
        ZOSAPI.SystemData.ZemaxApertureType,
        ("FloatByStopSize", "Float By Stop Size"),
        ("float", "stop"),
    )
    aperture.ApodizationFactor = 0.0
    aperture.SemiDiameterMargin = 0.0
    aperture.SemiDiameterMarginPct = 0.0

    try:
        aperture.FastSemiDiameters = False
    except Exception:
        pass

    configure_wavelengths(ZOSAPI, system_data)
    configure_fields(ZOSAPI, system_data)
    configure_ray_aiming(ZOSAPI, system)
    ensure_catalogs_in_use(system)


# =============================================================================
# MATERIAL HELPERS
# =============================================================================

def model_glass_dpgf(vd, theta_gf):
    # Convert published relative partial dispersion PgF to OpticStudio dPgF.
    normal_pgf = 0.6438 - 0.001682 * float(vd)
    return float(theta_gf) - normal_pgf


def set_model_glass(ZOSAPI, row, nd, vd, theta_gf):
    material_solve = row.MaterialCell.CreateSolveType(
        ZOSAPI.Editors.SolveType.MaterialModel
    )

    model = None
    try:
        model = material_solve._S_MaterialModel
    except Exception:
        pass

    if model is None:
        model = material_solve

    model.IndexNd = float(nd)
    model.AbbeVd = float(vd)
    model.dPgF = float(model_glass_dpgf(vd, theta_gf))

    try:
        model.VaryIndex = False
        model.VaryAbbe = False
        model.VarydPgF = False
    except Exception:
        pass

    row.MaterialCell.SetSolveData(material_solve)


def set_catalog_glass(ZOSAPI, row, glass_name):
    # Remove any model-material solve if present, then assign catalog glass.
    try:
        fixed = row.MaterialCell.CreateSolveType(ZOSAPI.Editors.SolveType.Fixed)
        if fixed is not None:
            row.MaterialCell.SetSolveData(fixed)
    except Exception:
        pass

    row.Material = str(glass_name)

    if str(row.Material).upper() != str(glass_name).upper():
        raise RuntimeError(
            f"Catalog material assignment failed: requested {glass_name}, "
            f"LDE shows {row.Material}."
        )


# =============================================================================
# SURFACE HELPERS
# =============================================================================

def set_standard_surface(row, radius_mm, thickness_mm, clear_diameter_mm, comment):
    row.Comment = str(comment)
    row.Radius = math.inf if math.isinf(radius_mm) else float(radius_mm)
    row.Thickness = float(thickness_mm)
    row.Conic = 0.0
    row.SemiDiameter = float(clear_diameter_mm / 2.0)


def set_even_asphere(
    ZOSAPI,
    row,
    radius_mm,
    thickness_mm,
    clear_diameter_mm,
    coeffs,
    comment,
):
    settings = row.GetSurfaceTypeSettings(
        ZOSAPI.Editors.LDE.SurfaceType.EvenAspheric
    )
    row.ChangeType(settings)

    row.Comment = str(comment)
    row.Radius = float(radius_mm)
    row.Thickness = float(thickness_mm)
    row.Conic = float(coeffs["K"])
    row.SemiDiameter = float(clear_diameter_mm / 2.0)

    # A2 = 0, patent A4/A6/A8 -> Par2/Par3/Par4.
    row.GetSurfaceCell(
        ZOSAPI.Editors.LDE.SurfaceColumn.Par1
    ).DoubleValue = 0.0

    row.GetSurfaceCell(
        ZOSAPI.Editors.LDE.SurfaceColumn.Par2
    ).DoubleValue = float(coeffs["A4"])

    row.GetSurfaceCell(
        ZOSAPI.Editors.LDE.SurfaceColumn.Par3
    ).DoubleValue = float(coeffs["A6"])

    row.GetSurfaceCell(
        ZOSAPI.Editors.LDE.SurfaceColumn.Par4
    ).DoubleValue = float(coeffs["A8"])


# =============================================================================
# BUILD COMPLETE LDE FROM THE DEFAULT OBJ / STOP / IMAGE FILE
# =============================================================================

def build_full_lde(ZOSAPI, system):
    lde = system.LDE

    if lde.NumberOfSurfaces != 3:
        raise RuntimeError(
            "Fresh Sequential file must start with OBJ + STOP + IMAGE = 3 rows; "
            f"found {lde.NumberOfSurfaces}."
        )

    if not lde.GetSurfaceAt(0).IsObject:
        raise RuntimeError("Default S0 is not OBJECT.")
    if not lde.GetSurfaceAt(1).IsStop:
        raise RuntimeError("Default S1 is not STOP.")
    if not lde.GetSurfaceAt(2).IsImage:
        raise RuntimeError("Default S2 is not IMAGE.")

    # Insert S1-S28 in front of the original STOP. The original STOP moves
    # from S1 to S29 and remains the physical stop.
    for surface_number in range(1, 29):
        lde.InsertNewSurfaceAt(surface_number)

    if not lde.GetSurfaceAt(29).IsStop:
        raise RuntimeError("Original STOP was not preserved at S29.")

    # Insert S30-S48 between S29 STOP and the IMAGE. IMAGE moves to S49.
    for surface_number in range(30, 49):
        lde.InsertNewSurfaceAt(surface_number)

    if lde.NumberOfSurfaces != 50:
        raise RuntimeError(
            "Expected OBJ + 48 optical surfaces + IMAGE = 50 rows; "
            f"found {lde.NumberOfSurfaces}."
        )

    if not lde.GetSurfaceAt(29).IsStop:
        raise RuntimeError("STOP is not S29 after all insertions.")
    if not lde.GetSurfaceAt(49).IsImage:
        raise RuntimeError("IMAGE is not S49 after all insertions.")

    lde.GetSurfaceAt(0).Comment = (
        "OBJECT AT INFINITY - IMX530 VISIBLE 5X ZOOM"
    )

    for surface_number, radius, thickness, clear_diameter in SURFACES:
        row = lde.GetSurfaceAt(surface_number)

        # MCE configuration 1 starts from these WIDE air gaps.
        if surface_number == 18:
            thickness = ZOOM_CONFIGS[0]["d18"]
        elif surface_number == 25:
            thickness = ZOOM_CONFIGS[0]["d25"]
        elif surface_number == 28:
            thickness = ZOOM_CONFIGS[0]["d28"]

        if surface_number in ASPHERES:
            set_even_asphere(
                ZOSAPI,
                row,
                radius,
                thickness,
                clear_diameter,
                ASPHERES[surface_number],
                f"S{surface_number:02d} EVEN ASPHERE",
            )
        else:
            set_standard_surface(
                row,
                radius,
                thickness,
                clear_diameter,
                (
                    "S29 PHYSICAL APERTURE STOP"
                    if surface_number == 29
                    else f"S{surface_number:02d}"
                ),
            )

        if surface_number in REAL_MATERIALS:
            catalog, glass_name = REAL_MATERIALS[surface_number]
            set_catalog_glass(ZOSAPI, row, glass_name)
            row.Comment = f"{row.Comment} | {catalog}:{glass_name}"

        elif surface_number in MODEL_MATERIALS:
            model = MODEL_MATERIALS[surface_number]
            set_model_glass(
                ZOSAPI,
                row,
                model["nd"],
                model["vd"],
                model["theta_gf"],
            )
            row.Comment = (
                f"{row.Comment} | MODEL Nd={model['nd']:.6f} "
                f"Vd={model['vd']:.2f}"
            )

        else:
            row.Material = ""

    stop = lde.GetSurfaceAt(29)
    if not stop.IsStop:
        raise RuntimeError("S29 lost the STOP flag.")
    stop.Comment = "S29 PHYSICAL APERTURE STOP - FIXED"
    stop.SemiDiameter = float(STOP_SEMI_DIAMETER_MM)

    image = lde.GetSurfaceAt(49)
    image.Comment = "IMX530-CLASS IMAGE PLANE - FIXED"
    image.Thickness = 0.0
    image.SemiDiameter = float(IMAGE_SEMI_DIAMETER_MM)

    return lde


# =============================================================================
# MULTI-CONFIGURATION EDITOR
# =============================================================================

def _change_mce_type(ZOSAPI, row, operand_name):
    operand_type = _enum_value(
        ZOSAPI.Editors.MCE.MultiConfigOperandType,
        (operand_name,),
        (operand_name.lower(),),
    )

    # ChangeType is void in some pythonnet builds, so verify after changing.
    row.ChangeType(operand_type)

    if row.Type != operand_type:
        raise RuntimeError(
            f"Could not change MCE row to {operand_name}; got {row.Type}."
        )

    return operand_type


def _set_mce_values(row, values):
    if len(values) != 3:
        raise ValueError("Exactly three WIDE/MID/TELE values are required.")

    for config_number, value in enumerate(values, start=1):
        cell = row.GetOperandCell(config_number)

        if cell is None or not cell.IsActive:
            raise RuntimeError(
                f"Inactive MCE cell in configuration {config_number}."
            )

        cell.DoubleValue = float(value)


def add_mce_thic(ZOSAPI, mce, surface_number, values, existing_row=None):
    row = existing_row if existing_row is not None else mce.AddOperand()

    if row is None:
        raise RuntimeError(f"Could not create THIC row for S{surface_number}.")

    _change_mce_type(ZOSAPI, row, "THIC")

    if not row.Param1Enabled:
        raise RuntimeError("THIC row does not expose Param1.")

    row.Param1 = int(surface_number)
    _set_mce_values(row, values)
    return row


def add_mce_yfie(ZOSAPI, mce, human_field_number, values):
    row = mce.AddOperand()

    if row is None:
        raise RuntimeError(
            f"Could not create YFIE row for human Field {human_field_number}."
        )

    _change_mce_type(ZOSAPI, row, "YFIE")

    if not row.Param1Enabled:
        raise RuntimeError("YFIE row does not expose Param1.")

    # Correct 2024 R1 Python/.NET mapping:
    # human Field 2 -> Param1 1, ..., human Field 6 -> Param1 5.
    row.Param1 = int(human_field_number - 1)
    _set_mce_values(row, values)
    return row


def configure_mce(ZOSAPI, system):
    mce = system.MCE

    # A fresh New(False) system has 1 configuration and 1 default operand row.
    if (
        mce.NumberOfConfigurations != 1
        or mce.NumberOfOperands != 1
    ):
        raise RuntimeError(
            "Expected fresh MCE = 1 configuration + 1 default row; "
            f"found {mce.NumberOfConfigurations} configs and "
            f"{mce.NumberOfOperands} rows."
        )

    default_row = mce.GetOperandAt(1)
    if default_row is None:
        raise RuntimeError("Could not access default MCE row.")

    if not mce.AddConfiguration(False):
        raise RuntimeError("Could not add MID configuration.")
    if not mce.AddConfiguration(False):
        raise RuntimeError("Could not add TELE configuration.")

    if mce.NumberOfConfigurations != 3:
        raise RuntimeError(
            f"Expected exactly 3 configurations, found {mce.NumberOfConfigurations}."
        )

    # Physical zoom motion.
    add_mce_thic(
        ZOSAPI,
        mce,
        18,
        tuple(cfg["d18"] for cfg in ZOOM_CONFIGS),
        existing_row=default_row,
    )

    add_mce_thic(
        ZOSAPI,
        mce,
        25,
        tuple(cfg["d25"] for cfg in ZOOM_CONFIGS),
    )

    add_mce_thic(
        ZOSAPI,
        mce,
        28,
        tuple(cfg["d28"] for cfg in ZOOM_CONFIGS),
    )

    # Analysis-only field angles. Field 1 = 0 deg in all states, so only
    # human Fields 2-6 need YFIE rows.
    for human_field_number in range(2, 7):
        values = tuple(
            FIELD_Y_DEG[config_index][human_field_number - 1]
            for config_index in range(3)
        )
        add_mce_yfie(
            ZOSAPI,
            mce,
            human_field_number,
            values,
        )

    if mce.NumberOfOperands != 8:
        raise RuntimeError(
            f"Expected 8 MCE rows = 3 THIC + 5 YFIE; found {mce.NumberOfOperands}."
        )

    if not mce.SetCurrentConfiguration(1):
        raise RuntimeError("Could not select WIDE configuration.")

    return mce


def make_zoom_gaps_variable(system, mce):
    # Clear any accidental variables before defining the only nine variables.
    system.Tools.RemoveAllVariables()

    count = 0

    for row_number in (1, 2, 3):
        row = mce.GetOperandAt(row_number)

        for config_number in (1, 2, 3):
            cell = row.GetOperandCell(config_number)

            if cell is None or not cell.IsActive:
                raise RuntimeError(
                    f"Inactive MCE cell row {row_number}, config {config_number}."
                )

            if not cell.MakeSolveVariable():
                raise RuntimeError(
                    f"Could not make MCE row {row_number}, "
                    f"config {config_number} Variable."
                )

            count += 1

    if count != 9:
        raise RuntimeError(f"Expected 9 zoom variables, created {count}.")

    return count


# =============================================================================
# VERIFICATION
# =============================================================================

def verify_wavelengths(system):
    waves = system.SystemData.Wavelengths

    if waves.NumberOfWavelengths != 3:
        raise RuntimeError("Wavelength table does not contain exactly 3 waves.")

    values = tuple(
        float(waves.GetWavelength(i).Wavelength)
        for i in (1, 2, 3)
    )

    expected = (
        0.4861327,
        0.5875618,
        0.6562725,
    )

    for actual, target in zip(values, expected):
        if abs(actual - target) > 2.0e-6:
            raise RuntimeError(
                f"Unexpected F/d/C wavelength: got {actual}, expected {target}."
            )

    return values


def verify_lde(lde):
    if lde.NumberOfSurfaces != 50:
        raise RuntimeError(f"Expected 50 LDE rows; found {lde.NumberOfSurfaces}.")

    if not lde.GetSurfaceAt(0).IsObject:
        raise RuntimeError("S0 is not OBJECT.")
    if not lde.GetSurfaceAt(29).IsStop:
        raise RuntimeError("S29 is not STOP.")
    if not lde.GetSurfaceAt(49).IsImage:
        raise RuntimeError("S49 is not IMAGE.")

    # Verify every prescription radius and WIDE thickness after writing.
    for surface_number, radius, nominal_thickness, _clear_diameter in SURFACES:
        row = lde.GetSurfaceAt(surface_number)

        expected_thickness = nominal_thickness
        if surface_number == 18:
            expected_thickness = ZOOM_CONFIGS[0]["d18"]
        elif surface_number == 25:
            expected_thickness = ZOOM_CONFIGS[0]["d25"]
        elif surface_number == 28:
            expected_thickness = ZOOM_CONFIGS[0]["d28"]

        actual_radius = float(row.Radius)
        actual_thickness = float(row.Thickness)

        if math.isinf(radius):
            if not math.isinf(actual_radius):
                raise RuntimeError(f"S{surface_number}: radius readback failed.")
        else:
            if abs(actual_radius - radius) > 1.0e-8:
                raise RuntimeError(
                    f"S{surface_number}: radius {actual_radius} != {radius}."
                )

        if abs(actual_thickness - expected_thickness) > 1.0e-8:
            raise RuntimeError(
                f"S{surface_number}: thickness {actual_thickness} "
                f"!= {expected_thickness}."
            )


def verify_mce(mce):
    if mce.NumberOfConfigurations != 3:
        raise RuntimeError("MCE does not contain exactly 3 configurations.")

    if mce.NumberOfOperands != 8:
        raise RuntimeError("MCE does not contain exactly 8 operands.")

    expected_thic = {
        1: 18,
        2: 25,
        3: 28,
    }

    for row_number, surface_number in expected_thic.items():
        row = mce.GetOperandAt(row_number)

        if "THIC" not in str(row.Type).upper():
            raise RuntimeError(f"MCE row {row_number} is not THIC.")

        if int(row.Param1) != surface_number:
            raise RuntimeError(
                f"MCE row {row_number} should control S{surface_number}; "
                f"found Param1={row.Param1}."
            )

    for row_number, human_field_number in zip(range(4, 9), range(2, 7)):
        row = mce.GetOperandAt(row_number)

        if "YFIE" not in str(row.Type).upper():
            raise RuntimeError(f"MCE row {row_number} is not YFIE.")

        expected_param1 = human_field_number - 1
        if int(row.Param1) != expected_param1:
            raise RuntimeError(
                f"MCE row {row_number}: human Field {human_field_number} "
                f"must use Param1={expected_param1}; found {row.Param1}."
            )


def print_summary(system, lde, mce, output_path, variable_count):
    waves = verify_wavelengths(system)

    print()
    print("FULL ZOOM LENS CREATED")
    print("======================")
    print(f"Saved:\n{output_path}")

    print()
    print("LDE")
    print("---")
    print("G1    : S1-S18")
    print("G2    : S19-S25")
    print("G3    : S26-S28")
    print("STOP  : S29")
    print("G4    : S29-S48")
    print("IMAGE : S49")
    print(f"LDE rows: {lde.NumberOfSurfaces}")

    print()
    print("Sensor")
    print("------")
    print(f"{SENSOR_NAME}")
    print(f"{SENSOR_NX} x {SENSOR_NY}, {PIXEL_PITCH_UM:.2f} um pitch")
    print(f"Active area = {SENSOR_X_MM:.5f} x {SENSOR_Y_MM:.5f} mm")

    print()
    print("Materials")
    print("---------")
    print("Catalogs: OHARA / HIKARI (SCHOTT also activated when available)")
    print(f"Catalog glass surfaces: {len(REAL_MATERIALS)}")
    print("MODEL S17: Nd=1.730000, Vd=49.00, theta_gF=0.5575")
    print("MODEL S22: Nd=1.846660, Vd=23.78, theta_gF=0.6034")

    print()
    print("Aspheres")
    print("--------")
    print("S1, S9, S19")

    print()
    print("Aperture")
    print("--------")
    print("Float By Stop Size")
    print(f"Fixed stop S29 radius = {STOP_SEMI_DIAMETER_MM:.4f} mm")
    print("Expected EPD readback by configuration:")
    print(f"  WIDE = {EXPECTED_EPD_MM[0]:.6f} mm")
    print(f"  MID  = {EXPECTED_EPD_MM[1]:.6f} mm")
    print(f"  TELE = {EXPECTED_EPD_MM[2]:.6f} mm")

    print()
    print("Wavelengths")
    print("-----------")
    print(" / ".join(f"{value:.7f} um" for value in waves))
    print("Primary = d-line, Wave 2")

    print()
    print("MCE")
    print("---")
    print(f"Configurations: {mce.NumberOfConfigurations}")
    print(f"Operands: {mce.NumberOfOperands}")
    print(f"Variable zoom-gap cells: {variable_count}")

    for index, cfg in enumerate(ZOOM_CONFIGS, start=1):
        print(
            f"Config {index} {cfg['name']:4s}: "
            f"S18={cfg['d18']:.6f}, "
            f"S25={cfg['d25']:.6f}, "
            f"S28={cfg['d28']:.6f}, "
            f"expected EFL={EXPECTED_EFL_MM[index-1]:.5f} mm"
        )
        print(
            "    Y fields = "
            + ", ".join(f"{x:.6f}" for x in FIELD_Y_DEG[index - 1])
            + " deg"
        )

    print()
    print("No Merit Function was created.")
    print("No optimization was run.")
    print("The 9 physical zoom-gap MCE cells are Variable and ready for later use.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    output_dir = os.path.dirname(OUTPUT_ZOS)
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(OUTPUT_ZOS) and not ALLOW_OVERWRITE:
        raise FileExistsError(f"Output already exists:\n{OUTPUT_ZOS}")

    application = None

    try:
        print("[1/8] Connecting to OpticStudio 2024 R1 ZOS-API...", flush=True)
        ZOSAPI, application, system = connect_to_opticstudio()

        print("[2/8] Creating NEW Sequential system data...", flush=True)
        configure_system(ZOSAPI, system)

        print("[3/8] Building complete S1-S48 real lens...", flush=True)
        lde = build_full_lde(ZOSAPI, system)

        print("[4/8] Creating WIDE / MID / TELE MCE...", flush=True)
        mce = configure_mce(ZOSAPI, system)

        print("[5/8] Making only S18/S25/S28 MCE cells Variable...", flush=True)
        variable_count = make_zoom_gaps_variable(system, mce)

        print("[6/8] Verifying LDE / MCE / F-d-C setup...", flush=True)
        verify_lde(lde)
        verify_mce(mce)
        verify_wavelengths(system)

        if not mce.SetCurrentConfiguration(1):
            raise RuntimeError("Could not return to WIDE before save.")

        print("[7/8] Saving fresh full zoom lens...", flush=True)
        system.SaveAs(OUTPUT_ZOS)

        print("[8/8] Completed.", flush=True)
        print_summary(system, lde, mce, OUTPUT_ZOS, variable_count)

    finally:
        if application is not None:
            print("Closing ZOS-API application...", flush=True)
            application.CloseApplication()


if __name__ == "__main__":
    main()
