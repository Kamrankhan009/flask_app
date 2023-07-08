const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let circles = [];
let lines = [];
const maxCircleRadius = 5;
const minCircleRadius = 5;
const maxLineDistance = 200;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function init() {
  resizeCanvas();

  // Create circles
  for (let i = 0; i < 200; i++) {
    const radius = Math.random() * (maxCircleRadius - minCircleRadius) + minCircleRadius;
    const x = Math.random() * (canvas.width - radius * 2) + radius;
    const y = Math.random() * (canvas.height - radius * 2) + radius;
    const dx = (Math.random() - 0.5) * 2;
    const dy = (Math.random() - 0.5) * 2;

    circles.push({ x, y, radius, dx, dy });
  }

  animate();
}

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}

async function animate() {
  requestAnimationFrame(animate);
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Update circle positions
  for (let i = 0; i < circles.length; i++) {
    const circle = circles[i];
    circle.x += circle.dx;
    circle.y += circle.dy;

    // Check for collisions with other circles
    for (let j = 0; j < circles.length; j++) {
      if (i !== j) {
        const otherCircle = circles[j];
        const distance = Math.sqrt(
          Math.pow(circle.x - otherCircle.x, 2) +
          Math.pow(circle.y - otherCircle.y, 2)
        );
        const combinedRadius = circle.radius + otherCircle.radius;

        if (distance < combinedRadius) {
          // Circles are colliding, change their directions
          circle.dx = -circle.dx;
          circle.dy = -circle.dy;

          otherCircle.dx = -otherCircle.dx;
          otherCircle.dy = -otherCircle.dy;
        }
      }
    }

    // Keep circles within the canvas bounds
    if (circle.x + circle.radius > canvas.width || circle.x - circle.radius < 0) {
      circle.dx = -circle.dx;
    }
    if (circle.y + circle.radius > canvas.height || circle.y - circle.radius < 0) {
      circle.dy = -circle.dy;
    }

    drawCircle(circle);
  }

  // Draw lines
  lines = [];
  for (let i = 0; i < circles.length; i++) {
    for (let j = i + 1; j < circles.length; j++) {
      const circle1 = circles[i];
      const circle2 = circles[j];

      const distance = Math.sqrt(
        Math.pow(circle1.x - circle2.x, 2) +
        Math.pow(circle1.y - circle2.y, 2)
      );

      if (distance < maxLineDistance) {
        lines.push({ x1: circle1.x, y1: circle1.y, x2: circle2.x, y2: circle2.y });
      }
    }
  }

  drawLines();
}

function drawCircle(circle) {
  ctx.beginPath();
  ctx.arc(circle.x, circle.y, circle.radius, 0, Math.PI * 2);
  ctx.fillStyle = 'red';
  ctx.fill();
  ctx.closePath();
}

function drawLines() {
  for (let i = 0; i < lines.length; i++) {
    drawLine(lines[i]);
  }
}

function drawLine(line) {
  ctx.beginPath();
  ctx.moveTo(line.x1, line.y1);
  ctx.lineTo(line.x2, line.y2);
  ctx.strokeStyle = 'red';
  ctx.stroke();
  ctx.closePath();
}

init();

window.addEventListener('resize', function() {
  resizeCanvas();
  circles = [];
  lines = [];
  init();
});
