// Typed.js initialization (guarded so missing library does not break other scripts)
if (typeof Typed !== 'undefined' && document.querySelector('.texted')) {
    new Typed(".texted", {
        strings: ["Web Applications", "Digital Solutions", "UI/UX Designs", "E-Commerce Sites"],
        typeSpeed: 90,
        backSpeed: 70,
        backDelay: 500,
        loop: true
    });
}

// --- MOBILE NAVBAR SIDEBAR LOGIC ---
const menuToggle = document.getElementById('menu-toggle');
const navbar = document.getElementById('navbar');
const overlay = document.getElementById('overlay');

function updateMenuIcon(isOpen) {
    if (!menuToggle) return;
    const icon = menuToggle.querySelector('i');
    if (!icon) return;

    icon.classList.toggle('bx-menu', !isOpen);
    icon.classList.toggle('bx-x', isOpen);
    menuToggle.setAttribute('aria-expanded', String(isOpen));
}

function closeSidebar() {
    if (!navbar || !overlay) return;
    navbar.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    updateMenuIcon(false);
}

// Function to open/close sidebar
function toggleSidebar() {
    if (!navbar || !overlay) return;
    const isOpen = navbar.classList.toggle('active');
    overlay.classList.toggle('active', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
    updateMenuIcon(isOpen);
}

// Event Listeners
if (menuToggle && navbar && overlay) {
    menuToggle.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);
}

// Close sidebar when clicking a link inside it
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (navbar && navbar.classList.contains('active')) {
            closeSidebar();
        }
    });
});

window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        closeSidebar();
    }
});


// --- CHATBOT LOGIC ---

function toggleChatbot() {
    const container = document.getElementById('chatbot-container');
    if (container) {
        container.classList.toggle('active');
    }
}

function handleEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    // Add User Message to UI
    addMessage(message, 'user-msg');
    input.value = '';

    // Send to Flask Backend -> OpenAI
    fetch('/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        addMessage(data.response, 'bot-msg');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage("Error connecting to server.", 'bot-msg');
    });
}

function addMessage(text, className) {
    const body = document.getElementById('chatbot-body');
    if (!body) return;
    
    const msgDiv = document.createElement('div');
    msgDiv.classList.add(className);
    msgDiv.innerText = text;
    body.appendChild(msgDiv);
    
    // Auto scroll to bottom
    body.scrollTop = body.scrollHeight;
}
