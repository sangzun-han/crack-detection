function handleImageView(files) {
  let file = files[0];

  if (!file.type.match(/image.*/)) {
    alert('not image file!');
  }

  let reader = new FileReader();
  reader.onload = function (e) {
    let img = new Image();
    img.onload = function () {
      let ctx = document.getElementById('canvas').getContext('2d');
      ctx.drawImage(img, 0, 0, 480, 320);
    };
    img.src = e.target.result;
  };

  reader.readAsDataURL(file);
}

function clickEvent(event) {
  const canvas = document.getElementById('canvas');
  const context = canvas.getContext('2d');
  context.beginPath();
  context.arc(event.offsetX, event.offsetY, 2, 0, Math.PI * 2);
  context.fill();
  console.log(event.offsetX, event.offsetY);
}
canvas.addEventListener('click', clickEvent);
``;
