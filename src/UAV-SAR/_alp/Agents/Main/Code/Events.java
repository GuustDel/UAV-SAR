void eventDrawPheromones()
{/*ALCODESTART::1778310007029*/
pheromoneCanvas.clear();

double ox = 50;
double oy = 50;

// 1. Pheromone grid tiles
for (int row = 0; row < varGridRows; row++) {
    for (int col = 0; col < varGridCols; col++) {
        int idx = row * varGridCols + col;
        double ph = fnGetPheromone(idx);
        double intensity = Math.min(1.0, ph / 5.0);
        int alpha = (int)(intensity * 220);
        if (alpha < 5) continue;
        int r, g, b;
        if (intensity < 0.5) {
            float t = (float)(intensity / 0.5);
            r = 255; g = (int)(255 * t); b = 0;
        } else {
            float t = (float)((intensity - 0.5) / 0.5);
            r = (int)(255 * (1 - t)); g = 255; b = 0;
        }
        double px = col * varGridCellSize;
        double py = row * varGridCellSize;
        pheromoneCanvas.fillRectangle(px, py, varGridCellSize, varGridCellSize,
            new java.awt.Color(r, g, b, alpha));
    }
}

// 2. FOV cones — drawn in Main's coordinate space, scale matches sensing exactly
for (UAV u : uavs) {
    if (u.varMovingToCharger || u.varCharging) continue;
 
    double cx          = u.getX() - ox;
    double cy          = u.getY() - oy;
    double centerAngle = u.getRotation();
    double halfRad     = Math.toRadians(u.varFovHalfAngleDeg);
    double rMax        = u.varSensorRange;

    boolean detected = u.varTargetConfidence >= u.varDetectionThreshold;
    java.awt.Color fill = detected
        ? new java.awt.Color(255, 140, 0, 60)
        : new java.awt.Color(100, 200, 255, 50);
    java.awt.Color outline = detected
        ? new java.awt.Color(255, 100, 0, 180)
        : new java.awt.Color(50, 150, 255, 160);

    // Fill slice
    for (double a = centerAngle - halfRad; a <= centerAngle + halfRad; a += Math.toRadians(2)) {
        for (double r = 0; r <= rMax; r += 2) {
            pheromoneCanvas.fillCircle(cx + r * Math.cos(a), cy + r * Math.sin(a), 2, fill);
        }
    }
    // Boundary rays
    for (double r = 0; r <= rMax; r += 2) {
        pheromoneCanvas.fillCircle(cx + r * Math.cos(centerAngle - halfRad),
                                   cy + r * Math.sin(centerAngle - halfRad), 2, outline);
        pheromoneCanvas.fillCircle(cx + r * Math.cos(centerAngle + halfRad),
                                   cy + r * Math.sin(centerAngle + halfRad), 2, outline);
    }
    // Outer arc
    for (double a = centerAngle - halfRad; a <= centerAngle + halfRad; a += Math.toRadians(1)) {
        pheromoneCanvas.fillCircle(cx + rMax * Math.cos(a), cy + rMax * Math.sin(a), 2, outline);
    }
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

// 4. Found victim markers
for (Victims v : victims) {
    if (!v.varIsFound) continue;
    double mx = v.getX() - ox;
    double my = v.getY() - oy;
    pheromoneCanvas.fillCircle(mx, my, 12, new java.awt.Color(255, 0, 0, 180));
    pheromoneCanvas.fillCircle(mx, my, 5,  new java.awt.Color(255, 255, 255, 255));
}
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

