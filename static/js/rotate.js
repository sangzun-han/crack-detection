function setup() {
  createCanvas('{{width}}', '{{height}}');
  let x = 0;
  let y = 0;
  let max_x = Number.MIN_SAFE_INTEGER;
  let min_x = Number.MAX_SAFE_INTEGER;
  let max_y = Number.MIN_SAFE_INTEGER;
  let min_y = Number.MAX_SAFE_INTEGER;
  let xMaxIndex = 0;
  let yMaxIndex = 0;
  let center = [];

  for (let i = 0; i < point.length; i++) {
    x += point[i][0];
    y += point[i][1];
  }

  for (let i = 0; i < point.length; i++) {
    if (max_x < point[i][0]) {
      max_x = point[i][0];
      xMaxIndex = i;
    } else if (min_x > point[i][0]) {
      min_x = point[i][0];
    }
  }

  for (let i = 0; i < point.length; i++) {
    if (max_y < point[i][1]) {
      max_y = point[i][1];
      yMaxIndex = i;
    } else if (min_y > point[i][1]) {
      min_y = point[i][1];
    }
  }
  width = max_x - min_x;
  height = max_y - min_y;
  console.log(max_x, min_x);
  console.log(max_y, min_y);

  x = parseInt(x / point.length);
  y = parseInt(y / point.length);
  center.push(x, y);

  angle = getAngleFromThreePoints(point[xMaxIndex], center, point[yMaxIndex]);
  // angle = getAngle(x, y);
  // console.log(x, y, width, height);
  document.getElementById('defaultCanvas0').style.transform = `rotate(${
    angle - 90
  }deg)`;
  console.log((width / 2) * (height / 2) * 3.14);
  console.log(width, height);
  ellipse(x, y, width, height);
}

function getAngleFromThreePoints(p1, p2, p3) {
  let p12 = Math.sqrt(Math.pow(p1[0] - p2[0], 2) + Math.pow(p1[1] - p2[1], 2));
  let p23 = Math.sqrt(Math.pow(p2[0] - p3[0], 2) + Math.pow(p2[1] - p3[1], 2));
  let p31 = Math.sqrt(Math.pow(p3[0] - p1[0], 2) + Math.pow(p3[1] - p1[1], 2));
  let radian = Math.acos((p12 * p12 + p23 * p23 - p31 * p31) / (2 * p12 * p23));

  let degree = parseInt((radian / Math.PI) * 180);
  return degree;
}
