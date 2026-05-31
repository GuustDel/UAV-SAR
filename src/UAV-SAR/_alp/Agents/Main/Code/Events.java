void eventDrawPheromones()
{/*ALCODESTART::1778310007029*/
if (!varEnablePheromoneRendering) return;
if (pheromoneCanvas == null) return;
pheromoneCanvas.clear();

double ox = 50;
double oy = 50;
int[][] stops = {
    {255,  80,  0},   // intensity 0.00 — dark orange
    {255, 140,  0},   // intensity 0.17 — orange
    {255, 200,  0},   // intensity 0.33 — amber
    {255, 255,  0},   // intensity 0.50 — yellow
    {180, 255,  0},   // intensity 0.67 — yellow-green
    { 80, 240,  0},   // intensity 0.83 — light green
    {  0, 200,  0}    // intensity 1.00 — green
};

// 1. Pheromone grid tiles
for (int row = 0; row < varGridRows; row++) {
    for (int col = 0; col < varGridCols; col++) {
        int idx = row * varGridCols + col;
        double ph = fnGetPheromone(idx);
        double intensity = Math.min(1.0, ph / 5.0);
        int alpha = (int)(intensity * 220);
        if (alpha < 5) continue;
        int r, g, b;
        int segmentCount = stops.length - 1;
        double scaledIntensity = intensity * segmentCount;
        int seg = Math.min((int)scaledIntensity, segmentCount - 1);
        float t  = (float)(scaledIntensity - seg);
        r = stops[seg][0] + (int)(t * (stops[seg+1][0] - stops[seg][0]));
        g = stops[seg][1] + (int)(t * (stops[seg+1][1] - stops[seg][1]));
        b = stops[seg][2] + (int)(t * (stops[seg+1][2] - stops[seg][2]));
        double px = col * varGridCellSize;
        double py = row * varGridCellSize;
        pheromoneCanvas.fillRectangle(px, py, varGridCellSize, varGridCellSize,
            new java.awt.Color(r, g, b, alpha));
    }
}

// 2. FOV cones — drawn in Main's coordinate space, scale matches sensing exactly
for (UAV u : uavs) {
    boolean visible = !u.varCharging;
    u.cone1.setVisible(visible);
    u.cone2.setVisible(visible);
    u.cone3.setVisible(visible);
    if (!visible) continue;

    boolean detected = (u.varTargetConfidence >= u.varDetectionThreshold)
                       && !u.varMovingToCharger;
    java.awt.Color c = detected
        ? new java.awt.Color(255, 120, 0, 220)
        : new java.awt.Color(80, 190, 255, 180);

    u.cone1.setColor(c);
    u.cone2.setLineColor(c);
    u.cone3.setColor(c);
} 

// 3. Candidate waypoints
for (UAV u : uavs) {
    if (u.varMovingToCharger || u.varCharging) continue;
    int n = Math.min(u.varAcoCandidateCount, u.varCandX.length);
    for (int i = 0; i < n; i++) {
        if (i == u.varChosenIdx) {
            pheromoneCanvas.fillCircle(u.varCandX[i] - ox, u.varCandY[i] - oy, 3,
                new java.awt.Color(255, 50, 50, 220));
        } else {
            pheromoneCanvas.fillCircle(u.varCandX[i] - ox, u.varCandY[i] - oy, 3,
                new java.awt.Color(255, 200, 0, 130));
        }
    }
}

// 4. Found victim markers — red X
for (Victims v : victims) {
    if (!v.varIsFound) continue;
    double mx = v.getX() - ox;
    double my = v.getY() - oy;
    java.awt.Color xColor = new java.awt.Color(220, 0, 0, 255);
    for (int d = -10; d <= 10; d++) {
        pheromoneCanvas.fillCircle(mx + d, my + d, 2, xColor);
        pheromoneCanvas.fillCircle(mx + d, my - d, 2, xColor);
    }
}

if (uavs.size() > 0) uavState0.setText("UAV" + (uavs.get(0).getIndex() + 1) + ": " + uavs.get(0).varCurrentStateName);
if (uavs.size() > 1) uavState1.setText("UAV" + (uavs.get(1).getIndex() + 1) + ": " + uavs.get(1).varCurrentStateName);
/*ALCODEEND*/}

void eventSafetyStop()
{/*ALCODESTART::1778824420442*/
if (!varAllVictimsFound) {
    varConvergenceTime = Double.NaN;
    traceln("TIMEOUT not all victims found by t=" + time()
        + " found=" + varFoundVictimCount + "/" + victims.size());
    fnLogRunSummary();
    finishSimulation();
}
/*ALCODEEND*/}

