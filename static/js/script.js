const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const image = new Image();

image.src = "{{img.image.url}}"
image.onload = function() {
  ctx.drawImage(image, 0,0)
}
const width = image.clientWidth;
const height = image.clientHeight;

canvas.width = width;
canvas.height = height;
