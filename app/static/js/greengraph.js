const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let circles = [];
let lines = [];
let maxCircleRadius;
let minCircleRadius;
let maxLineDistance;
let animationId;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function init() {
  resizeCanvas();

  // Create circles
  for (let i = 0; i < balls_num; i++) {
    const radius = Math.random() * (maxCircleRadius - minCircleRadius) + minCircleRadius;
    const x = Math.random() * (canvas.width - radius * 2) + radius;
    const y = Math.random() * (canvas.height - radius * 2) + radius;
    const dx = (Math.random() - 0.5) * color2;
    const dy = (Math.random() - 0.5) * color2;
    circles.push({ x, y, radius, dx, dy });
  }

  animate();
}

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const zoomLevel = window.devicePixelRatio || 1;
  const zoomedWidth = canvas.width / zoomLevel;
  const zoomedHeight = canvas.height / zoomLevel;

  maxCircleRadius = 5 / zoomLevel;
  minCircleRadius = 5 / zoomLevel;
  maxLineDistance = 120 / zoomLevel;

  // Adjust circles' positions to stay within the new canvas size
  for (let i = 0; i < circles.length; i++) {
    const circle = circles[i];
    if (circle.x + circle.radius > zoomedWidth) {
      circle.x = zoomedWidth - circle.radius;
    }
    if (circle.x - circle.radius < 0) {
      circle.x = circle.radius;
    }
    if (circle.y + circle.radius > zoomedHeight) {
      circle.y = zoomedHeight - circle.radius;
    }
    if (circle.y - circle.radius < 0) {
      circle.y = circle.radius;
    }
  }
}

function animate() {
  animationId = requestAnimationFrame(animate);
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
  ctx.fillStyle = colors;
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
  ctx.strokeStyle = colors;
  ctx.stroke();
  ctx.closePath();
}

// Initialize the animation
init();

// Listen for window resize event
window.addEventListener('resize', () => {
  cancelAnimationFrame(animationId); // Stop the animation
  circles = []; // Clear the circles array
  lines = []; // Clear the lines array
  resizeCanvas(); // Adjust the canvas size
  init(); // Reinitialize the animation with updated canvas dimensions
});