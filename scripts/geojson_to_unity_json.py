import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ACCESS_POINTS_PATH = PROJECT_ROOT / "data" / "raw" / "access_points.geojson"
ACCESS_POINTS_GPS_PATH = PROJECT_ROOT / "data" / "raw" / "access_points_gps.geojson"
UTILITIES_PATH = PROJECT_ROOT / "data" / "raw" / "utilities.geojson"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "unity_utilities.json"

ORIGIN_POINT_ID = "A0"


def load_geojson(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_point_coordinates(feature):
    return feature["geometry"]["coordinates"]


def convert_to_local_coordinates(coordinates, origin):
    x = coordinates[0] - origin[0]
    z = coordinates[1] - origin[1]

    return {
        "x": round(x, 3),
        "z": round(z, 3)
    }


def get_line_coordinates(feature):
    geometry = feature["geometry"]
    geometry_type = geometry["type"]
    coordinates = geometry["coordinates"]

    if geometry_type == "LineString":
        return coordinates

    if geometry_type == "MultiLineString":
        return coordinates[0]

    raise ValueError(f"Unsupported geometry type: {geometry_type}")


def build_gps_lookup(access_points_gps_geojson):
    gps_lookup = {}

    for feature in access_points_gps_geojson["features"]:
        properties = feature["properties"]
        point_id = properties.get("point_id")

        if not point_id:
            continue

        coords = feature["geometry"]["coordinates"]

        gps_lookup[point_id] = {
            "longitude": coords[0],
            "latitude": coords[1]
        }

    return gps_lookup


def main():
    access_points_geojson = load_geojson(ACCESS_POINTS_PATH)
    access_points_gps_geojson = load_geojson(ACCESS_POINTS_GPS_PATH)
    utilities_geojson = load_geojson(UTILITIES_PATH)

    gps_lookup = build_gps_lookup(access_points_gps_geojson)

    origin_coordinates = None

    for feature in access_points_geojson["features"]:
        properties = feature["properties"]

        if properties.get("point_id") == ORIGIN_POINT_ID:
            origin_coordinates = get_point_coordinates(feature)
            break

    if origin_coordinates is None:
        raise ValueError(f"Origin point {ORIGIN_POINT_ID} was not found.")

    access_points = []

    for feature in access_points_geojson["features"]:
        properties = feature["properties"]
        coordinates = get_point_coordinates(feature)
        local_coordinates = convert_to_local_coordinates(coordinates, origin_coordinates)
        point_id = properties.get("point_id")

        access_points.append({
            "point_id": point_id,
            "type": properties.get("type"),
            "position": local_coordinates,
            "gps_coordinates": gps_lookup.get(point_id),
            "notes": properties.get("notes")
        })

    utilities = []

    for feature in utilities_geojson["features"]:
        properties = feature["properties"]
        line_coordinates = get_line_coordinates(feature)

        local_line_coordinates = [
            convert_to_local_coordinates(coordinate, origin_coordinates)
            for coordinate in line_coordinates
        ]

        utilities.append({
            "line_id": properties.get("line_id"),
            "type": properties.get("type"),
            "depth": properties.get("depth"),
            "material": properties.get("material"),
            "from": properties.get("from"),
            "to": properties.get("to"),
            "coordinates": local_line_coordinates
        })

    output_data = {
        "origin_point_id": ORIGIN_POINT_ID,
        "access_points": access_points,
        "utilities": utilities
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=2, ensure_ascii=False)

   
    try:
        relative_path = OUTPUT_PATH.relative_to(PROJECT_ROOT)
    except ValueError:
        relative_path = OUTPUT_PATH.name

    print(f"Unity JSON created: {relative_path}")


if __name__ == "__main__":
    main()