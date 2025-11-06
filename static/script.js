// Parallax background effect
const bg3d = document.getElementById('bg3d');
let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;
    
    targetX = (mouseX - centerX) / centerX * 30;
    targetY = (mouseY - centerY) / centerY * 30;
});

function animateParallax() {
    const currentX = targetX * 0.05 + (parseFloat(bg3d.style.transform.match(/translateX\\((.*?)px\\)/)?.[1] || 0) * 0.95);
    const currentY = targetY * 0.05 + (parseFloat(bg3d.style.transform.match(/translateY\\((.*?)px\\)/)?.[1] || 0) * 0.95);
    
    bg3d.style.transform = `translateX(${currentX}px) translateY(${currentY}px) translateZ(-100px)`;
    requestAnimationFrame(animateParallax);
}
animateParallax();

// Galaxy Star System with Cursor Interaction
const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let w, h, dpr, stars;
const STAR_COUNT = 400;
const TAU = Math.PI * 2;
let cursorX = 0, cursorY = 0;
let time = 0;

function resize() {
    dpr = Math.max(1, window.devicePixelRatio || 1);
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

// Star class with properties
class Star {
    constructor() {
        this.reset();
        this.y = Math.random() * h;
        this.x = Math.random() * w;
    }
    
    reset() {
        this.x = Math.random() * w;
        this.y = Math.random() * h;
        this.z = Math.random() * 2000;
        this.size = Math.random() * 2.5 + 0.5;
        this.baseSpeed = Math.random() * 0.3 + 0.1;
        this.vx = (Math.random() - 0.5) * this.baseSpeed;
        this.vy = (Math.random() - 0.5) * this.baseSpeed;
        this.vz = (Math.random() - 0.5) * 1.5;
        
        // Pure white stars only
        this.color = { r: 255, g: 255, b: 255, a: 1 };
        
        // Twinkle properties
        this.twinkleSpeed = Math.random() * 0.03 + 0.01;
        this.twinklePhase = Math.random() * TAU;
        
        // Layer depth for parallax
        this.layer = Math.floor(this.z / 500);
    }
}

function init() {
    stars = Array.from({length: STAR_COUNT}, () => new Star());
}

function project3D(x, y, z) {
    const fov = 800;
    const scale = fov / (fov + z);
    return {
        sx: x * scale + w / 2,
        sy: y * scale + h / 2,
        scale: scale
    };
}

function step() {
    time += 0.01;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, w, h);
    
    // No cursor glow effects - pure black background
    
    for (const star of stars) {
        // Cursor interaction - stars move away from cursor
        const dx = star.x - cursorX;
        const dy = star.y - cursorY;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const maxDist = 200;
        
        if (dist < maxDist && dist > 0) {
            const force = (1 - dist / maxDist) * 0.8;
            star.vx += (dx / dist) * force;
            star.vy += (dy / dist) * force;
        }
        
        // Apply friction to smooth movement
        star.vx *= 0.98;
        star.vy *= 0.98;
        
        // Update position
        star.x += star.vx;
        star.y += star.vy;
        star.z += star.vz;
        
        // Wrap around screen edges
        if (star.x < -100) star.x = w + 100;
        if (star.x > w + 100) star.x = -100;
        if (star.y < -100) star.y = h + 100;
        if (star.y > h + 100) star.y = -100;
        if (star.z < 0) star.z = 2000;
        if (star.z > 2000) star.z = 0;
        
        // Calculate twinkle effect
        star.twinklePhase += star.twinkleSpeed;
        const twinkle = 0.7 + Math.sin(star.twinklePhase) * 0.3;
        
        // Calculate depth-based opacity
        const depthOpacity = 1 - (star.z / 2000) * 0.7;
        
        // Draw star with glow
        const size = star.size * depthOpacity;
        
        // Outer glow
        const glowGrad = ctx.createRadialGradient(
            star.x, star.y, 0,
            star.x, star.y, size * 4
        );
        glowGrad.addColorStop(0, `rgba(${star.color.r}, ${star.color.g}, ${star.color.b}, ${twinkle * depthOpacity * 0.8})`);
        glowGrad.addColorStop(0.5, `rgba(${star.color.r}, ${star.color.g}, ${star.color.b}, ${twinkle * depthOpacity * 0.3})`);
        glowGrad.addColorStop(1, 'transparent');
        
        ctx.beginPath();
        ctx.arc(star.x, star.y, size * 4, 0, TAU);
        ctx.fillStyle = glowGrad;
        ctx.fill();
        
        // Core star
        ctx.beginPath();
        ctx.arc(star.x, star.y, size, 0, TAU);
        ctx.fillStyle = `rgba(${star.color.r}, ${star.color.g}, ${star.color.b}, ${twinkle * depthOpacity})`;
        ctx.fill();
        
        // Bright center
        ctx.beginPath();
        ctx.arc(star.x, star.y, size * 0.5, 0, TAU);
        ctx.fillStyle = `rgba(255, 255, 255, ${twinkle * depthOpacity})`;
        ctx.fill();
    }
    
    requestAnimationFrame(step);
}

// Update cursor position for star interaction
document.addEventListener('mousemove', (e) => {
    cursorX = e.clientX;
    cursorY = e.clientY;
});

window.addEventListener('resize', () => { resize(); init(); });
resize();
init();
step();

// UI Functions
function toggleAccordion(header) {
    const content = header.nextElementSibling;
    const isActive = content.classList.contains('active');
    
    document.querySelectorAll('.accordion-content').forEach(c => {
        c.classList.remove('active');
    });
    
    if (!isActive) {
        content.classList.add('active');
    }
}

function switchTab(tabName, eventElement) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    
    if (eventElement) {
        eventElement.classList.add('active');
    }
    document.getElementById(tabName + 'Tab').classList.add('active');
}

// Temperature slider
document.getElementById('temperature').addEventListener('input', (e) => {
    document.getElementById('tempValue').textContent = e.target.value;
});

// Form submission
document.getElementById('storyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        model: document.getElementById('model').value,
        temperature: parseFloat(document.getElementById('temperature').value),
        genre: document.getElementById('genre').value,
        character1_name: document.getElementById('character1_name').value,
        character2_name: document.getElementById('character2_name').value,
        character1_appearance: document.getElementById('character1_appearance').value,
        character1_vehicle: document.getElementById('character1_vehicle').value,
        character1_weapons: document.getElementById('character1_weapons').value,
        character2_appearance: document.getElementById('character2_appearance').value,
        character2_vehicle: document.getElementById('character2_vehicle').value,
        character2_weapons: document.getElementById('character2_weapons').value,
        custom_prompt: document.getElementById('custom_prompt').value,
        num_images: parseInt(document.getElementById('num_images').value)
    };
    
    // Show loading
    document.getElementById('loading').classList.add('active');
    document.getElementById('outputSection').style.display = 'none';
    document.getElementById('errorMsg').classList.remove('active');
    document.getElementById('generateBtn').disabled = true;
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display story
            document.getElementById('storyOutput').innerHTML = convertMarkdown(data.story);
            
            // Display images - using safe DOM manipulation
            const gallery = document.getElementById('imageGallery');
            gallery.innerHTML = '';
            data.images.forEach((img, idx) => {
                const item = document.createElement('div');
                item.className = 'gallery-item';
                
                // Create image element
                const imgEl = document.createElement('img');
                imgEl.src = img.image;
                imgEl.alt = `Scene ${idx + 1}`;
                item.appendChild(imgEl);
                
                // Create scene info
                const sceneInfo = document.createElement('div');
                sceneInfo.className = 'scene-info';
                
                const h4 = document.createElement('h4');
                h4.textContent = `Scene ${idx + 1}`;
                sceneInfo.appendChild(h4);
                
                const p = document.createElement('p');
                p.textContent = img.scene;
                sceneInfo.appendChild(p);
                
                // Add dialogues if available
                if (img.dialogues && img.dialogues.length > 0) {
                    const dialogueDiv = document.createElement('div');
                    dialogueDiv.className = 'dialogue';
                    
                    img.dialogues.forEach(d => {
                        const dialogueText = document.createElement('div');
                        const strong = document.createElement('strong');
                        strong.textContent = d.speaker + ': ';
                        dialogueText.appendChild(strong);
                        dialogueText.appendChild(document.createTextNode('"' + d.text + '"'));
                        dialogueDiv.appendChild(dialogueText);
                    });
                    
                    sceneInfo.appendChild(dialogueDiv);
                }
                
                item.appendChild(sceneInfo);
                gallery.appendChild(item);
            });
            
            document.getElementById('outputSection').style.display = 'block';
        } else {
            throw new Error(data.error || 'Failed to generate story');
        }
    } catch (error) {
        document.getElementById('errorMsg').textContent = 'Error: ' + error.message;
        document.getElementById('errorMsg').classList.add('active');
    } finally {
        document.getElementById('loading').classList.remove('active');
        document.getElementById('generateBtn').disabled = false;
    }
});

// Simple markdown to HTML converter
function convertMarkdown(text) {
    return text
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
        .replace(/\n/gim, '<br>');
}

