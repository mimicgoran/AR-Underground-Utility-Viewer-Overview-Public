# AR Underground Utility Viewer

## Repository note

This repository provides only a high level overview of the prototype.

The complete working dataset, implementation details, technical documentation, experiments, and internal development notes are maintained separately.

Access to the full documentation and dataset can be provided upon request.

## 1. Project overview

This project is a mobile augmented reality prototype for visualizing underground utility infrastructure in the real world.

The main idea is to allow a user to stand on site, point a phone toward the ground, place reference points on visible telecom access points, and see underground infrastructure aligned with the physical environment.

The current MVP visualizes:

1. Telecom cables
2. Electric cables
3. Water pipes

The alignment is currently based on visible telecom access points. Other utility geometries are positioned relative to those reference points using GIS data.

The project combines:

1. GIS data preparation
2. GeoJSON export from QGIS
3. Python data conversion
4. Unity mobile AR application
5. ARCore ground plane detection
6. Manual reference point placement
7. Spatial alignment of GIS geometry in AR space
8. Utility labels in the AR scene

The project is intentionally limited to a small test area. The goal is not to build a full city scale system, but to create a strong proof of concept.

## 2. MVP scope

The MVP is based on a small local utility network.

The test area contains:

1. Visible telecom access points used as alignment references
2. Telecom cable geometry
3. Electric cable geometry
4. Water pipe geometry
5. Utility lines spatially positioned relative to the telecom reference points

The current app does not use automatic computer vision detection yet. Reference points are placed manually by the user.

The intended workflow is:

1. User opens the AR app
2. User sees the live camera feed
3. Green placement preview appears on the detected ground plane
4. User places the first reference point on the first visible telecom access point
5. User places the second reference point on the second visible telecom access point
6. App aligns the GIS network using those 2 reference points
7. App renders telecom, electric, and water utilities
8. App displays labels such as Telecom cable, Electric cable, and Water pipe

## 3. Technology stack

The prototype uses:

1. QGIS for GIS data preparation
2. GeoJSON as the exchange format
3. Python for data transformation
4. Unity for mobile development
5. AR Foundation and ARCore for AR functionality
6. Android as the target platform

## 4. Current features

Current implemented features include:

1. Mobile AR camera view
2. Ground plane detection
3. AR placement preview
4. Manual placement of reference points
5. Two point GIS to AR alignment
6. Rendering of telecom, electric, and water utility lines
7. Floating labels for utility identification
8. Local JSON based utility data loading

## 5. Potential improvements

This MVP can be extended in several directions.

### 5.1 Computer vision based detection

A future version could use computer vision to detect visible access points such as manholes, covers, utility boxes, or valves.

Possible approach:

1. Train a lightweight YOLO model
2. Detect manholes or access points in the camera feed
3. Use the detected object center for AR raycasting
4. Automatically place a reference point
5. Match it with the nearest GIS access point

This would reduce the need for manual point placement.

### 5.2 AI assisted field workflow

AI could support the workflow by:

1. Identifying likely utility access objects from camera snapshots
2. Assisting with object classification
3. Suggesting the most likely utility type
4. Helping field users interpret visible infrastructure
5. Summarizing utility metadata for non technical users

For real time detection, an on device model would be more suitable than cloud based AI due to latency and connectivity requirements.

### 5.3 Improved alignment

Future alignment improvements could include:

1. Using more than 2 reference points
2. Calculating alignment error
3. Showing confidence score
4. Warning users when reference points are inconsistent
5. Combining AR tracking, GIS geometry, GPS, and visual detection

### 5.4 Realistic visualization

The current MVP uses line rendering.

Future versions could include:

1. 3D cable or pipe models
2. Utility depth visualization
3. Transparent underground view
4. Different styles for different utility types
5. Interactive popups with metadata

### 5.5 Data integration

The prototype currently uses local JSON data.

Future versions could connect to:

1. ArcGIS Feature Services
2. PostGIS database
3. cloud hosted utility datasets
4. municipal infrastructure systems
5. field data collection platforms

## 6. Potential challenges

Several challenges should be considered before moving toward a production ready solution:

1. Phone GPS accuracy may not be sufficient in certain scenarios for precise underground utility alignment, particularly in dense urban environments or when reference points are closely spaced
2. GIS data must be spatially accurate and well maintained
3. Utility lines must be correctly snapped to access points
4. AR plane detection can be affected by poor lighting or reflective surfaces
5. Manual reference point placement introduces user error
6. Computer vision models require suitable training data
7. Underground infrastructure records may be incomplete or outdated
8. Field conditions such as parked cars, shadows, and occlusions can affect detection

## 7. Current project status

This is an MVP and proof of concept.

It is not intended to be used as a production grade utility locating tool.

The purpose is to demonstrate how GIS data, AR visualization, and spatial alignment logic can be combined into a practical field oriented prototype.
