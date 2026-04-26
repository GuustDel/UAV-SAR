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

public void onArrival()
{/*ALCODESTART::1778000001002*/
fnMoveToRandomWaypoint();
/*ALCODEEND*/}
