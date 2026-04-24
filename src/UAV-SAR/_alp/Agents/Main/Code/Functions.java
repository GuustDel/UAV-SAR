void fnPlaceVictimsGMM()
{/*ALCODESTART::1777049001651*/
int nClusters = varNClusters;
double margin = varGmmMargin;

// choose cluster centers ONCE
double[][] centers = new double[nClusters][2];

for (int i = 0; i < nClusters; i++) {
  centers[i][0] = uniform(
    spaceRelease.getX() + margin,
    spaceRelease.getX() + spaceRelease.getWidth() - margin
  );

  centers[i][1] = uniform(
    spaceRelease.getY() + margin,
    spaceRelease.getY() + spaceRelease.getHeight() - margin
  );

  traceln("Cluster " + i + " center = " + centers[i][0] + ", " + centers[i][1]);
}

// place victims
for (Victims v : victims) {

  double u = uniform(0, 1);
  int k = 0;

  double cumulative = 0;
  for (int i = 0; i < varGmmWeights.length; i++) {
    cumulative += varGmmWeights[i];
    if (u <= cumulative) {
      k = i;
      break;
    }
  }

  double x = normal(varGmmSd[k][0], centers[k][0]);
  double y = normal(varGmmSd[k][1], centers[k][1]);

  v.setXY(x, y);

  traceln("Victim placed in cluster " + k + " at " + x + ", " + y);
}
/*ALCODEEND*/}

