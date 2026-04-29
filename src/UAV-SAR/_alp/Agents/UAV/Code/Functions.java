void fnMoveToRandomWaypoint()
{/*ALCODESTART::1778000001001*/
double margin = 10;
double minX = 100 + margin;
double maxX = 900 - margin;
double minY = 100 + margin;
double maxY = 500 - margin;

double x = uniform(minX, maxX);
double y = uniform(minY, maxY);

setSpeed(Math.max(0.1, varSpeed));
moveTo(x, y, Math.max(0.1, varSpeed));
/*ALCODEEND*/}

void onArrival()
{/*ALCODESTART::1778000001002*/
fnSenseIfOutdated();
fnMoveToRandomWaypoint();
/*ALCODEEND*/}

void fnSenseIfOutdated()
{/*ALCODESTART::1778000001003*/
double now = time();
double elapsed = Math.max(0, now - varLastBeliefUpdateTime);
if (elapsed > 0) {
	varTargetConfidence = Math.max(0, varTargetConfidence - (varBeliefDecayPerSecond * elapsed));
	varLastBeliefUpdateTime = now;
}

if (confidenceText != null) {
	confidenceText.setText(varEnableSenseDebug
		? String.format("c=%.2f", varTargetConfidence)
		: "");
}

boolean isStale = (varLastSenseTime < 0) || ((now - varLastSenseTime) >= varBeliefStaleSeconds);
if (!isStale) {
	return;
}

fnSenseNow();
/*ALCODEEND*/}

void fnSenseNow()
{/*ALCODESTART::1778000001004*/
double bestConfidence = 0;
double bestX = -1;
double bestY = -1;

if (main != null) {
	for (Victims v : main.victims) {
		double d = distanceTo(v);
		if (d <= varSensorRange) {
			double conf = 1.0 - (d / Math.max(1e-6, varSensorRange));
			if (conf > bestConfidence) {
				bestConfidence = conf;
				bestX = v.getX();
				bestY = v.getY();
			}
		}
	}
}

varTargetConfidence = bestConfidence;
if (bestConfidence > 0) {
	varTargetX = bestX;
	varTargetY = bestY;
} else {
	varTargetX = -1;
	varTargetY = -1;
}

varLastSenseTime = time();
varBatteryLevel = Math.max(0, varBatteryLevel - varScanEnergyCost);
varEnergyUsed += varScanEnergyCost;

if (confidenceText != null) {
	confidenceText.setText(varEnableSenseDebug
		? String.format("c=%.2f", varTargetConfidence)
		: "");
}

if (varEnableSenseDebug) {
	traceln(String.format("UAV %d sense t=%.1f conf=%.2f target=(%.1f, %.1f)",
		getIndex(), time(), varTargetConfidence, varTargetX, varTargetY));
}
/*ALCODEEND*/}

