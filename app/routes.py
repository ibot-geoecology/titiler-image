from morecantile.defaults import TileMatrixSets, tms as default_tms
from morecantile.models import TileMatrixSet
from pyproj import CRS
from titiler.core.factory import TMSFactory, TilerFactory, ColorMapFactory
from titiler.extensions.cogeo import cogValidateExtension
from titiler.extensions.viewer import cogViewerExtension
from titiler.extensions.wmts import wmtsExtension

CZ_BOUNDS_WGS84 = [12.0, 48.5, 18.9, 51.1]
WGS84 = CRS.from_epsg(4326)


def make_custom_tms(epsg: int) -> TileMatrixSet:
    return TileMatrixSet.custom(
        extent=CZ_BOUNDS_WGS84,
        extent_crs=WGS84,
        crs=CRS.from_epsg(epsg),
        id=f"EPSG{epsg}Quad",
        title=f"Czech Republic grid in EPSG:{epsg}",
        matrix_scale=[1, 1],
    )


supported_tms = TileMatrixSets(
    {
        "EPSG5514Quad": make_custom_tms(5514),
        # Keep WebMercatorQuad aligned with standard XYZ tiling expected by web maps.
        "WebMercatorQuad": default_tms.get("WebMercatorQuad"),
        "EPSG32633Quad": make_custom_tms(32633),
        "EPSG32634Quad": make_custom_tms(32634),
    }
)

cog = TilerFactory(
    router_prefix="/cog",
    extensions=[
        cogValidateExtension(),
        cogViewerExtension(),
        wmtsExtension(),
    ],
    supported_tms=supported_tms,
)

# Optional endpoint exposing the list/definitions of TMS.
tms_router = TMSFactory(supported_tms=supported_tms)

# Colormaps router (built-in TiTiler endpoint)
colormap_router = ColorMapFactory(router_prefix="/cog")
